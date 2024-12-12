"""Adaptation of the erdantic functionality for the EYA DEF.

This module comprises the custom classes and methods to refine how the
entity relationship diagrams (ERDs) are rendered. It includes adding
model field descriptions in the text that displays in the SVG graphics
when hovering over a model, adding JSON Schema types and refining some
of the type annotations.

"""

import html
import inspect
from typing import (
    Any,
    Collection,
    Literal,
    Self,
    Sequence,
    Type,
    TypeGuard,
    Union,
    get_args,
    get_origin,
)

import erdantic.core as erd_core
import erdantic.exceptions as erd_exceptions
import erdantic.plugins as erd_plugins
import pydantic.errors as pdt_errors
import pydantic.fields as pdt_fields
import pydantic_core as pdt_core
import sortedcontainers_pydantic

from eya_def_tools.constants import ALL_OF_TAG, ANY_OF_TAG, REFERENCE_TAG
from eya_def_tools.data_models.base_model import EyaDefBaseModel

EyaDefBaseModelType = Type[EyaDefBaseModel]


class EyaDefFieldInfo(erd_core.FieldInfo):
    """Custom erdantic ``FieldInfo`` subclass for the EYA DEF."""

    json_schema_type_name: str = ""

    _dot_row_template = (
        """<tr>"""
        """<td>{name}</td>"""
        """<td>{type_name}</td>"""
        """<td port="{name}" width="36">{json_schema_type_name}</td>"""
        """</tr>"""
    )

    def to_dot_row(self) -> str:
        """Render the field info to DOT format."""
        return self._dot_row_template.format(
            name=self.name,
            type_name=self.type_name,
            json_schema_type_name=html.escape(self.json_schema_type_name),
        )


class EyaDefModelInfo(erd_core.ModelInfo[EyaDefBaseModelType]):
    """Custom erdantic ``ModelInfo`` subclass for the EYA DEF."""

    @classmethod
    def from_raw_model(cls, raw_model: EyaDefBaseModelType) -> Self:
        """Build model info from an EYA DEF model."""
        get_fields_fn = erd_plugins.identify_field_extractor_fn(raw_model)
        if not get_fields_fn:
            raise erd_exceptions.UnknownModelTypeError(
                model=raw_model,
                available_plugins=erd_plugins.list_plugins(),
            )

        full_name = erd_core.FullyQualifiedName.from_object(raw_model)
        description = _get_model_description(full_name=full_name, raw_model=raw_model)
        model_info = cls(
            full_name=full_name,
            name=raw_model.__name__,
            fields={
                field_info.name: field_info for field_info in get_fields_fn(raw_model)
            },
            description=description,
        )

        model_info._raw_model = raw_model

        return model_info


class EyaDefEntityRelationshipDiagram(erd_core.EntityRelationshipDiagram):
    """Custom ``EntityRelationshipDiagram`` subclass for the EYA DEF."""

    models: sortedcontainers_pydantic.SortedDict[str, EyaDefModelInfo] = (
        sortedcontainers_pydantic.SortedDict()
    )


def is_eya_def_model(obj: Any) -> TypeGuard[EyaDefBaseModelType]:
    """Predicate function to determine if an object is an EYA DEF model."""
    return inspect.isclass(obj) and issubclass(obj, EyaDefBaseModel)


def get_fields_from_eya_def_model(
    model: EyaDefBaseModelType,
) -> Sequence[EyaDefFieldInfo]:
    """Modified version of ``get_fields_from_pydantic_model()``."""
    try:
        model.model_rebuild()
    except pdt_errors.PydanticUndefinedAnnotation as exc:
        model_full_name = erd_core.FullyQualifiedName.from_object(model)
        forward_ref = exc.name
        message = (
            f"Failed to resolve forward reference '{forward_ref}' in the type "
            f"annotations for the model {model_full_name}. The model's "
            f"``model_rebuild()`` method should be used to manually resolve it."
        )
        raise erd_exceptions.UnresolvableForwardRefError(
            message,
            name=forward_ref,
            model_full_name=model_full_name,
        ) from exc

    model_json_schema = model.model_json_schema(by_alias=False)

    field_infos: list[EyaDefFieldInfo] = []
    for field_name, pydantic_field_info in model.model_fields.items():
        field_info = EyaDefFieldInfo.from_raw_type(
            model_full_name=erd_core.FullyQualifiedName.from_object(model),
            name=field_name,
            raw_type=pydantic_field_info.annotation or Any,  # type: ignore
        )

        field_info.json_schema_type_name = _get_field_json_schema_type(
            field_name=field_name,
            model_json_schema=model_json_schema,
        )

        abbreviated_field_type_name = _get_abbreviated_type_name(
            field_name=field_name,
            pydantic_field_info=pydantic_field_info,
        )
        if abbreviated_field_type_name is not None:
            field_info.type_name = abbreviated_field_type_name

        field_infos.append(field_info)

    return field_infos


def register_plugin() -> None:
    """Register the EYA DEF erdantic plugin.

    Calling this function will override the default pydantic plugin.
    """
    erd_plugins.register_plugin(
        key="pydantic",
        predicate_fn=is_eya_def_model,
        get_fields_fn=get_fields_from_eya_def_model,
    )


def create(
    model: EyaDefBaseModelType,
    terminal_models: Collection[type] = tuple(),
) -> EyaDefEntityRelationshipDiagram:
    diagram = EyaDefEntityRelationshipDiagram()

    for terminal_model in terminal_models:
        diagram.add_model(model=terminal_model, recurse=False)

    diagram.add_model(model=model)

    return diagram


def _get_abbreviated_type_name(
    field_name: str,
    pydantic_field_info: pdt_fields.FieldInfo,
) -> str | None:
    match field_name:
        case "measurement_stations" | "reference_meteorological_datasets":
            return "Optional[list[IEATask43WraDataModel]]"
        case "turbine_models":
            return "Optional[list[IEC61400d16PowerCurveDataModel]]"
        case "values":
            if (
                pydantic_field_info.description is not None
                and "Dataset value(s)" in pydantic_field_info.description
                and get_origin(pydantic_field_info.annotation) == Union
            ):
                return "Union[float, list[tuple[list[Union[int, float, str]], float]]]"
        case "return_period":
            if get_origin(pydantic_field_info.annotation) == Union:
                return "Optional[int | float]"
        case "basis":
            if get_origin(pydantic_field_info.annotation) == Literal:
                return "AssessmentComponentBasis"
        case "assessor_type":
            if get_origin(pydantic_field_info.annotation) == Literal:
                return "AssessorType"

    if get_origin(pydantic_field_info.annotation) == Literal:
        options = ", ".join(
            f"'{option}'" for option in get_args(pydantic_field_info.annotation)
        )
        return f"Literal[{options}]"

    return None


def _get_model_description(
    full_name: erd_core.FullyQualifiedName,
    raw_model: type[EyaDefBaseModel],
) -> str:
    description = str(full_name)

    docstring = inspect.getdoc(object=raw_model)
    if docstring:
        description += "\n\n" + docstring + "\n"

    if all(
        model_field.description is None
        for model_field in raw_model.model_fields.values()
    ):
        return description

    description += "\nFields:\n"
    for field_name, pydantic_field_info in raw_model.model_fields.items():
        if pydantic_field_info.description is None:
            continue

        description += (
            "    "
            + _get_field_description(
                field_name=field_name,
                pydantic_field_info=pydantic_field_info,
            ).strip()
            + "\n"
        )

    return description


def _get_field_description(
    field_name: str,
    pydantic_field_info: pdt_fields.FieldInfo,
) -> str:
    field_description = f"{field_name}: {pydantic_field_info.description}"

    if (
        not isinstance(pydantic_field_info.default, pdt_core.PydanticUndefinedType)
        and pydantic_field_info.default is not ...
    ):
        if not field_description.strip().endswith("."):
            field_description = field_description.rstrip() + ". "
        else:
            field_description = field_description.rstrip() + " "

        if isinstance(pydantic_field_info.default, str):
            field_description += f"Default is '{pydantic_field_info.default}'."
        else:
            field_description += f"Default is {pydantic_field_info.default}."

    return field_description


def _get_field_json_schema_type(
    field_name: str,
    model_json_schema: dict[str, Any],
) -> str:
    if "properties" not in model_json_schema.keys():
        return ""

    schema = model_json_schema["properties"]
    if field_name not in schema.keys():
        return ""

    schema = schema[field_name]
    if "type" in schema.keys():
        return str(schema["type"])

    if ALL_OF_TAG in schema.keys():
        schema = schema[ALL_OF_TAG]
        if not isinstance(schema, list):
            return ""

        if (
            len(schema) == 1
            and isinstance(schema[0], dict)
            and schema[0].keys() == {REFERENCE_TAG}
        ):
            return "object"

        return " & ".join(
            item["type"]
            for item in schema
            if isinstance(item, dict) and "type" in item.keys()
        )

    if ANY_OF_TAG in schema.keys():
        schema = schema[ANY_OF_TAG]
        if not isinstance(schema, list):
            return ""

        return " | ".join(
            item["type"]
            for item in schema
            if isinstance(item, dict) and "type" in item.keys()
        )

    return ""
