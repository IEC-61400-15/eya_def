"""JSON Schema utilities related to the ``pydantic`` package.

"""

from typing import Any, Type

import pydantic as pdt


def add_null_type_to_schema_optional_fields(
    schema: dict[str, Any], model: Type[pdt.BaseModel]
) -> None:
    """Add ``null`` as a type to all optional fields in a schema.

    :param schema: the model schema dictionary to modify
    :param model: the ``pydantic`` model for which the schema is created
    """
    for prop, value in schema.get("properties", {}).items():
        field = [x for x in model.__fields__.values() if x.alias == prop][0]
        if field.allow_none:
            if "type" in value:
                value["type"] = [value["type"], "null"]


def move_field_to_definitions(
    schema: dict[str, Any], defined_field_dict: dict[str, str]
) -> None:
    """Move the details of a field to the ``definitions`` section.

    :param schema: the model schema dictionary to modify
    :param defined_field_dict: a dictionary mapping model field labels
        onto definition labels
    """
    for field_label, definition_label in defined_field_dict.items():
        field_definition = _find_field_definition(
            schema=schema, field_label=field_label
        )
        if field_definition is None:
            raise ValueError(
                f"the field {defined_field_dict} was not found in the schema"
            )
        schema["definitions"][definition_label] = field_definition
        _recursive_replace_field_definition(
            schema=schema, field_label=field_label, field_definition=field_definition
        )


def reduce_json_schema_all_of(schema: dict[str, Any]) -> None:
    """Get copy of JSON Schema ``dict`` without superfluous ``allOf``.

    :param schema: the original schema ``dict``
    :return: a copy of ``schema`` where ``allOf`` definitions are
        removed for instanced where there is only one item
    """
    for key, value in schema.copy().items():
        if isinstance(value, dict):
            reduce_json_schema_all_of(value)
        elif key == "allOf" and isinstance(value, list) and len(value) == 1:
            schema.update(value[0].items())
            del schema["allOf"]


def tuple_fields_to_prefix_items(schema: dict[str, Any]) -> None:
    """Convert ``items`` to ``prefixItems`` for tuple fields.

    :param schema: the model schema dictionary to modify
    """
    if (
        "items" in schema
        and "minItems" in schema
        and "maxItems" in schema
        and schema["minItems"] == schema["maxItems"]
    ):
        schema["prefixItems"] = schema["items"]
        schema["items"] = False
    else:
        for key, value in schema.items():
            if isinstance(value, dict):
                tuple_fields_to_prefix_items(schema=value)
            elif isinstance(value, list):
                for list_value in value:
                    if isinstance(list_value, dict):
                        tuple_fields_to_prefix_items(schema=list_value)


def _find_field_definition(
    schema: dict[str, Any], field_label: str
) -> dict[str, Any] | None:
    for key, value in schema.items():
        if isinstance(value, dict):
            if key == "properties" and field_label in value.keys():
                return value[field_label]
            else:
                return _find_field_definition(schema=value, field_label=field_label)
    return None


def _recursive_replace_field_definition(
    schema: dict[str, Any], field_label: str, field_definition: dict[str, Any]
) -> None:
    for key, value in schema.items():
        if isinstance(value, dict):
            if key == "properties" and field_label in value.keys():
                value[field_label] = {"$ref": f"#/definitions/{field_label.title()}"}
            else:
                _recursive_replace_field_definition(
                    schema=value,
                    field_label=field_label,
                    field_definition=field_definition,
                )
