"""Modified pydantic base model for the EYA DEF."""

import json
import re
from typing import Any

import pydantic as pdt
import pydantic.json_schema as pdt_json_schema
import pydantic_core as pdt_core

from eya_def_tools.constants import (
    ALL_OF_TAG,
    DEFINITIONS_TAG,
    EXTERNAL_REFERENCE_TAG,
    REFERENCE_TAG,
)


class EyaDefGenerateJsonSchema(pdt_json_schema.GenerateJsonSchema):
    """Custom JSON Schema generator for the EYA DEF top-level model."""

    def generate(
        self,
        schema: pdt_core.CoreSchema,
        mode: pdt_json_schema.JsonSchemaMode = "validation",
    ) -> pdt_json_schema.JsonSchemaValue:
        """Generate a JSON Schema from a pydantic schema.

        :param schema: the pydantic code schema to generate the JSON
            Schema for
        :param mode: the mode in which to generate the JSON Schema
        :return: a ``dict`` representation of the JSON Schema
        """
        json_schema_dict = super().generate(schema=schema, mode=mode)
        json_schema_dict["$schema"] = self.schema_dialect
        self.reduce_json_schema_single_use_definitions(
            json_schema_dict=json_schema_dict
        )
        return json_schema_dict

    @classmethod
    def reduce_json_schema_single_use_definitions(
        cls, json_schema_dict: dict[str, Any]
    ) -> None:
        """Move single use definitions to where they are used.

        The current behaviour of the pydantic JSON Schema generator is
        to include all sub-model definitions in the ``$defs`` section.
        This function modifies the standard pydantic schema to define
        only sub-models used in more than one place in ``$defs`` and
        define single use models in the hierarchical tree of properties
        instead.

        :param json_schema_dict: the model JSON Schema dictionary to
            modify in place
        """
        if DEFINITIONS_TAG not in json_schema_dict:
            return

        for definition_label in json_schema_dict[DEFINITIONS_TAG].copy():
            definition_count = cls._recursive_get_definition_count(
                json_schema_dict=json_schema_dict, definition_label=definition_label
            )
            if definition_count < 2:
                cls._recursive_move_definition_to_tree(
                    json_schema_dict=json_schema_dict,
                    definition_label=definition_label,
                    definition=json_schema_dict[DEFINITIONS_TAG][definition_label],
                )
                del json_schema_dict[DEFINITIONS_TAG][definition_label]

    @classmethod
    def _recursive_get_definition_count(
        cls,
        json_schema_dict: Any,
        definition_label: str,
    ) -> int:
        if not isinstance(json_schema_dict, dict):
            return 0

        count = 0
        for value in json_schema_dict.values():
            if value == f"#/{DEFINITIONS_TAG}/{definition_label}":
                return count + 1
            elif isinstance(value, dict):
                count = count + cls._recursive_get_definition_count(
                    json_schema_dict=value, definition_label=definition_label
                )
            elif isinstance(value, list):
                for item in value:
                    count = count + cls._recursive_get_definition_count(
                        json_schema_dict=item, definition_label=definition_label
                    )

        return count

    @classmethod
    def _recursive_move_definition_to_tree(
        cls,
        json_schema_dict: Any,
        definition_label: str,
        definition: dict[str, Any],
    ) -> None:
        if not isinstance(json_schema_dict, dict):
            return

        for key, value in json_schema_dict.copy().items():
            cls._process_definition_to_tree_schema_item(
                key=key,
                value=value,
                json_schema_dict=json_schema_dict,
                definition_label=definition_label,
                definition=definition,
            )

    @classmethod
    def _process_definition_to_tree_schema_item(
        cls,
        key: str,
        value: Any,
        json_schema_dict: Any,
        definition_label: str,
        definition: dict[str, Any],
    ) -> None:
        if key == REFERENCE_TAG and value == f"#/{DEFINITIONS_TAG}/{definition_label}":
            cls._move_definition(
                json_schema_dict=json_schema_dict,
                definition=definition,
            )
            del json_schema_dict[REFERENCE_TAG]

        elif isinstance(value, dict):
            cls._recursive_move_definition_to_tree(
                json_schema_dict=value,
                definition_label=definition_label,
                definition=definition,
            )

        elif isinstance(value, list):
            if (
                key == ALL_OF_TAG
                and len(value) == 1
                and isinstance(value[0], dict)
                and value[0]
                == {REFERENCE_TAG: f"#/{DEFINITIONS_TAG}/{definition_label}"}
            ):
                cls._move_definition(
                    json_schema_dict=json_schema_dict,
                    definition=definition,
                )
                del json_schema_dict[ALL_OF_TAG]

            else:
                for item in value:
                    cls._recursive_move_definition_to_tree(
                        json_schema_dict=item,
                        definition_label=definition_label,
                        definition=definition,
                    )

    @classmethod
    def _move_definition(
        cls,
        json_schema_dict: dict[str, Any],
        definition: dict[str, Any],
    ) -> None:
        schema_copy = json_schema_dict.copy()
        json_schema_dict.update(definition)
        json_schema_dict["title"] = re.sub(
            r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))",
            r" \1",
            json_schema_dict["title"],
        )
        for field_attribute in ["title", "description"]:
            if field_attribute in schema_copy:
                json_schema_dict[field_attribute] = schema_copy[field_attribute]


class EyaDefBaseModel(pdt.BaseModel):
    """Base pydantic model for the EYA DEF.

    This base model includes some adaptations to ``pydantic.BaseModel``
    to tune the output JSON Schema as desired.
    """

    model_config = pdt.ConfigDict(
        # The model config ``extra="forbid"`` is equivalent of the JSON
        # Schema specification ``"additionalProperties": false``, which
        # is used as the default, not to allow any further fields
        extra="forbid",
        # As a default, infinity of nan float values are not permitted
        allow_inf_nan=False,
    )

    @classmethod
    def model_json_schema(
        cls,
        by_alias: bool = True,
        ref_template: str = pdt_json_schema.DEFAULT_REF_TEMPLATE,
        schema_generator: type[
            pdt_json_schema.GenerateJsonSchema
        ] = EyaDefGenerateJsonSchema,
        mode: pdt_json_schema.JsonSchemaMode = "validation",
    ) -> pdt_json_schema.JsonSchemaValue:
        """Generate a JSON Schema dictionary for a model class.

        This class method is identical to the one defined on
        ``pydantic.BaseModel``, except that it uses the custom JSON
        Schema generator class ``EyaDefGenerateJsonSchema`` instead of
        the default ``GenerateJsonSchema``.

        :param by_alias: whether to use field aliases
        :param ref_template: the reference template to use
        :param schema_generator: the JSON Schema generator class, which
            defaults to the ``EyaDefGenerateJsonSchema`` class
        :param mode: the mode in which to generate the JSON Schema
        :return: a ``dict`` representation of the JSON Schema
        """
        return pdt_json_schema.model_json_schema(
            cls,
            by_alias=by_alias,
            ref_template=ref_template,
            schema_generator=schema_generator,
            mode=mode,
        )

    @classmethod
    def model_json_schema_str(
        cls,
        by_alias: bool = True,
        ref_template: str = pdt_json_schema.DEFAULT_REF_TEMPLATE,
        schema_generator: type[
            pdt_json_schema.GenerateJsonSchema
        ] = EyaDefGenerateJsonSchema,
        mode: pdt_json_schema.JsonSchemaMode = "validation",
        indent: int = 2,
    ) -> str:
        """Generate a JSON Schema string for a model class.

        Single and double newline characters are replaced by spaces.

        See also documentation of ``model_json_schema``.

        :param by_alias: whether to use field aliases
        :param ref_template: the reference template to use
        :param schema_generator: the JSON Schema generator class, which
            defaults to the ``EyaDefGenerateJsonSchema`` class
        :param mode: the mode in which to generate the JSON Schema
        :param indent: the indentation to use in the JSON string
        :return: a ``str`` representation of the JSON Schema
        """
        return (
            json.dumps(
                obj=cls.model_json_schema(
                    by_alias=by_alias,
                    ref_template=ref_template,
                    schema_generator=schema_generator,
                    mode=mode,
                ),
                indent=indent,
            )
            .replace(r"\n\n", " ")
            .replace(r"\n", " ")
            .replace(EXTERNAL_REFERENCE_TAG, REFERENCE_TAG)
        )
