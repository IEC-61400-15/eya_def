"""Test validate schema on examples.

"""

from typing import Any

import jsonschema
import pydantic as pdt
import pytest

from eya_def_tools.data_models.eya_def import EyaDef


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
            # TODO
            # Several examples temporarily have dummy references, so we temporarily
            # accept that some references cannot be resolved
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
            # TODO
            # Several examples temporarily have dummy references, so we temporarily
            # accept that some references cannot be resolved
            pass


def test_validate_pydantic_model(json_example_dict: dict[str, Any]) -> None:
    """Test validate all json file examples against pydantic model."""
    for json_filename, json_example in json_example_dict.items():
        try:
            energy_yield_assessment = EyaDef(**json_example)
            assert isinstance(energy_yield_assessment, EyaDef)
        except pdt.ValidationError as exc:
            pytest.fail(
                f"the json example '{json_filename}' did not pass the "
                f"pydantic model json schema validation ({exc})"
            )


def test_validate_iea43_wra_data_model(
    measurement_station_a_json: dict[str, Any],
    iea43_wra_data_model_json_schema: dict[str, Any],
) -> None:
    jsonschema.validate(
        instance=measurement_station_a_json,
        schema=iea43_wra_data_model_json_schema,
    )
