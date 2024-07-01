"""Data models relating to wind resource and gross energy uncertainty.

"""

from __future__ import annotations

from enum import StrEnum, auto
from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.dataset import Dataset


class UncertaintyResults(EyaDefBaseModel):
    """Gross energy uncertainty assessment results."""

    relative_wind_speed_uncertainty: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Uncertainty assessment results as dimensionless relative "
            "values expressed in terms of wind speed and calculated as "
            "the standard deviation of the wind speed uncertainty "
            "distribution divided by the mean wind speed."
        ),
    )
    relative_energy_uncertainty: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Uncertainty assessment results as dimensionless relative "
            "values expressed in terms of AEP (annual energy production) and "
            "calculated as the standard deviation of the energy uncertainty "
            "distribution divided by the net P50 (50% probability of "
            "exceedance level) AEP."
        ),
    )


class WindUncertaintySubcategoryElement(EyaDefBaseModel):
    """Subcategory element of a wind related uncertainty assessment."""

    label: str = pdt.Field(
        default=...,
        min_length=1,
        description="Label of the wind related uncertainty subcategory element.",
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the wind related uncertainty "
            "subcategory element, which should not be empty if the "
            "field is included."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the wind related uncertainty "
            "subcategory element, which should not be empty if the "
            "field is included."
        ),
    )
    results: UncertaintyResults = pdt.Field(
        default=...,
        description=(
            "Wind related uncertainty assessment subcategory element results."
        ),
    )


class WindUncertaintySubcategoryLabel(StrEnum):
    """Subcategory labels in the wind uncertainty assessment."""

    # Historical wind resource
    LONG_TERM_PERIOD_REPRESENTATIVENESS = auto()
    REFERENCE_DATA_CONSISTENCY = auto()
    LONG_TERM_ADJUSTMENT = auto()
    WIND_SPEED_DISTRIBUTION_UNCERTAINTY = auto()
    ON_SITE_DATA_SYNTHESIS = auto()
    MEASURED_DATA_REPRESENTATIVENESS = auto()

    # Project evaluation period annual variability
    WIND_SPEED_VARIABILITY = auto()
    CLIMATE_CHANGE = auto()
    PLANT_PERFORMANCE = auto()  # TODO clarify distinction to energy uncertainty

    # Measurement uncertainty
    WIND_SPEED_MEASUREMENT = auto()
    WIND_DIRECTION_MEASUREMENT = auto()  # TODO clarify conversion to wind speed
    OTHER_ATMOSPHERIC_PARAMETERS = auto()  # TODO clarify conversion to wind speed
    DATA_INTEGRITY = auto()  # Includes data integrity and documentation

    # Horizontal extrapolation
    MODEL_INPUTS = auto()
    MODEL_SENSITIVITY = auto()  # Covering model stress tests
    MODEL_APPROPRIATENESS = auto()

    # Vertical extrapolation
    MODEL_UNCERTAINTY = auto()
    EXCESS_PROPAGATED_UNCERTAINTY = auto()  # Propagated from measurement uncertainty

    OTHER = auto()

    @property
    def category(self) -> WindUncertaintyCategoryLabel:
        """The category parent corresponding to the subcategory."""
        match self:
            case WindUncertaintySubcategoryLabel.LONG_TERM_PERIOD_REPRESENTATIVENESS:
                return WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE
            case WindUncertaintySubcategoryLabel.REFERENCE_DATA_CONSISTENCY:
                return WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE
            case WindUncertaintySubcategoryLabel.LONG_TERM_ADJUSTMENT:
                return WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE
            case WindUncertaintySubcategoryLabel.WIND_SPEED_DISTRIBUTION_UNCERTAINTY:
                return WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE
            case WindUncertaintySubcategoryLabel.ON_SITE_DATA_SYNTHESIS:
                return WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE
            case WindUncertaintySubcategoryLabel.MEASURED_DATA_REPRESENTATIVENESS:
                return WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE
            case WindUncertaintySubcategoryLabel.WIND_SPEED_VARIABILITY:
                return WindUncertaintyCategoryLabel.FUTURE_ASSESSMENT_PERIOD_VARIABILITY
            case WindUncertaintySubcategoryLabel.CLIMATE_CHANGE:
                return WindUncertaintyCategoryLabel.FUTURE_ASSESSMENT_PERIOD_VARIABILITY
            case WindUncertaintySubcategoryLabel.PLANT_PERFORMANCE:
                return WindUncertaintyCategoryLabel.FUTURE_ASSESSMENT_PERIOD_VARIABILITY
            case WindUncertaintySubcategoryLabel.WIND_SPEED_MEASUREMENT:
                return WindUncertaintyCategoryLabel.MEASUREMENT
            case WindUncertaintySubcategoryLabel.WIND_DIRECTION_MEASUREMENT:
                return WindUncertaintyCategoryLabel.MEASUREMENT
            case WindUncertaintySubcategoryLabel.OTHER_ATMOSPHERIC_PARAMETERS:
                return WindUncertaintyCategoryLabel.MEASUREMENT
            case WindUncertaintySubcategoryLabel.DATA_INTEGRITY:
                return WindUncertaintyCategoryLabel.MEASUREMENT
            case WindUncertaintySubcategoryLabel.MODEL_INPUTS:
                return WindUncertaintyCategoryLabel.HORIZONTAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.MODEL_SENSITIVITY:
                return WindUncertaintyCategoryLabel.HORIZONTAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.MODEL_APPROPRIATENESS:
                return WindUncertaintyCategoryLabel.HORIZONTAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.MODEL_UNCERTAINTY:
                return WindUncertaintyCategoryLabel.VERTICAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.EXCESS_PROPAGATED_UNCERTAINTY:
                return WindUncertaintyCategoryLabel.VERTICAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.OTHER:
                return WindUncertaintyCategoryLabel.OTHER


class WindUncertaintySubcategory(EyaDefBaseModel):
    """Subcategory of a wind related uncertainty assessment."""

    label: WindUncertaintySubcategoryLabel = pdt.Field(
        default=...,
        description="Label of the wind related uncertainty subcategory.",
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the wind related uncertainty "
            "subcategory, which should not be empty if the field is "
            "included."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the wind related uncertainty "
            "subcategory, which should not be empty if the field is "
            "included."
        ),
    )
    elements: Optional[list[WindUncertaintySubcategoryElement]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Wind related uncertainty assessment elements that fall under "
            "the subcategory. The element objects include details and results "
            "at the element level. A breakdown of wind related uncertainty "
            "subcategories into elements is optional and can be included only "
            "for a subset of the subcategories, as relevant. Whereas the "
            "categories and subcategories are fixed, the user may freely "
            "define element labels."
        ),
    )
    results: UncertaintyResults = pdt.Field(
        default=...,
        description="Wind related uncertainty assessment subcategory results.",
    )


class WindUncertaintyCategoryLabel(StrEnum):
    """Category labels in the wind uncertainty assessment."""

    MEASUREMENT = auto()
    HISTORICAL_WIND_RESOURCE = auto()
    FUTURE_ASSESSMENT_PERIOD_VARIABILITY = auto()
    VERTICAL_EXTRAPOLATION = auto()
    HORIZONTAL_EXTRAPOLATION = auto()
    OTHER = auto()


class WindUncertaintyCategory(EyaDefBaseModel):
    """Category of a wind related uncertainty assessment."""

    label: WindUncertaintyCategoryLabel = pdt.Field(
        default=...,
        description="Label of the wind related uncertainty assessment category.",
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the wind related uncertainty "
            "category, which should not be empty if the field is "
            "included."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the wind related uncertainty "
            "category, which should not be empty if the field is "
            "included."
        ),
    )
    subcategories: list[WindUncertaintySubcategory] = pdt.Field(
        default=...,
        description=(
            "Wind related uncertainty assessment subcategories that fall "
            "under the category. The subcategory objects include details and "
            "results at the subcategory level."
        ),
    )
    results: UncertaintyResults = pdt.Field(
        default=...,
        description="Wind related uncertainty assessment category results.",
    )


class WindUncertaintyAssessment(EyaDefBaseModel):
    """Wind related uncertainty assessment broken into categories."""

    categories: list[WindUncertaintyCategory] = pdt.Field(
        default=...,
        min_length=1,
        description="Wind related uncertainty assessment categories including results.",
    )
    results: UncertaintyResults = pdt.Field(
        default=...,
        description="Overall wind related uncertainty assessment results.",
    )
    # TODO consider including wind speed to energy sensitivity ratio
