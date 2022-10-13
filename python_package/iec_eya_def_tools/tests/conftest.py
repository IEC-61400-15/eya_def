# -*- coding: utf-8 -*-
"""Setup and fixtures for the entire `iec_eya_def_tools` test module.

"""

import pytest
import json
from pathlib import Path


TEST_INPUT_DATA_DIRNAME = "test_input_data"
"""Directory name of test input data."""


@pytest.fixture(scope='session')
def test_input_data_dirpath():
    """Get the path of the directory where test input data is located.

    :return: the directory path of test input data
    """
    dirpath = Path(__file__).parent
    return dirpath / TEST_INPUT_DATA_DIRNAME


@pytest.fixture(scope='session')
def top_level_dirpath() -> Path:
    """Get the path of the top-level project directory.

    The top-level is the git repository, one level above the python
    package.

    :return: path to the project top-level directory
    """
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture(scope='session')
def master_json_schema_dirpath(top_level_dirpath) -> Path:
    """Get the path of the json schema directory.

    :param top_level_dirpath: path to the project top-level directory
    :return: directory path where the master json schema is located
    :raises ValueError: if the directory does not exist at the expected
        location
    """
    master_json_schema_dirpath = top_level_dirpath / "json_schema"
    if not master_json_schema_dirpath.is_dir():
        raise ValueError(
            f"the expected json schema directory "
            f"'{master_json_schema_dirpath}' does not exist")
    return master_json_schema_dirpath


@pytest.fixture(scope='session')
def master_json_schema_filepath(master_json_schema_dirpath) -> Path:
    """Get the path of the IEC 61400-15-2 Reporting DEF json schema.

    :param master_json_schema_dirpath: directory path where the master
        json schema is located
    :return: file path of the master json schema
    :raises ValueError: if the file does not exist at the expected
        location
    """
    filepath = (
        master_json_schema_dirpath
        / "iec_61400-15-2_reporting_def.schema.json")
    if not filepath.is_file():
        raise ValueError(
            f"the expected json schema file '{filepath}' does not exist")
    return filepath


@pytest.fixture(scope='session')
def master_json_schema(master_json_schema_filepath) -> dict:
    """Get `dict` representation of the master json schema.

    Note that this function returns a representation of the master
    IEC 61400-15-2 Reporting DEF json schema and not a json schema
    representation of the pydantic model.

    :param master_json_schema_filepath: file path of the master json
        schema
    :return: a `dict` representation of the master IEC 61400-15-2
        Reporting DEF json schema
    """
    with open(master_json_schema_filepath) as f:
        json_schema = json.load(f)
    return json_schema


@pytest.fixture(scope='session')
def pydantic_json_schema() -> dict:
    """Get a `dict` representation of the pydantic json schema.

    :return: a `dict` representation of the pydantic data model json
        schema exported from the `data_model.EnergyAssessmentReport`
        class
    """
    from iec_eya_def_tools.data_model import EnergyAssessmentReport
    return EnergyAssessmentReport.final_json_schema()


@pytest.fixture(scope='session')
def pydantic_json_schema_tmp_path(
        pydantic_json_schema, tmp_path_factory) -> Path:
    """Get the path to the temporary pydantic json schema file.

    :param pydantic_json_schema: a `dict` representation of the pydantic
        json schema exported from `data_model.EnergyAssessmentReport`
    :param tmp_path_factory: the `pytest` `tmp_path_factory`
    :return: the path to the temporary json schema file representation
        of the pydantic data model
    """
    tmp_dirpath = tmp_path_factory.mktemp("schema")
    filepath = tmp_dirpath / "iec_61400-15-2_reporting_def.schema.json"
    with open(filepath, 'w') as f:
        f.write(json.dumps(pydantic_json_schema, indent=2))
    return filepath


@pytest.fixture(scope='session')
def pydantic_json_schema_from_file(pydantic_json_schema_tmp_path) -> dict:
    """Get `dict` representation of the pydantic json schema from file.

    :param pydantic_json_schema_tmp_path: the path to the temporary json
        schema file representation of the pydantic data model
    :return: a `dict` representation of the pydantic data model json
        schema read back from the temporary file
    """
    with open(pydantic_json_schema_tmp_path) as f:
        json_schema = json.load(f)
    return json_schema


@pytest.fixture(scope='session')
def examples_tmp_dirpath(tmp_path_factory) -> Path:
    """Get a temporary directory path for json schema example files.

    :param tmp_path_factory: the `pytest` `tmp_path_factory`
    :return: a `Path` representation of the temporary json schema
        examples directory
    """
    return tmp_path_factory.mktemp("examples")
