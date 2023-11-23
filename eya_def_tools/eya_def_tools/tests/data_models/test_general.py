"""Test the ``data_models.general`` module.

"""

import pytest

from eya_def_tools.data_models.general import MeasurementQuantity, MeasurementUnit


@pytest.mark.parametrize(
    "measurement_quantity, expected",
    [
        (
            MeasurementQuantity.WIND_SPEED,
            MeasurementUnit.METRE_PER_SECOND,
        ),
        (
            MeasurementQuantity.EFFICIENCY,
            MeasurementUnit.ONE,
        ),
        (
            MeasurementQuantity.RELATIVE_WIND_SPEED_UNCERTAINTY,
            MeasurementUnit.ONE,
        ),
    ],
)
def test_measurement_quantity_returns_correct_measurement_unit(
    measurement_quantity: MeasurementQuantity,
    expected: MeasurementUnit,
) -> None:
    assert measurement_quantity.measurement_unit == expected
