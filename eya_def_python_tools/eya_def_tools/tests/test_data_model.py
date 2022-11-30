# -*- coding: utf-8 -*-
"""Test the ``eya_def_tools.data_model`` module.

"""

import json


def test_initiate_energy_yield_assessment_a(energy_yield_assessment_a):
    """Assert test case instance 'a' is successfully initiated."""
    from eya_def_tools.data_model import EnergyYieldAssessment
    assert bool(energy_yield_assessment_a)
    assert isinstance(
        energy_yield_assessment_a, EnergyYieldAssessment)


def test_energy_yield_assessment_round_trip_conversion(energy_yield_assessment_a):
    """Test ``EnergyYieldAssessment`` example json round-trip conversion."""
    from eya_def_tools.data_model import EnergyYieldAssessment
    energy_yield_assessment_a_conv = EnergyYieldAssessment(
        **json.loads(energy_yield_assessment_a.json(
            exclude_none=True, by_alias=True)))
    assert energy_yield_assessment_a == energy_yield_assessment_a_conv


def test_make_model_raw_schema(energy_yield_assessment_a):
    """Test that the raw schema is successfully created."""
    schema = energy_yield_assessment_a.schema()
    assert bool(schema)
    assert isinstance(schema, dict)


def test_make_model_final_json_schema(pydantic_json_schema):
    """Test that the final json schema is successfully created."""
    assert bool(pydantic_json_schema)
    assert isinstance(pydantic_json_schema, dict)


def test_export_json_schema(pydantic_json_schema_tmp_path):
    """Test that the json schema is exported to temporary file."""
    assert pydantic_json_schema_tmp_path.is_file()


# # TODO: TEMPORARY CODE
# def test_copy_pydantic_json_schema(pydantic_json_schema_tmp_path):
#     """Temporary test to copy pydantic schema."""
#     from pathlib import Path
#     import shutil
#     shutil.copy(
#         pydantic_json_schema_tmp_path,
#         Path("iec_61400-15-2_eya_def.schema.json"))
#
#
# # TODO: TEMPORARY CODE
# def test_copy_energy_yield_assessment_a(
#         energy_yield_assessment_a_tmp_filepath):
#     """Temporary test to copy pydantic example 'a'."""
#     from pathlib import Path
#     import shutil
#     shutil.copy(
#         energy_yield_assessment_a_tmp_filepath,
#         Path("iec_61400-15-2_eya_def_example_a.json"))
