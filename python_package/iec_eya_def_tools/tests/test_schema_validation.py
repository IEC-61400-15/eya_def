# -*- coding: utf-8 -*-
"""Test the `iec_eya_def_tools.data_model` module on example datasets.

"""

import pytest
import json
import jsonschema
from pathlib import Path

from iec_eya_def_tools.data_model import export_json_schema


@pytest.fixture(scope='session')
def top_level_dirpath() -> Path:
    """Get the path of the top-level project directory.

    The top-level is the git repository, one level above the python
    package.

    :return: path to the project top-level directory
    """
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture(scope='session')
def json_schema_dirpath(top_level_dirpath) -> Path:
    """Get the path of the json schema directory.

    :param top_level_dirpath: path to the project top-level directory
    :return: directory path where the json schema is located
    :raises ValueError: if the directory does not exist at the expected
        location
    """
    json_schema_dirpath = top_level_dirpath / "json_schema"
    if not json_schema_dirpath.is_dir():
        raise ValueError(
            f"the expected json schema directory "
            f"'{json_schema_dirpath}' does not exist")
    return json_schema_dirpath


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
def json_schema_filepath(json_schema_dirpath) -> Path:
    """Get the path of the IEC 61400-15-2 Reporting DEF json schema.

    :param json_schema_dirpath: directory path where the json schema is
        located
    :return: file path of the json schema
    :raises ValueError: if the file does not exist at the expected
        location
    """
    filepath = (
        json_schema_dirpath
        / "iec_61400-15-2_reporting_def.schema.json")
    if not filepath.is_file():
        raise ValueError(
            f"the expected json schema file '{filepath}' does not exist")
    return filepath


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


def test_validate_master_schema(json_schema_filepath, json_example_filepaths):
    with open(json_schema_filepath) as f:
        json_schema = json.load(f)
    json_example_dict = {}
    for json_example_filepath in json_example_filepaths:
        with open(json_example_filepath) as f:
            json_example_dict[f.name] = json.load(f)
    for json_filename, json_example in json_example_dict.items():
        try:
            jsonschema.validate(instance=json_example, schema=json_schema)
        except jsonschema.exceptions.ValidationError as exc:
            pytest.fail(
                f"the json example '{json_filename}' did not pass the "
                f"json schema validation ({exc})")
