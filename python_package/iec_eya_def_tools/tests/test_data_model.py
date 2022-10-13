# -*- coding: utf-8 -*-
"""Test the `iec_eya_def_tools.data_model` module.

"""


def test_export_json_schema(pydantic_json_schema_tmp_path):
    """Test that the json schema was exported to temporary file."""
    assert pydantic_json_schema_tmp_path.is_file()
