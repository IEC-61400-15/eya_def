"""Test validate schema on examples."""

import copy
from typing import Any

import jsonschema
import jsonschema.exceptions as jsonschema_exceptions
import pydantic as pdt
import pytest

from eya_def_tools.data_models.eya_def import EyaDefDocument


def test_validate_master_json_schema(
    master_json_schema: dict[str, Any],
    json_example_dict: dict[str, Any],
) -> None:
    """Test validate all json file examples against master schema."""
    json_schema = _clear_json_schema_id(json_schema=master_json_schema)

    for json_filename, json_example in json_example_dict.items():
        processed_json_example = _clear_reference_to_schema(json_example=json_example)

        try:
            jsonschema.validate(instance=processed_json_example, schema=json_schema)
        except jsonschema_exceptions.ValidationError as exc:
            pytest.fail(
                f"The json example '{json_filename}' did not pass the "
                f"master json schema validation ({exc})."
            )


def test_validate_pydantic_model_json_schema(
    pydantic_json_schema: dict[str, Any],
    json_example_dict: dict[str, Any],
) -> None:
    """Test validate all json file examples against pydantic schema."""
    json_schema = _clear_json_schema_id(json_schema=pydantic_json_schema)

    for json_filename, json_example in json_example_dict.items():
        processed_json_example = _clear_reference_to_schema(json_example=json_example)

        try:
            jsonschema.validate(instance=processed_json_example, schema=json_schema)
        except jsonschema_exceptions.ValidationError as exc:
            pytest.fail(
                f"The json example '{json_filename}' did not pass the "
                f"pydantic model json schema validation ({exc})."
            )


def test_validate_pydantic_model(json_example_dict: dict[str, Any]) -> None:
    """Test validate all json file examples against pydantic model."""
    for json_filename, json_example in json_example_dict.items():
        try:
            print(json_example["measurement_stations"])
            energy_yield_assessment = EyaDefDocument(**json_example)
            assert isinstance(energy_yield_assessment, EyaDefDocument)
        except pdt.ValidationError as exc:
            pytest.fail(
                f"The json example '{json_filename}' did not pass the "
                f"pydantic model validation ({exc})."
            )


def test_json_schema_validate_measurement_station_a(
    measurement_station_a: dict[str, Any],
    iea43_wra_data_model_json_schema: dict[str, Any],
) -> None:
    jsonschema.validate(
        instance=measurement_station_a,
        schema=iea43_wra_data_model_json_schema,
    )


def test_json_schema_validate_reference_meteorological_dataset_a(
    reference_meteorological_dataset_a: dict[str, Any],
    iea43_wra_data_model_json_schema: dict[str, Any],
) -> None:
    jsonschema.validate(
        instance=reference_meteorological_dataset_a,
        schema=iea43_wra_data_model_json_schema,
    )


@pytest.mark.parametrize(
    argnames="model_name",
    argvalues=["ABC165-5.5MW", "PQR169-5.8MW", "XYZ-3.2_140"],
)
def test_json_schema_validate_power_curve_documents(
    model_name: str,
    power_curve_document_map: dict[str, dict[str, Any]],
    iec61400_16_power_curve_schema_json_schema: dict[str, Any],
) -> None:
    jsonschema.validate(
        instance=power_curve_document_map[model_name],
        schema=iec61400_16_power_curve_schema_json_schema,
    )


def _clear_json_schema_id(json_schema: dict[str, Any]) -> dict[str, Any]:
    """Remove the ``$id`` field from a schema to avoid resolving URI."""
    if "$id" not in json_schema:
        return json_schema

    updated_json_schema = copy.deepcopy(json_schema)
    del updated_json_schema["$id"]

    return updated_json_schema


def _clear_reference_to_schema(json_example: dict[str, Any]) -> dict[str, Any]:
    """Remove the ``$schema`` field from a JSON example.

    The removal of the ``$schema`` field is to avoid attempting to
    resolve the URI instead of validating against the local copy of the
    schema.
    """
    if "$schema" not in json_example:
        return json_example

    json_example_reduced = copy.deepcopy(json_example)
    del json_example_reduced["$schema"]

    return json_example_reduced
