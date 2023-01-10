"""Test ``eya_def_tools`` module and submodule imports.

"""

import importlib
import sys


def test_package_module_found():
    """Test ``eya_def_tools`` module is found."""
    import importlib

    assert importlib.util.find_spec("eya_def_tools") is not None


def test_import_package_module():
    """Test ``eya_def_tools`` is successfully imported."""
    import eya_def_tools

    assert eya_def_tools is not None
    assert "eya_def_tools" in sys.modules


def test_data_model_module_found():
    """Test ``eya_def_tools.data_model.energy_yield_assessment`` is found."""
    assert (
        importlib.util.find_spec("eya_def_tools.data_models.energy_yield_assessment")
        is not None
    )


def test_import_data_model_module():
    """Test ``eya_def_tools.data_model.energy_yield_assessment`` is imported."""
    import sys

    import eya_def_tools.data_models.energy_yield_assessment

    assert eya_def_tools.data_models.energy_yield_assessment is not None
    assert "eya_def_tools.data_models.energy_yield_assessment" in sys.modules
