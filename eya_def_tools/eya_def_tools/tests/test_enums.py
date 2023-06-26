"""Test the ``enums`` module.

"""

import pytest

from eya_def_tools.data_models.enums import (
    MeasurementQuantity,
    MeasurementUnit,
    PlantPerformanceCategoryLabel,
    PlantPerformanceSubcategoryLabel,
    WindUncertaintyCategoryLabel,
    WindUncertaintySubcategoryLabel,
)


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
            MeasurementQuantity.RELATIVE_UNCERTAINTY,
            MeasurementUnit.ONE,
        ),
    ],
)
def test_measurement_quantity_returns_correct_measurement_unit(
    measurement_quantity: MeasurementQuantity,
    expected: MeasurementUnit,
) -> None:
    assert measurement_quantity.measurement_unit == expected


@pytest.mark.parametrize(
    "plant_performance_component_label, expected",
    [
        (
            PlantPerformanceSubcategoryLabel.INTERNAL_TURBINE_INTERACTION,
            PlantPerformanceCategoryLabel.TURBINE_INTERACTION,
        ),
        (
            PlantPerformanceSubcategoryLabel.EXTERNAL_TURBINE_INTERACTION,
            PlantPerformanceCategoryLabel.TURBINE_INTERACTION,
        ),
        (
            PlantPerformanceSubcategoryLabel.TURBINE_AVAILABILITY,
            PlantPerformanceCategoryLabel.AVAILABILITY,
        ),
    ],
)
def test_plant_performance_subcategory_label_returns_correct_category_label(
    plant_performance_component_label: PlantPerformanceSubcategoryLabel,
    expected: PlantPerformanceCategoryLabel,
) -> None:
    assert plant_performance_component_label.category == expected


@pytest.mark.parametrize(
    "wind_uncertainty_subcategory_label, expected",
    [
        (
            WindUncertaintySubcategoryLabel.LONG_TERM_PERIOD_REPRESENTATIVENESS,
            WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE,
        ),
        (
            WindUncertaintySubcategoryLabel.LONG_TERM_ADJUSTMENT,
            WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE,
        ),
        (
            WindUncertaintySubcategoryLabel.WIND_SPEED_MEASUREMENT,
            WindUncertaintyCategoryLabel.MEASUREMENT_UNCERTAINTY,
        ),
    ],
)
def test_wind_uncertainty_subcategory_label_returns_correct_category_label(
    wind_uncertainty_subcategory_label: WindUncertaintySubcategoryLabel,
    expected: WindUncertaintyCategoryLabel,
) -> None:
    assert wind_uncertainty_subcategory_label.category == expected
