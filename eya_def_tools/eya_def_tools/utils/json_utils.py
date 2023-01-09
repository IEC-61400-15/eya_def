"""Utilities associated with the JSON format.

"""


def reduce_json_all_of(json_dict: dict) -> dict:
    """Get copy of JSON ``dict`` without superfluous ``allOf``.

    :param json_dict: the original ``dict`` in JSON format
    :return: a copy of ``json_dict`` where ``allOf`` definitions are
        removed for instanced where there is only one item
    """
    reduced_json_dict = {}
    for key, val in json_dict.items():
        if isinstance(val, dict):
            reduced_json_dict[key] = reduce_json_all_of(val)
        elif key == "allOf" and isinstance(val, list) and len(val) == 1:
            reduced_json_dict.update(val[0].items())
        else:
            reduced_json_dict[key] = val
    return reduced_json_dict
