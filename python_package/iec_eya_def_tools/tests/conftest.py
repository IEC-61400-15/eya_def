# -*- coding: utf-8 -*-
"""Setup and fixtures for the entire `iec_eya_def_tools` test module.

"""

import pytest
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
