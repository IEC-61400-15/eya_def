"""Pydantic data models relating to wind uncertainty.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.enums import (
    WindUncertaintyCategoryLabel,
    WindUncertaintySubcategoryLabel,
)
from eya_def_tools.data_models.generic_fields import comments_field, description_field
from eya_def_tools.data_models.result import Result


class WindUncertaintySubcategoryElement(EyaDefBaseModel):
    """Subcategory element of a wind related uncertainty assessment."""

    label: str = pdt.Field(
        ...,
        description="Label of the wind related uncertainty subcategory element.",
    )
    description: str | None = description_field
    comments: str | None = comments_field
    is_independent: bool = pdt.Field(
        True,
        description=(
            "Whether the wind related uncertainty subcategory element is "
            "independent of all other elements."
        ),
    )
    element_results: list[Result] = pdt.Field(
        ...,
        description=(
            "Wind related uncertainty assessment subcategory element result(s) as "
            "dimensionless relative values."
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
    subcategory_results: list[Result] = pdt.Field(
        ...,
        description=(
            "Wind related uncertainty assessment subcategory result(s) as "
            "dimensionless relative values."
        ),
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
            "Wind related uncertainty assessment subcategories that fall under "
            "the category. The subcategory objects include details and results "
            "at the subcategory level."
        ),
    )
    category_results: list[Result] = pdt.Field(
        ...,
        description=(
            "Wind related uncertainty assessment category result(s) as "
            "dimensionless relative values."
        ),
    )
