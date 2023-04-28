"""Test ``eya_def_tools.data_model.energy_yield_assessment`` on examples.

"""

from typing import Any

import jsonschema
import pydantic as pdt
import pytest


def test_validate_master_json_schema(
    master_json_schema: dict[str, Any], json_example_dict: dict[str, Any]
) -> None:
    """Test validate all json file examples against master schema."""
    for json_filename, json_example in json_example_dict.items():
        try:
            jsonschema.validate(instance=json_example, schema=master_json_schema)
        except jsonschema.exceptions.ValidationError as exc:
            pytest.fail(
                f"the json example '{json_filename}' did not pass the "
                f"master json schema validation ({exc})"
            )
        except jsonschema.exceptions.RefResolutionError:
            # Several examples have dummy references, so we accept that
            # some references cannot be resolved
            pass


def test_validate_pydantic_model_json_schema(
    pydantic_json_schema: dict[str, Any], json_example_dict: dict[str, Any]
) -> None:
    """Test validate all json file examples against pydantic schema."""
    for json_filename, json_example in json_example_dict.items():
        try:
            jsonschema.validate(instance=json_example, schema=pydantic_json_schema)
        except jsonschema.exceptions.ValidationError as exc:
            pytest.fail(
                f"the json example '{json_filename}' did not pass the "
                f"pydantic model json schema validation ({exc})"
            )
        except jsonschema.exceptions.RefResolutionError:
            # Several examples have dummy references, so we accept that
            # some references cannot be resolved
            pass


def test_validate_pydantic_model(json_example_dict: dict[str, Any]) -> None:
    """Test validate all json file examples against pydantic model."""
    from eya_def_tools.data_models.eya_def import EyaDef

    for json_filename, json_example in json_example_dict.items():
        try:
            energy_yield_assessment = EyaDef(**json_example)
            assert isinstance(energy_yield_assessment, EyaDef)
        except pdt.ValidationError as exc:
            pytest.fail(
                f"the json example '{json_filename}' did not pass the "
                f"pydantic model json schema validation ({exc})"
            )
