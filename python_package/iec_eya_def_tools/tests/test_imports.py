# -*- coding: utf-8 -*-
"""Test `iec_eya_def_tools` module and submodule imports.

"""


def test_package_module_found():
    """Test `iec_eya_def_tools` module is found."""
    import importlib
    assert importlib.util.find_spec('iec_eya_def_tools') is not None


def test_import_package_module():
    """Test `iec_eya_def_tools` is successfully imported."""
    import sys
    import iec_eya_def_tools
    assert iec_eya_def_tools is not None
    assert 'iec_eya_def_tools' in sys.modules


def test_data_model_module_found():
    """Test `iec_eya_def_tools.data_model` module is found."""
    import importlib
    assert importlib.util.find_spec('iec_eya_def_tools.data_model') is not None


def test_import_data_model_module():
    """Test `iec_eya_def_tools.data_model` is successfully imported."""
    import sys
    import iec_eya_def_tools.data_model
    assert iec_eya_def_tools.data_model is not None
    assert 'iec_eya_def_tools.data_model' in sys.modules
