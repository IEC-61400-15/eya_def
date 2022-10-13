# -*- coding: utf-8 -*-
"""Test the `iec_eya_def_tools.data_model` module.

"""


def test_make_model_raw_schema():
    """Test that the raw schema is successfully created."""
    from iec_eya_def_tools.data_model import EnergyAssessmentReport
    schema = EnergyAssessmentReport.schema()
    assert schema
    print(schema)
    assert isinstance(schema, dict)


def test_make_model_final_json_schema(pydantic_json_schema):
    """Test that the final json schema is successfully created."""
    assert pydantic_json_schema
    assert isinstance(pydantic_json_schema, dict)


def test_export_json_schema(pydantic_json_schema_tmp_path):
    """Test that the json schema is exported to temporary file."""
    assert pydantic_json_schema_tmp_path.is_file()
