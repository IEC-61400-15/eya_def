"""Utility functions to get up-to-date references.

"""

import pydantic as pdt


def get_json_schema_uri() -> pdt.AnyUrl:
    """Get the URI of the EYA DEF JSON Schema.

    :return: the public URI of the latest released version of the JSON
        Schema
    """
    # TODO this is a placeholder to be updated (and consider including
    #      version in URI)
    return pdt.AnyUrl(
        "https://raw.githubusercontent.com/IEC-61400-15/eya_def/blob/main/"
        "iec_61400-15-2_eya_def.schema.json"
    )


def get_json_schema_version() -> str:
    """Get the current version string of the EYA DEF JSON Schema.

    :return: the semantic version string of the JSON Schema, following
        the format <major>.<minor>.<patch> (e.g. '1.2.3')
    """
    # TODO this is a placeholder to be updated (consider linking to git
    #      repo tags and consider how to distinguish JSON Schema and
    #      python package versions)
    return "0.0.1"
