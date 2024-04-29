"""Test the ``data_models.plant_performance`` module.

"""

import pytest

from eya_def_tools.data_models.plant_performance import (
    PlantPerformanceCategoryLabel,
    PlantPerformanceSubcategoryLabel,
)


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
