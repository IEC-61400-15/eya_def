# -*- coding: utf-8 -*-
"""Test the `iec_eya_def_tools.data_model` module on example datasets.

"""
import pytest
import pydantic
import json
import jsonschema
from pathlib import Path


@pytest.fixture(scope='session')
def json_examples_dirpath(top_level_dirpath) -> Path:
    """Get the path of the json examples directory.

    :param top_level_dirpath: path to the project top-level directory
    :return: directory path where the json examples are located
    :raises ValueError: if the directory does not exist at the expected
        location
    """
    json_examples_dirpath = top_level_dirpath / "json_schema" / "examples"
    if not json_examples_dirpath.is_dir():
        raise ValueError(
            f"the expected json examples directory "
            f"'{json_examples_dirpath}' does not exist")
    return json_examples_dirpath


@pytest.fixture(scope='session')
def json_example_filepaths(json_examples_dirpath) -> list[Path]:
    """Get the paths of the IEC 61400-15-2 Reporting DEF json examples.

    :param json_examples_dirpath: directory path where the json examples
        are located
    :return: file paths of the json examples
    :raises ValueError: if no example json files exist at the expected
        location
    """
    filename_pattern = "iec_61400-15-2_reporting_def_example*.json"
    json_example_filepaths = list(json_examples_dirpath.glob(filename_pattern))
    if len(json_example_filepaths) < 1:
        raise ValueError(
            f"no example json files with the expected filename pattern "
            f"exist in the directory '{json_examples_dirpath}'")
    return json_example_filepaths


@pytest.fixture(scope='session')
def json_example_dict(json_example_filepaths) -> dict[str, dict]:
    """Get `dict` of the IEC 61400-15-2 Reporting DEF json examples.

    :param json_example_filepaths: list of paths to the json example
        files
    :return: a `dict` of the form {<filename>: <example_dict>}
    """
    json_example_dict = {}
    for json_example_filepath in json_example_filepaths:
        with open(json_example_filepath) as f:
            json_example_dict[f.name] = json.load(f)
    return json_example_dict


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
        except jsonschema.exceptions.RefResolutionError as exc:
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
        except jsonschema.exceptions.RefResolutionError as exc:
            # Several examples have dummy references, so we accept that
            # some references cannot be resolved
            pass


def test_validate_pydantic_model(json_example_dict):
    """Test validate all json file examples against pydantic model."""
    from iec_eya_def_tools.data_model import EnergyAssessmentReport
    for json_filename, json_example in json_example_dict.items():
        try:
            energy_assessment_report = EnergyAssessmentReport(**json_example)
            assert isinstance(energy_assessment_report, EnergyAssessmentReport)
        except pydantic.ValidationError as exc:
            pytest.fail(
                f"the json example '{json_filename}' did not pass the "
                f"pydantic model json schema validation ({exc})")
