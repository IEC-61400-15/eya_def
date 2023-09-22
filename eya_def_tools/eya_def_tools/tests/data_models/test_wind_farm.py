"""Test the ``wind_farm`` module.

"""

import pytest

from eya_def_tools.data_models.wind_farm import WindFarmConfiguration


@pytest.mark.parametrize(
    "wind_farm_id, expected",
    [
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
    expected: float,
) -> None:
    wind_farm: WindFarmConfiguration
    if wind_farm_id == wind_farm_a.id:
        wind_farm = wind_farm_a
    elif wind_farm_id == wind_farm_b.id:
        wind_farm = wind_farm_b
    else:
        raise ValueError(
            "The wind farm ID used to reference test configuration objects "
            "does not match any of the expected values."
        )

    assert wind_farm.capacity == expected
