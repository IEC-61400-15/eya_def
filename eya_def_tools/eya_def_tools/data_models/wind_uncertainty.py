"""Data models relating to wind uncertainty.

The wind uncertainty covers the different elements of the wind resource
assessment, which feed into the estimate of the gross energy production.
The uncertainty components are assessed in relative wind speed terms and
converted to relative energy terms through a sensitivity. The wind speed
to energy sensitivity is calculated from a perturbation around the net
energy estimate, hence the relative energy uncertainty values relate to
net AEP and not gross AEP.

"""

from __future__ import annotations

from enum import StrEnum, auto

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.dataset import Dataset


class WindUncertaintyResults(EyaDefBaseModel):
    """Wind uncertainty assessment results."""

    relative_wind_speed_uncertainty: list[Dataset] | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Uncertainty assessment results as dimensionless relative "
            "values expressed in terms of wind speed and calculated as "
            "the standard deviation of the wind speed uncertainty "
            "distribution divided by the mean wind speed. The first "
            "standard dataset should present results without binning "
            "(i.e. correspond to the overall value for the wind farm "
            "under assessment). For wind uncertainty components "
            "related to a wind dataset (e.g. measurement uncertainty), "
            "a second standard dataset should present results with "
            "binning dimension 'wind_dataset_id'. Datasets with other "
            "binning dimensions may also be included optionally."
        ),
    )
    relative_energy_uncertainty: list[Dataset] | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Uncertainty assessment results as dimensionless relative "
            "values expressed in terms of net annual energy production "
            "(AEP) and calculated as the standard deviation of the "
            "energy uncertainty distribution divided by the net P50 "
            "(50% probability of exceedance level) AEP. The first "
            "standard dataset should present results without binning "
            "(i.e. correspond to the overall value for the wind farm "
            "under assessment). Datasets with other binning dimensions "
            "may also be included optionally."
        ),
    )

    @pdt.model_validator(mode="after")
    def validate_has_at_least_one_result(self) -> WindUncertaintyResults:
        if (
            self.relative_wind_speed_uncertainty is None
            and self.relative_energy_uncertainty is None
        ):
            raise ValueError(
                "A wind uncertainty assessment results object without "
                "any results datasets is not valid. At least one of "
                "the field 'relative_wind_speed_uncertainty' and "
                "'relative_energy_uncertainty' must be included."
            )

        return self


class WindUncertaintySubcategoryElement(EyaDefBaseModel):
    """Subcategory element of a wind related uncertainty assessment."""

    label: str = pdt.Field(
        default=...,
        min_length=1,
        description="Label of the wind uncertainty subcategory element.",
    )
    description: str | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the wind uncertainty subcategory "
            "element, which should not be empty if the field is included."
        ),
    )
    comments: str | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the wind uncertainty subcategory "
            "element, which should not be empty if the field is included."
        ),
    )
    results: WindUncertaintyResults = pdt.Field(
        default=...,
        description=("Wind uncertainty assessment subcategory element results."),
    )


class WindUncertaintySubcategoryLabel(StrEnum):
    """Subcategory labels in the wind uncertainty assessment."""

    # Measurement uncertainty
    WIND_SPEED_MEASUREMENT = auto()
    WIND_DIRECTION_MEASUREMENT = auto()
    OTHER_ATMOSPHERIC_PARAMETERS = auto()
    DATA_INTEGRITY = auto()

    # Historical wind resource
    LONG_TERM_PERIOD_REPRESENTATIVENESS = auto()
    REFERENCE_DATA_CONSISTENCY = auto()
    LONG_TERM_ADJUSTMENT = auto()
    WIND_SPEED_DISTRIBUTION_UNCERTAINTY = auto()
    ON_SITE_DATA_SYNTHESIS = auto()
    MEASURED_DATA_REPRESENTATIVENESS = auto()

    # Vertical extrapolation
    VERTICAL_MODEL_UNCERTAINTY = auto()
    EXCESS_PROPAGATED_UNCERTAINTY = auto()

    # Horizontal extrapolation
    HORIZONTAL_MODEL_INPUTS = auto()
    HORIZONTAL_MODEL_SENSITIVITY = auto()
    HORIZONTAL_MODEL_APPROPRIATENESS = auto()

    # Project evaluation period annual variability
    WIND_SPEED_VARIABILITY = auto()
    CLIMATE_CHANGE = auto()

    OTHER = auto()

    @property
    def category(self) -> WindUncertaintyCategoryLabel:
        """The category parent corresponding to the subcategory."""
        match self:
            case WindUncertaintySubcategoryLabel.WIND_SPEED_MEASUREMENT:
                return WindUncertaintyCategoryLabel.MEASUREMENT
            case WindUncertaintySubcategoryLabel.WIND_DIRECTION_MEASUREMENT:
                return WindUncertaintyCategoryLabel.MEASUREMENT
            case WindUncertaintySubcategoryLabel.OTHER_ATMOSPHERIC_PARAMETERS:
                return WindUncertaintyCategoryLabel.MEASUREMENT
            case WindUncertaintySubcategoryLabel.DATA_INTEGRITY:
                return WindUncertaintyCategoryLabel.MEASUREMENT
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
            case WindUncertaintySubcategoryLabel.HORIZONTAL_MODEL_INPUTS:
                return WindUncertaintyCategoryLabel.HORIZONTAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.HORIZONTAL_MODEL_SENSITIVITY:
                return WindUncertaintyCategoryLabel.HORIZONTAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.HORIZONTAL_MODEL_APPROPRIATENESS:
                return WindUncertaintyCategoryLabel.HORIZONTAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.VERTICAL_MODEL_UNCERTAINTY:
                return WindUncertaintyCategoryLabel.VERTICAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.EXCESS_PROPAGATED_UNCERTAINTY:
                return WindUncertaintyCategoryLabel.VERTICAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.WIND_SPEED_VARIABILITY:
                return WindUncertaintyCategoryLabel.FUTURE_ASSESSMENT_PERIOD_VARIABILITY
            case WindUncertaintySubcategoryLabel.CLIMATE_CHANGE:
                return WindUncertaintyCategoryLabel.FUTURE_ASSESSMENT_PERIOD_VARIABILITY
            case WindUncertaintySubcategoryLabel.OTHER:
                return WindUncertaintyCategoryLabel.OTHER


class WindUncertaintySubcategory(EyaDefBaseModel):
    """Subcategory of a wind uncertainty assessment."""

    label: WindUncertaintySubcategoryLabel = pdt.Field(
        default=...,
        description="Label of the wind uncertainty subcategory.",
    )
    description: str | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the wind uncertainty subcategory, "
            "which should not be empty if the field is included."
        ),
    )
    comments: str | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the wind uncertainty subcategory, which should not be empty if the field is included."
        ),
    )
    elements: list[WindUncertaintySubcategoryElement] | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Wind uncertainty assessment elements that fall under the "
            "subcategory. The element objects include details and "
            "results at the element level. A breakdown of wind "
            "uncertainty subcategories into elements is optional and "
            "can be included only for a subset of the subcategories, "
            "as relevant. Whereas the categories and subcategories are "
            "fixed, the user may freely define element labels."
        ),
    )
    results: WindUncertaintyResults = pdt.Field(
        default=...,
        description="Wind uncertainty assessment subcategory results.",
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
    """Category of a wind uncertainty assessment."""

    label: WindUncertaintyCategoryLabel = pdt.Field(
        default=...,
        description="Label of the wind uncertainty assessment category.",
    )
    description: str | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the wind uncertainty category, which should not be empty if the field is included."
        ),
    )
    comments: str | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the wind uncertainty category, which should not be empty if the field is included."
        ),
    )
    subcategories: list[WindUncertaintySubcategory] = pdt.Field(
        default=...,
        description=(
            "Wind uncertainty assessment subcategories that fall under "
            "the category. The subcategory objects include details and "
            "results at the subcategory level."
        ),
    )
    results: WindUncertaintyResults = pdt.Field(
        default=...,
        description="Wind uncertainty assessment category results.",
    )


class WindUncertaintyAssessment(EyaDefBaseModel):
    """Wind uncertainty assessment broken into categories."""

    categories: list[WindUncertaintyCategory] = pdt.Field(
        default=...,
        min_length=1,
        description="Wind uncertainty assessment categories including results.",
    )
    results: WindUncertaintyResults = pdt.Field(
        default=...,
        description="Overall wind related uncertainty assessment results.",
    )
    wind_speed_to_energy_sensitivity_factor: pdt.PositiveFloat = pdt.Field(
        default=...,
        description=(
            "The dimensionless relative wind-speed-to-energy "
            "sensitivity factor, calculated as the dimensionless "
            "relative difference in net energy divided by the "
            "corresponding relative wind speed perturbation."
        ),
        examples=[1.6, 2.1],
    )
