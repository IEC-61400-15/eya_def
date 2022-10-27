# -*- coding: utf-8 -*-
"""Test the `eya_def_tools.data_model` module.

"""


def test_initiate_energy_assessment_report_a(energy_assessment_report_a):
    """Assert test case instance 'a' is successfully initiated."""
    from eya_def_tools.data_model import EnergyAssessmentReport
    assert bool(energy_assessment_report_a)
    assert isinstance(
        energy_assessment_report_a, EnergyAssessmentReport)


def test_make_model_raw_schema(energy_assessment_report_a):
    """Test that the raw schema is successfully created."""
    schema = energy_assessment_report_a.schema()
    assert bool(schema)
    assert isinstance(schema, dict)


def test_make_model_final_json_schema(pydantic_json_schema):
    """Test that the final json schema is successfully created."""
    assert bool(pydantic_json_schema)
    assert isinstance(pydantic_json_schema, dict)


def test_export_json_schema(pydantic_json_schema_tmp_path):
    """Test that the json schema is exported to temporary file."""
    assert pydantic_json_schema_tmp_path.is_file()
