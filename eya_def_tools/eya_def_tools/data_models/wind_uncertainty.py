"""Data models relating to wind uncertainty.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.enums import (
    WindUncertaintyCategoryLabel,
    WindUncertaintySubcategoryLabel,
)
from eya_def_tools.data_models.generic_fields import comments_field, description_field
from eya_def_tools.data_models.result import Result


class UncertaintyResults(EyaDefBaseModel):
    """Uncertainty assessment results."""

    relative_wind_speed_uncertainty: list[Result] | None = pdt.Field(
        None,
        description=(
            "Uncertainty assessment results as dimensionless relative values "
            "expressed in terms of wind speed and calculated as the standard "
            "deviation of the wind speed uncertainty distribution divided by "
            "the mean wind speed."
        ),
    )
    relative_energy_uncertainty: list[Result] | None = pdt.Field(
        None,
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
        ...,
        description="Label of the wind related uncertainty subcategory element.",
    )
    description: str | None = description_field
    comments: str | None = comments_field
    # TODO decide whether to include details on uncertainty correlation
    # is_independent: bool = pdt.Field(
    #     True,
    #     description=(
    #         "Whether the wind related uncertainty subcategory element is "
    #         "independent of all other elements."
    #     ),
    # )
    results: UncertaintyResults = pdt.Field(
        ...,
        description=(
            "Wind related uncertainty assessment subcategory element results."
        ),
    )


class WindUncertaintySubcategory(EyaDefBaseModel):
    """Subcategory of a wind related uncertainty assessment."""

    label: WindUncertaintySubcategoryLabel = pdt.Field(
        ...,
        description="Label of the wind related uncertainty subcategory.",
    )
    description: str | None = description_field
    comments: str | None = comments_field
    elements: list[WindUncertaintySubcategoryElement] | None = pdt.Field(
        None,
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
        ...,
        description="Wind related uncertainty assessment subcategory results.",
    )


class WindUncertaintyCategory(EyaDefBaseModel):
    """Category of a wind related uncertainty assessment."""

    label: WindUncertaintyCategoryLabel = pdt.Field(
        ...,
        description="Label of the wind related uncertainty assessment category.",
    )
    description: str | None = description_field
    comments: str | None = comments_field
    subcategories: list[WindUncertaintySubcategory] = pdt.Field(
        ...,
        description=(
            "Wind related uncertainty assessment subcategories that fall "
            "under the category. The subcategory objects include details and "
            "results at the subcategory level."
        ),
    )
    results: UncertaintyResults = pdt.Field(
        ...,
        description="Wind related uncertainty assessment category results.",
    )


class WindUncertaintyAssessment(EyaDefBaseModel):
    """Wind related uncertainty assessment broken into categories."""

    categories: list[WindUncertaintyCategory] = pdt.Field(
        ...,
        description="Wind related uncertainty assessment categories including results.",
    )
    results: UncertaintyResults = pdt.Field(
        ...,
        description="Overall wind related uncertainty assessment results.",
    )
    # TODO consider including wind speed to energy sensitivity ratio
