"""Test validate schema on examples.

"""
import copy
import json
from pathlib import Path
from typing import Any

import jsonschema
import pydantic as pdt
import pytest

from eya_def_tools.data_models.eya_def import EyaDefDocument


def test_validate_master_json_schema(
    master_json_schema: dict[str, Any],
    json_example_dict: dict[str, Any],
    json_examples_dirpath: Path,
) -> None:
    """Test validate all json file examples against master schema."""
    json_schema = master_json_schema.copy()

    # Remove ``$id`` field from schema to avoid resolving from URL
    if "$id" in json_schema.keys():
        del json_schema["$id"]

    for json_filename, json_example in json_example_dict.items():
        json_example_processed = _get_reduced_json_example(json_example=json_example)
        json_example_processed = _resolve_measurement_stations_references(
            json_example=json_example_processed,
            json_examples_dirpath=json_examples_dirpath,
        )

        try:
            jsonschema.validate(instance=json_example_processed, schema=json_schema)
        except jsonschema.exceptions.ValidationError as exc:
            pytest.fail(
                f"the json example '{json_filename}' did not pass the "
                f"master json schema validation ({exc})"
            )
        except jsonschema.exceptions.RefResolutionError:
            # TODO
            # Several examples temporarily have dummy references, so we temporarily
            # accept that some references cannot be resolved
            pass


def test_validate_pydantic_model_json_schema(
    pydantic_json_schema: dict[str, Any],
    json_example_dict: dict[str, Any],
    json_examples_dirpath: Path,
) -> None:
    """Test validate all json file examples against pydantic schema."""
    json_schema = pydantic_json_schema.copy()

    # Remove ``$id`` field from schema to avoid resolving from URL
    if "$id" in json_schema.keys():
        del json_schema["$id"]

    for json_filename, json_example in json_example_dict.items():
        json_example_processed = _get_reduced_json_example(json_example=json_example)
        json_example_processed = _resolve_measurement_stations_references(
            json_example=json_example_processed,
            json_examples_dirpath=json_examples_dirpath,
        )

        try:
            jsonschema.validate(instance=json_example_processed, schema=json_schema)
        except jsonschema.exceptions.ValidationError as exc:
            pytest.fail(
                f"the json example '{json_filename}' did not pass the "
                f"pydantic model json schema validation ({exc})"
            )
        except jsonschema.exceptions.RefResolutionError:
            # TODO
            # Several examples temporarily have dummy references, so we temporarily
            # accept that some references cannot be resolved
            pass


def test_validate_pydantic_model(json_example_dict: dict[str, Any]) -> None:
    """Test validate all json file examples against pydantic model."""
    for json_filename, json_example in json_example_dict.items():
        try:
            print(json_example["measurement_stations"])
            energy_yield_assessment = EyaDefDocument(**json_example)
            assert isinstance(energy_yield_assessment, EyaDefDocument)
        except pdt.ValidationError as exc:
            pytest.fail(
                f"the json example '{json_filename}' did not pass the "
                f"pydantic model validation ({exc})"
            )


def test_validate_iea43_wra_data_model(
    measurement_station_a_json: dict[str, Any],
    iea43_wra_data_model_json_schema: dict[str, Any],
) -> None:
    jsonschema.validate(
        instance=measurement_station_a_json,
        schema=iea43_wra_data_model_json_schema,
    )


def _get_reduced_json_example(json_example: dict[str, Any]) -> dict[str, Any]:
    """Remove ``$id`` and `$schema``` fields from a JSON example.

    This is to avoid attempting to use these fields when resolving URLs,
    as the tests should use the local copies
    """
    json_example_reduced = copy.deepcopy(json_example)

    if "$id" in json_example_reduced.keys():
        del json_example_reduced["$id"]
    if "$schema" in json_example_reduced.keys():
        del json_example_reduced["$schema"]

    return json_example_reduced


def _resolve_measurement_stations_references(
    json_example: dict[str, Any],
    json_examples_dirpath: Path,
) -> dict[str, Any]:
    json_example_resolved = copy.deepcopy(json_example)

    for i, _ in enumerate(json_example["measurement_stations"]):
        if (
            isinstance(json_example["measurement_stations"][i], dict)
            and "$ref" in json_example["measurement_stations"][i].keys()
        ):
            measurement_station_json_filepath = (
                json_examples_dirpath / json_example["measurement_stations"][i]["$ref"]
            )

            with open(measurement_station_json_filepath) as f:
                measurement_station_json = json.load(f)

            json_example_resolved["measurement_stations"][i] = measurement_station_json

    return json_example_resolved
