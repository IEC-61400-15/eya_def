"""Test the ``eya_def_tools.data_model.enums`` module.

"""

import pytest

from eya_def_tools.data_models.enums import (
    PlantPerformanceCategoryLabel,
    PlantPerformanceComponentLabel,
)


@pytest.mark.parametrize(
    "plant_performance_category_label, expected",
    [
        (PlantPerformanceCategoryLabel.WAKES, True),
        (PlantPerformanceCategoryLabel.BLOCKAGE, True),
        (PlantPerformanceCategoryLabel.AVAILABILITY, False),
    ],
)
def test_plant_performance_category_label_returns_correct_is_turbine_interaction(
    plant_performance_category_label: PlantPerformanceCategoryLabel, expected: bool
) -> None:
    assert plant_performance_category_label.is_turbine_interaction() == expected


@pytest.mark.parametrize(
    "plant_performance_component_label, expected",
    [
        (
            PlantPerformanceComponentLabel.INTERNAL_WAKES,
            PlantPerformanceCategoryLabel.WAKES,
        ),
        (
            PlantPerformanceComponentLabel.EXTERNAL_BLOCKAGE,
            PlantPerformanceCategoryLabel.BLOCKAGE,
        ),
        (
            PlantPerformanceComponentLabel.TURBINE_AVAILABILITY,
            PlantPerformanceCategoryLabel.AVAILABILITY,
        ),
    ],
)
def test_plant_performance_component_label_returns_correct_category(
    plant_performance_component_label: PlantPerformanceComponentLabel,
    expected: PlantPerformanceCategoryLabel,
) -> None:
    assert plant_performance_component_label.category() == expected
