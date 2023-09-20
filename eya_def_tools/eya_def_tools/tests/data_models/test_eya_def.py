"""Test the ``eya_def`` top-level data model module.

"""

import json
from pathlib import Path
from typing import Any

from eya_def_tools.data_models import eya_def


def test_initiate_eya_def_a(
    eya_def_a: eya_def.EyaDefDocument,
) -> None:
    """Assert test case instance 'a' is successfully initiated."""
    assert isinstance(eya_def_a, eya_def.EyaDefDocument)


def test_eya_def_round_trip_conversion(
    eya_def_a: eya_def.EyaDefDocument,
) -> None:
    """Test ``EyaDef`` example json round-trip conversion."""
    eya_def_a_conv = eya_def.EyaDefDocument(
        **json.loads(eya_def_a.model_dump_json(by_alias=True))
    )
    assert eya_def_a == eya_def_a_conv


def test_make_model_raw_schema(
    eya_def_a: eya_def.EyaDefDocument,
) -> None:
    """Test that the raw schema is successfully created."""
    schema = eya_def_a.model_dump(mode="python")
    assert schema is not None
    assert isinstance(schema, dict)


def test_generate_model_json_schema(pydantic_json_schema: dict[str, Any]) -> None:
    """Test that the final json schema is successfully created."""
    assert pydantic_json_schema is not None
    assert isinstance(pydantic_json_schema, dict)


def test_export_json_schema(pydantic_json_schema_tmp_path: Path) -> None:
    """Test that the json schema is exported to temporary file."""
    assert pydantic_json_schema_tmp_path.is_file()


# # TODO: TEMPORARY CODE TO GENERATE JSON SCHEMA
# def test_copy_pydantic_json_schema(pydantic_json_schema_tmp_path: Path) -> None:
#     """Temporary test to copy pydantic schema."""
#     import shutil
#
#     shutil.copy(
#         pydantic_json_schema_tmp_path, Path("iec_61400-15-2_eya_def.schema.json")
#     )
#
#
# # TODO: TEMPORARY CODE TO GENERATE JSON EXAMPLE
# def test_copy_eya_def_a(
#     eya_def_a_tmp_filepath: Path,
# ) -> None:
#     """Temporary test to copy pydantic example 'a'."""
#     import shutil
#
#     shutil.copy(
#         eya_def_a_tmp_filepath,
#         Path("iec_61400-15-2_eya_def_example_a.json"),
#     )
