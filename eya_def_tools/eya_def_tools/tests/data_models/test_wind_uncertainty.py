"""Test the ``data_models.wind_uncertainty`` module.

"""

import pytest

from eya_def_tools.data_models.wind_uncertainty import (
    WindUncertaintyCategoryLabel,
    WindUncertaintySubcategoryLabel,
)


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
