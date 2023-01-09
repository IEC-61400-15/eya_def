"""JSON Schema utilities.

"""

from typing import Any, Type

import pydantic as pdt


def reduce_json_schema_all_of(json_dict: dict) -> dict:
    """Get copy of JSON ``dict`` without superfluous ``allOf``.

    :param json_dict: the original ``dict`` in JSON format
    :return: a copy of ``json_dict`` where ``allOf`` definitions are
        removed for instanced where there is only one item
    """
    reduced_json_dict = {}
    for key, val in json_dict.items():
        if isinstance(val, dict):
            reduced_json_dict[key] = reduce_json_schema_all_of(val)
        elif key == "allOf" and isinstance(val, list) and len(val) == 1:
            reduced_json_dict.update(val[0].items())
        else:
            reduced_json_dict[key] = val
    return reduced_json_dict


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
