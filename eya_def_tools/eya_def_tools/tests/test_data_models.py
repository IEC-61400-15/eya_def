"""Test the ``eya_def_tools.data_model.energy_yield_assessment`` module.

"""

import json
from pathlib import Path
from typing import Any

from eya_def_tools.data_models.energy_yield_assessment import EnergyYieldAssessment


def test_initiate_energy_yield_assessment_a(
    energy_yield_assessment_a: EnergyYieldAssessment,
) -> None:
    """Assert test case instance 'a' is successfully initiated."""
    assert isinstance(energy_yield_assessment_a, EnergyYieldAssessment)


def test_energy_yield_assessment_round_trip_conversion(
    energy_yield_assessment_a: EnergyYieldAssessment,
) -> None:
    """Test ``EnergyYieldAssessment`` example json round-trip conversion."""
    energy_yield_assessment_a_conv = EnergyYieldAssessment(
        **json.loads(energy_yield_assessment_a.json(exclude_none=True, by_alias=True))
    )
    assert energy_yield_assessment_a == energy_yield_assessment_a_conv


def test_make_model_raw_schema(
    energy_yield_assessment_a: EnergyYieldAssessment,
) -> None:
    """Test that the raw schema is successfully created."""
    schema = energy_yield_assessment_a.schema()
    assert schema is not None
    assert isinstance(schema, dict)


def test_make_model_final_json_schema(pydantic_json_schema: dict[str, Any]) -> None:
    """Test that the final json schema is successfully created."""
    assert pydantic_json_schema is not None
    assert isinstance(pydantic_json_schema, dict)


def test_export_json_schema(pydantic_json_schema_tmp_path: Path) -> None:
    """Test that the json schema is exported to temporary file."""
    assert pydantic_json_schema_tmp_path.is_file()


# # TODO: TEMPORARY CODE
# def test_copy_pydantic_json_schema(pydantic_json_schema_tmp_path: Path) -> None:
#     """Temporary test to copy pydantic schema."""
#     import shutil
#
#     shutil.copy(
#         pydantic_json_schema_tmp_path, Path("iec_61400-15-2_eya_def.schema.json")
#     )
#
#
# # TODO: TEMPORARY CODE
# def test_copy_energy_yield_assessment_a(
#     energy_yield_assessment_a_tmp_filepath: Path
# ) -> None:
#     """Temporary test to copy pydantic example 'a'."""
#     import shutil
#
#     shutil.copy(
#         energy_yield_assessment_a_tmp_filepath,
#         Path("iec_61400-15-2_eya_def_example_a.json"),
#     )
