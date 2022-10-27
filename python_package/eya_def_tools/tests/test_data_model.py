# -*- coding: utf-8 -*-
"""Test the `eya_def_tools.data_model` module.

"""

import json


def test_metadata_ref_iea43_model_json_round_trip_conversion(
        wind_measurement_campaign_a):
    """Test `metadata_ref_iea43_mode` json round-trip conversion."""
    from eya_def_tools.data_model import WindMeasurementCampaign
    wind_measurement_campaign_a_conv = WindMeasurementCampaign(
        **json.loads(wind_measurement_campaign_a.json()))
    assert (wind_measurement_campaign_a.metadata_ref_iea43_model
            == wind_measurement_campaign_a_conv.metadata_ref_iea43_model)


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


# TODO: TEMPORARY CODE
def test_copy_pydantic_json_schema(pydantic_json_schema_tmp_path):
    """Temporary test to copy pydantic schema."""
    from pathlib import Path
    import shutil
    shutil.copy(
        pydantic_json_schema_tmp_path,
        Path("iec_61400-15-2_eya_def.schema.json"))


# TODO: TEMPORARY CODE
def test_copy_energy_assessment_report_a(
        energy_assessment_report_a_tmp_filepath):
    """Temporary test to copy pydantic example 'a'."""
    from pathlib import Path
    import shutil
    shutil.copy(
        energy_assessment_report_a_tmp_filepath,
        Path("iec_61400-15-2_eya_def_example_a.json"))
