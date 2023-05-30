"""Pydantic data models relating to uncertainty assessments.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_models import EyaDefBaseModel
from eya_def_tools.data_models.enums import UncertaintyCategoryLabel
from eya_def_tools.data_models.generic_fields import comments_field, description_field
from eya_def_tools.data_models.result import Result


# TODO - this needs to be completed with more fields for relevant details
#      - it may need to be separated for the measurement wind resource
#        assessment and the turbine wind resource assessment
class UncertaintySubcategory(EyaDefBaseModel):
    """Wind resource uncertainty assessment subcategory."""

    # TODO this should also be an enum
    label: str = pdt.Field(
        ...,
        description="Label of the wind resource uncertainty subcategory.",
        examples=["Long-term consistency"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    subcategory_results: list[Result] = pdt.Field(
        ...,
        description="Wind resource uncertainty assessment subcategory results.",
    )


class UncertaintyCategory(EyaDefBaseModel):
    """Wind resource uncertainty assessment category."""

    label: UncertaintyCategoryLabel = pdt.Field(
        ...,
        description="Label of the uncertainty category.",
    )
    subcategories: list[UncertaintySubcategory] = pdt.Field(
        ...,
        description="Wind resource uncertainty assessment subcategories.",
    )
    category_results: list[Result] = pdt.Field(
        ...,
        description="Category level assessment results.",
    )


class UncertaintyAssessment(EyaDefBaseModel):
    """Wind resource uncertainty assessment."""

    categories: list[UncertaintyCategory] = pdt.Field(
        ...,
        description="List of wind resource uncertainty assessment categories.",
    )
