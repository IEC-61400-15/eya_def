"""Utility functions to get up-to-date references.

"""


def get_json_schema_reference_uri() -> str:
    """Get the reference JSON Schema URI of the EYA DEF JSON Schema.

    :return: the public URI of the JSON Schema reference used
    """
    # TODO automate the checking of this version and link
    return "https://json-schema.org/draft/2020-12/schema"


def get_json_schema_uri() -> str:
    """Get the URI of the EYA DEF JSON Schema.

    :return: the public URI of the latest released version of the JSON
        Schema
    """
    # TODO this is a placeholder to be updated (and consider including
    #      version in URI)
    return (
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
