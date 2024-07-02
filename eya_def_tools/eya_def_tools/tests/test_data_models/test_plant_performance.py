import pytest

from eya_def_tools.data_models.plant_performance import (
    PlantPerformanceCategoryLabel,
    PlantPerformanceSubcategoryLabel,
)


@pytest.mark.parametrize(
    argnames=("plant_performance_component_label", "expected_category"),
    argvalues=[
        (
            PlantPerformanceSubcategoryLabel.INTERNAL_TURBINE_INTERACTION,
            PlantPerformanceCategoryLabel.TURBINE_INTERACTION,
        ),
        (
            PlantPerformanceSubcategoryLabel.EXTERNAL_TURBINE_INTERACTION,
            PlantPerformanceCategoryLabel.TURBINE_INTERACTION,
        ),
        (
            PlantPerformanceSubcategoryLabel.FUTURE_TURBINE_INTERACTION,
            PlantPerformanceCategoryLabel.TURBINE_INTERACTION,
        ),
        (
            PlantPerformanceSubcategoryLabel.TURBINE_AVAILABILITY,
            PlantPerformanceCategoryLabel.AVAILABILITY,
        ),
        (
            PlantPerformanceSubcategoryLabel.BOP_AVAILABILITY,
            PlantPerformanceCategoryLabel.AVAILABILITY,
        ),
        (
            PlantPerformanceSubcategoryLabel.GRID_AVAILABILITY,
            PlantPerformanceCategoryLabel.AVAILABILITY,
        ),
        (
            PlantPerformanceSubcategoryLabel.ELECTRICAL_EFFICIENCY,
            PlantPerformanceCategoryLabel.ELECTRICAL,
        ),
        (
            PlantPerformanceSubcategoryLabel.FACILITY_PARASITIC_CONSUMPTION,
            PlantPerformanceCategoryLabel.ELECTRICAL,
        ),
        (
            PlantPerformanceSubcategoryLabel.SUB_OPTIMAL_PERFORMANCE,
            PlantPerformanceCategoryLabel.TURBINE_PERFORMANCE,
        ),
        (
            PlantPerformanceSubcategoryLabel.GENERIC_POWER_CURVE_ADJUSTMENT,
            PlantPerformanceCategoryLabel.TURBINE_PERFORMANCE,
        ),
        (
            PlantPerformanceSubcategoryLabel.SITE_SPECIFIC_POWER_CURVE_ADJUSTMENT,
            PlantPerformanceCategoryLabel.TURBINE_PERFORMANCE,
        ),
        (
            PlantPerformanceSubcategoryLabel.HIGH_WIND_HYSTERESIS,
            PlantPerformanceCategoryLabel.TURBINE_PERFORMANCE,
        ),
        (
            PlantPerformanceSubcategoryLabel.ICING,
            PlantPerformanceCategoryLabel.ENVIRONMENTAL,
        ),
        (
            PlantPerformanceSubcategoryLabel.DEGRADATION,
            PlantPerformanceCategoryLabel.ENVIRONMENTAL,
        ),
        (
            PlantPerformanceSubcategoryLabel.EXTERNAL_CONDITIONS,
            PlantPerformanceCategoryLabel.ENVIRONMENTAL,
        ),
        (
            PlantPerformanceSubcategoryLabel.EXPOSURE_CHANGES,
            PlantPerformanceCategoryLabel.ENVIRONMENTAL,
        ),
        (
            PlantPerformanceSubcategoryLabel.LOAD_CURTAILMENT,
            PlantPerformanceCategoryLabel.CURTAILMENT,
        ),
        (
            PlantPerformanceSubcategoryLabel.GRID_CURTAILMENT,
            PlantPerformanceCategoryLabel.CURTAILMENT,
        ),
        (
            PlantPerformanceSubcategoryLabel.ENVIRONMENTAL_CURTAILMENT,
            PlantPerformanceCategoryLabel.CURTAILMENT,
        ),
        (
            PlantPerformanceSubcategoryLabel.OPERATIONAL_STRATEGIES,
            PlantPerformanceCategoryLabel.CURTAILMENT,
        ),
        (
            PlantPerformanceSubcategoryLabel.ASYMMETRIC_EFFECTS,
            PlantPerformanceCategoryLabel.OTHER,
        ),
        (
            PlantPerformanceSubcategoryLabel.UPSIDE_SCENARIOS,
            PlantPerformanceCategoryLabel.OTHER,
        ),
        (
            PlantPerformanceSubcategoryLabel.OTHER,
            PlantPerformanceCategoryLabel.OTHER,
        ),
    ],
)
def test_plant_performance_subcategory_label_returns_correct_category_label(
    plant_performance_component_label: PlantPerformanceSubcategoryLabel,
    expected_category: PlantPerformanceCategoryLabel,
) -> None:
    assert plant_performance_component_label.category == expected_category
