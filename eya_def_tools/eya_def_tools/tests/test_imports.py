"""Test module imports."""

import importlib.util as importlib_util
import sys


def test_package_module_found() -> None:
    """Test ``eya_def_tools`` module is found."""
    assert importlib_util.find_spec("eya_def_tools") is not None


def test_import_package_module() -> None:
    """Test ``eya_def_tools`` is successfully imported."""
    import eya_def_tools

    assert eya_def_tools is not None
    assert "eya_def_tools" in sys.modules
