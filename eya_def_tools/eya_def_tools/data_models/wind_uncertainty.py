"""Data models relating to wind uncertainty.

"""

from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.enums import (
    WindUncertaintyCategoryLabel,
    WindUncertaintySubcategoryLabel,
)
from eya_def_tools.data_models.result import Result


class UncertaintyResults(EyaDefBaseModel):
    """Uncertainty assessment results."""

    relative_wind_speed_uncertainty: Optional[list[Result]] = pdt.Field(
        default=None,
        description=(
            "Uncertainty assessment results as dimensionless relative values "
            "expressed in terms of wind speed and calculated as the standard "
            "deviation of the wind speed uncertainty distribution divided by "
            "the mean wind speed."
        ),
    )
    relative_energy_uncertainty: Optional[list[Result]] = pdt.Field(
        default=None,
        description=(
            "Uncertainty assessment results as dimensionless relative values "
            "expressed in terms of AEP (annual energy production) and "
            "calculated as the standard deviation of the energy uncertainty "
            "distribution divided by the net P50 (50% probability of "
            "exceedance level) AEP."
        ),
    )


class WindUncertaintySubcategoryElement(EyaDefBaseModel):
    """Subcategory element of a wind related uncertainty assessment."""

    label: str = pdt.Field(
        default=...,
        description="Label of the wind related uncertainty subcategory element.",
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description=(
            "Optional description of the wind related uncertainty subcategory element."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description=(
            "Optional comments on the wind related uncertainty subcategory element."
        ),
    )
    results: UncertaintyResults = pdt.Field(
        default=...,
        description=(
            "Wind related uncertainty assessment subcategory element results."
        ),
    )


class WindUncertaintySubcategory(EyaDefBaseModel):
    """Subcategory of a wind related uncertainty assessment."""

    label: WindUncertaintySubcategoryLabel = pdt.Field(
        default=...,
        description="Label of the wind related uncertainty subcategory.",
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the wind related uncertainty subcategory.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the wind related uncertainty subcategory.",
    )
    elements: Optional[list[WindUncertaintySubcategoryElement]] = pdt.Field(
        default=None,
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


class WindUncertaintyCategory(EyaDefBaseModel):
    """Category of a wind related uncertainty assessment."""

    label: WindUncertaintyCategoryLabel = pdt.Field(
        default=...,
        description="Label of the wind related uncertainty assessment category.",
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the wind related uncertainty category.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the wind related uncertainty category.",
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
        description="Wind related uncertainty assessment categories including results.",
    )
    results: UncertaintyResults = pdt.Field(
        default=...,
        description="Overall wind related uncertainty assessment results.",
    )
    # TODO consider including wind speed to energy sensitivity ratio
