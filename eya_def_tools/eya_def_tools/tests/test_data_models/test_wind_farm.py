"""Test the ``wind_farm`` module."""

from collections.abc import Iterable

import numpy as np
import pytest

from eya_def_tools.data_models.wind_farm import WindFarmConfiguration


@pytest.mark.parametrize(
    argnames=("wind_farm_id", "expected_capacity"),
    argvalues=[
        (
            "bf_a",
            11.0,
        ),
        (
            "bf_b",
            11.5,
        ),
    ],
)
def test_capacity_property_calculates_correctly(
    wind_farm_a: WindFarmConfiguration,
    wind_farm_b: WindFarmConfiguration,
    wind_farm_id: str,
    expected_capacity: float,
) -> None:
    wind_farm = _get_wind_farm_by_id(
        wind_farms=(wind_farm_a, wind_farm_b), wind_farm_id=wind_farm_id
    )

    assert np.isclose(wind_farm.capacity, expected_capacity)


@pytest.mark.parametrize(
    argnames=("wind_farm_id", "expected_assessment_period_length"),
    argvalues=[
        (
            "bf_a",
            30.99879531,
        ),
        (
            "bf_b",
            34.99890483,
        ),
    ],
)
def test_assessment_period_length_property_calculates_correctly(
    wind_farm_a: WindFarmConfiguration,
    wind_farm_b: WindFarmConfiguration,
    wind_farm_id: str,
    expected_assessment_period_length: float,
) -> None:
    wind_farm = _get_wind_farm_by_id(
        wind_farms=(wind_farm_a, wind_farm_b), wind_farm_id=wind_farm_id
    )

    assert np.isclose(
        wind_farm.assessment_period_length,
        expected_assessment_period_length,
    )


def _get_wind_farm_by_id(
    wind_farms: Iterable[WindFarmConfiguration],
    wind_farm_id: str,
) -> WindFarmConfiguration:
    for wind_farm in wind_farms:
        if wind_farm.id == wind_farm_id:
            return wind_farm

    raise ValueError(
        "The wind farm ID used to reference test configuration objects does not match any of the expected values."
    )
