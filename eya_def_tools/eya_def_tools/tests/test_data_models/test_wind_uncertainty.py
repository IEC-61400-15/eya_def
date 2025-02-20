"""Test the ``data_models.wind_uncertainty`` module."""

import pytest

from eya_def_tools.data_models.wind_uncertainty import (
    WindUncertaintyCategoryLabel,
    WindUncertaintyResults,
    WindUncertaintySubcategoryLabel,
)


def test_invalid_empty_wind_uncertainty_results_raises_error() -> None:
    with pytest.raises(
        expected_exception=ValueError,
        match="wind uncertainty assessment results.*without any results.*not valid",
    ):
        _ = WindUncertaintyResults()


@pytest.mark.parametrize(
    argnames=("wind_uncertainty_subcategory_label", "expected_category"),
    argvalues=[
        (
            WindUncertaintySubcategoryLabel.WIND_SPEED_MEASUREMENT,
            WindUncertaintyCategoryLabel.MEASUREMENT,
        ),
        (
            WindUncertaintySubcategoryLabel.WIND_DIRECTION_MEASUREMENT,
            WindUncertaintyCategoryLabel.MEASUREMENT,
        ),
        (
            WindUncertaintySubcategoryLabel.OTHER_ATMOSPHERIC_PARAMETERS,
            WindUncertaintyCategoryLabel.MEASUREMENT,
        ),
        (
            WindUncertaintySubcategoryLabel.DATA_INTEGRITY,
            WindUncertaintyCategoryLabel.MEASUREMENT,
        ),
        (
            WindUncertaintySubcategoryLabel.LONG_TERM_PERIOD_REPRESENTATIVENESS,
            WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE,
        ),
        (
            WindUncertaintySubcategoryLabel.REFERENCE_DATA_CONSISTENCY,
            WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE,
        ),
        (
            WindUncertaintySubcategoryLabel.LONG_TERM_ADJUSTMENT,
            WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE,
        ),
        (
            WindUncertaintySubcategoryLabel.WIND_SPEED_DISTRIBUTION_UNCERTAINTY,
            WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE,
        ),
        (
            WindUncertaintySubcategoryLabel.ON_SITE_DATA_SYNTHESIS,
            WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE,
        ),
        (
            WindUncertaintySubcategoryLabel.MEASURED_DATA_REPRESENTATIVENESS,
            WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE,
        ),
        (
            WindUncertaintySubcategoryLabel.HORIZONTAL_MODEL_INPUTS,
            WindUncertaintyCategoryLabel.HORIZONTAL_EXTRAPOLATION,
        ),
        (
            WindUncertaintySubcategoryLabel.HORIZONTAL_MODEL_SENSITIVITY,
            WindUncertaintyCategoryLabel.HORIZONTAL_EXTRAPOLATION,
        ),
        (
            WindUncertaintySubcategoryLabel.HORIZONTAL_MODEL_APPROPRIATENESS,
            WindUncertaintyCategoryLabel.HORIZONTAL_EXTRAPOLATION,
        ),
        (
            WindUncertaintySubcategoryLabel.VERTICAL_MODEL_UNCERTAINTY,
            WindUncertaintyCategoryLabel.VERTICAL_EXTRAPOLATION,
        ),
        (
            WindUncertaintySubcategoryLabel.EXCESS_PROPAGATED_UNCERTAINTY,
            WindUncertaintyCategoryLabel.VERTICAL_EXTRAPOLATION,
        ),
        (
            WindUncertaintySubcategoryLabel.WIND_SPEED_VARIABILITY,
            WindUncertaintyCategoryLabel.FUTURE_ASSESSMENT_PERIOD_VARIABILITY,
        ),
        (
            WindUncertaintySubcategoryLabel.CLIMATE_CHANGE,
            WindUncertaintyCategoryLabel.FUTURE_ASSESSMENT_PERIOD_VARIABILITY,
        ),
        (
            WindUncertaintySubcategoryLabel.OTHER,
            WindUncertaintyCategoryLabel.OTHER,
        ),
    ],
)
def test_wind_uncertainty_subcategory_label_returns_correct_category_label(
    wind_uncertainty_subcategory_label: WindUncertaintySubcategoryLabel,
    expected_category: WindUncertaintyCategoryLabel,
) -> None:
    assert wind_uncertainty_subcategory_label.category == expected_category
