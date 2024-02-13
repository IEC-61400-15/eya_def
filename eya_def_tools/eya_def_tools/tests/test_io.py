"""Tests for the ``io`` module.

"""

from pathlib import Path

import pytest

from eya_def_tools.data_models.eya_def import EyaDefDocument
from eya_def_tools.io import parser, writer


@pytest.mark.parametrize(
    "filename", ["eya_def_a.json", "eya_def_a.yaml"], ids=["JSON", "YAML"]
)
def test_file_write_parse_round_trip_json(
    eya_def_a: EyaDefDocument,
    tmp_path_factory: pytest.TempPathFactory,
    filename: str,
) -> None:
    filepath = tmp_path_factory.mktemp("io") / filename
    writer.write_file(model=eya_def_a, filepath=filepath)
    eya_def_a_round_trip = parser.parse_file(filepath=filepath)
    assert eya_def_a_round_trip == eya_def_a


def test_parse_invalid_file_type_raises_error() -> None:
    with pytest.raises(
        expected_exception=ValueError,
        match="does not support reading from the file format.*xml",
    ):
        _ = parser.parse_file(filepath=Path("eya_def_document.xml"))


def test_write_invalid_file_type_raises_error(eya_def_a: EyaDefDocument) -> None:
    with pytest.raises(
        expected_exception=ValueError,
        match="does not support output to the file format.*xml",
    ):
        writer.write_file(model=eya_def_a, filepath=Path("eya_def_document.xml"))
