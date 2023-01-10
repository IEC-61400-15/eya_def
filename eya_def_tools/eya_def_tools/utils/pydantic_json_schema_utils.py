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
    json_dict: dict[str, Any], field_label: str
) -> dict[str, Any]:
    """Move the details of a field to the ``definitions`` section.

    :param json_dict: the model schema dictionary to modify
    :param field_label: the label of the model field to move to the
        ``definitions`` section
    :return: a copy of ``json_dict`` where the ``properties`` and
        ``definitions`` sections have been updated
    """
    updated_json_dict = json_dict.copy()
    field_definition = _find_field_definition(
        json_dict=json_dict, field_label=field_label
    )
    if field_definition is None:
        raise ValueError(f"the field {field_label} was not found in the schema")
    updated_json_dict["definitions"][field_label.title()] = field_definition
    _recursive_replace_field_definition(
        json_dict=json_dict, field_label=field_label, field_definition=field_definition
    )
    return updated_json_dict


def reduce_json_schema_all_of(json_dict: dict[str, Any]) -> dict[str, Any]:
    """Get copy of JSON Schema ``dict`` without superfluous ``allOf``.

    :param json_dict: the original ``dict`` in JSON format
    :return: a copy of ``json_dict`` where ``allOf`` definitions are
        removed for instanced where there is only one item
    """
    reduced_json_dict = {}
    for key, value in json_dict.items():
        if isinstance(value, dict):
            reduced_json_dict[key] = reduce_json_schema_all_of(value)
        elif key == "allOf" and isinstance(value, list) and len(value) == 1:
            reduced_json_dict.update(value[0].items())
        else:
            reduced_json_dict[key] = value
    return reduced_json_dict


def _find_field_definition(
    json_dict: dict[str, Any], field_label: str
) -> dict[str, Any] | None:
    for key, value in json_dict.items():
        if isinstance(value, dict):
            if key == "properties" and field_label in value.keys():
                return value[field_label]
            else:
                return _find_field_definition(json_dict=value, field_label=field_label)
    return None


def _recursive_replace_field_definition(
    json_dict: dict[str, Any], field_label: str, field_definition: dict[str, Any]
) -> None:
    for key, value in json_dict.items():
        if isinstance(value, dict):
            if key == "properties" and field_label in value.keys():
                value[field_label] = {"$ref": f"#/definitions/{field_label.title()}"}
            else:
                _recursive_replace_field_definition(
                    json_dict=value,
                    field_label=field_label,
                    field_definition=field_definition,
                )
