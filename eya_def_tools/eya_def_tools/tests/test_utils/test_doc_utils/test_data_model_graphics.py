"""Test the ``data_model_graphics`` module.

"""

import os
from pathlib import Path

import pytest


@pytest.mark.erdantic
def test_data_model_graphics_main_completes_successfully(tmp_path: Path) -> None:
    from eya_def_tools.utils.doc_utils import data_model_graphics

    os.chdir(tmp_path)
    data_model_graphics.main()

    svg_filenames = [file.name for file in tmp_path.glob("*.svg")]
    png_filenames = [file.name for file in tmp_path.glob("*.png")]

    assert "eya_def_document_top_level.svg" in svg_filenames
    assert "eya_def_document_top_level.png" in png_filenames

    assert "scenario_reduced.svg" in svg_filenames
    assert "scenario_reduced.png" in png_filenames

    for filename in [
        data_model_graphics.get_filename_for_model_class(model_class=model_class)
        for model_class in data_model_graphics.MODEL_CLASSES_TO_DRAW
    ]:
        assert f"{filename}.svg" in svg_filenames
        assert f"{filename}.png" in png_filenames
