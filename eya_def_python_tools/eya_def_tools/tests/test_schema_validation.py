# -*- coding: utf-8 -*-
"""Test the ``eya_def_tools.data_model`` module on example datasets.

"""

import pytest
import pydantic
import jsonschema


def test_validate_master_json_schema(master_json_schema, json_example_dict):
    """Test validate all json file examples against master schema."""
    for json_filename, json_example in json_example_dict.items():
        try:
            jsonschema.validate(
                instance=json_example, schema=master_json_schema)
        except jsonschema.exceptions.ValidationError as exc:
            pytest.fail(
                f"the json example '{json_filename}' did not pass the "
                f"master json schema validation ({exc})")
        except jsonschema.exceptions.RefResolutionError:
            # Several examples have dummy references, so we accept that
            # some references cannot be resolved
            pass


def test_validate_pydantic_model_json_schema(
        pydantic_json_schema, json_example_dict):
    """Test validate all json file examples against pydantic schema."""
    for json_filename, json_example in json_example_dict.items():
        try:
            jsonschema.validate(
                instance=json_example, schema=pydantic_json_schema)
        except jsonschema.exceptions.ValidationError as exc:
            pytest.fail(
                f"the json example '{json_filename}' did not pass the "
                f"pydantic model json schema validation ({exc})")
        except jsonschema.exceptions.RefResolutionError:
            # Several examples have dummy references, so we accept that
            # some references cannot be resolved
            pass


def test_validate_pydantic_model(json_example_dict):
    """Test validate all json file examples against pydantic model."""
    from eya_def_tools.data_model import EnergyYieldAssessment
    for json_filename, json_example in json_example_dict.items():
        try:
            energy_yield_assessment = EnergyYieldAssessment(**json_example)
            assert isinstance(energy_yield_assessment, EnergyYieldAssessment)
        except pydantic.ValidationError as exc:
            pytest.fail(
                f"the json example '{json_filename}' did not pass the "
                f"pydantic model json schema validation ({exc})")
