"""Test the ``data_models.general`` module."""

import pytest

from eya_def_tools.data_models.general import MeasurementQuantity, MeasurementUnit


@pytest.mark.parametrize(
    argnames=("measurement_quantity", "expected"),
    argvalues=[
        (
            MeasurementQuantity.AIR_DENSITY,
            MeasurementUnit.KILOGRAM_PER_CUBIC_METRE,
        ),
        (
            MeasurementQuantity.AMBIENT_TURBULENCE_INTENSITY,
            MeasurementUnit.ONE,
        ),
        (
            MeasurementQuantity.ANNUAL_ENERGY_PRODUCTION,
            MeasurementUnit.GIGAWATT_HOUR_PER_ANNUM,
        ),
        (
            MeasurementQuantity.CAPACITY_FACTOR,
            MeasurementUnit.ONE,
        ),
        (
            MeasurementQuantity.DATA_AVAILABILITY,
            MeasurementUnit.ONE,
        ),
        (MeasurementQuantity.DISPLACEMENT_HEIGHT, MeasurementUnit.METRE),
        (MeasurementQuantity.DISTANCE, MeasurementUnit.METRE),
        (
            MeasurementQuantity.EFFICIENCY,
            MeasurementUnit.ONE,
        ),
        (MeasurementQuantity.ENERGY, MeasurementUnit.GIGAWATT_HOUR),
        (MeasurementQuantity.ENERGY_PRODUCTION, MeasurementUnit.GIGAWATT_HOUR),
        (
            MeasurementQuantity.POWER,
            MeasurementUnit.WATT,
        ),
        (
            MeasurementQuantity.PROBABILITY,
            MeasurementUnit.ONE,
        ),
        (
            MeasurementQuantity.RELATIVE_ENERGY_UNCERTAINTY,
            MeasurementUnit.ONE,
        ),
        (
            MeasurementQuantity.RELATIVE_WIND_SPEED_UNCERTAINTY,
            MeasurementUnit.ONE,
        ),
        (
            MeasurementQuantity.ROTOR_SPEED,
            MeasurementUnit.RPM,
        ),
        (
            MeasurementQuantity.WIND_SHEAR_EXPONENT,
            MeasurementUnit.ONE,
        ),
        (
            MeasurementQuantity.TEMPERATURE,
            MeasurementUnit.DEGREE_CELSIUS,
        ),
        (
            MeasurementQuantity.TIME,
            MeasurementUnit.HOUR,
        ),
        (
            MeasurementQuantity.WIND_FROM_DIRECTION,
            MeasurementUnit.DEGREE,
        ),
        (
            MeasurementQuantity.WIND_SPEED,
            MeasurementUnit.METRE_PER_SECOND,
        ),
    ],
)
def test_measurement_quantity_returns_correct_measurement_unit(
    measurement_quantity: MeasurementQuantity,
    expected: MeasurementUnit,
) -> None:
    assert measurement_quantity.measurement_unit == expected
