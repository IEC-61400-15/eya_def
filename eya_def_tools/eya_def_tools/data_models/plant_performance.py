"""Pydantic data models relating to plant performance loss assessments.

"""

import pydantic as pdt

from eya_def_tools.data_models import base_models, enums
from eya_def_tools.data_models.assessment_process_description import (
    AssessmentProcessDescription,
)
from eya_def_tools.data_models.assessment_results import Result
from eya_def_tools.data_models.fields import comments_field, description_field


class PlantPerformanceElement(base_models.EyaDefBaseModel):
    """Plant performance loss assessment element."""

    label: str = pdt.Field(
        ...,
        description="Label of the plant performance loss element.",
    )
    description: str | None = description_field
    comments: str | None = comments_field
    basis: enums.AssessmentBasis = pdt.Field(
        ...,
        description=(
            "Basis of plant performance loss element assessment. The basis "
            "describes the level of detail of the calculation or estimate used "
            "in the assessment of the element."
        ),
    )
    variability: enums.VariabilityType = pdt.Field(
        ...,
        description="Considered variability in the plant performance loss element.",
    )
    is_independent: bool = pdt.Field(
        True,
        description=(
            "Whether the plant performance loss element is independent of all other "
            "elements."
        ),
    )
    assessment_process_descriptions: list[
        AssessmentProcessDescription
    ] | None = pdt.Field(
        None,
        description=(
            "Description of calculation processes used in the assessment of "
            "the plant performance loss element."
        ),
    )
    is_preliminary: bool = pdt.Field(
        False,
        description=(
            "Whether the assessment of the plant performance loss assessment "
            "element should be marked as preliminary."
        ),
    )
    element_results: Result = pdt.Field(
        ...,
        description=(
            "Plant performance assessment element results as dimensionless loss "
            "factors (efficiencies)."
        ),
    )


class PlantPerformanceSubcategory(base_models.EyaDefBaseModel):
    """Plant performance loss assessment subcategory."""

    label: enums.PlantPerformanceSubcategoryLabel = pdt.Field(
        ...,
        description="Label of the plant performance loss subcategory.",
    )
    basis: enums.AssessmentBasis = pdt.Field(
        ...,
        description=(
            "Basis of plant performance loss subcategory assessment. The basis "
            "describes the level of detail of the calculation or estimate used "
            "in the assessment of the subcategory."
        ),
    )
    variability: enums.VariabilityType = pdt.Field(
        ...,
        description="Considered variability in the plant performance loss subcategory.",
    )
    assessment_process_descriptions: list[
        AssessmentProcessDescription
    ] | None = pdt.Field(
        None,
        description=(
            "Description of calculation processes used in the assessment of "
            "the plant performance loss subcategory."
        ),
    )
    is_preliminary: bool = pdt.Field(
        False,
        description=(
            "Whether the assessment of the plant performance loss assessment "
            "subcategory should be marked as preliminary."
        ),
    )
    elements: list[PlantPerformanceElement] | None = pdt.Field(
        None,
        description=(
            "Plant performance loss assessment elements that fall under the "
            "the subcategory. The element objects include details and results "
            "at the element level. A breakdown of plant performance loss "
            "subcategories into elements is optional and can be included only "
            "for a subset of the subcategories, as relevant. Whereas the "
            "categories and subcategories are fixed, the user may freely "
            "define element labels."
        ),
    )
    subcategory_results: Result = pdt.Field(
        ...,
        description=(
            "Plant performance assessment subcategory results as dimensionless loss "
            "factors (efficiencies)."
        ),
    )


class PlantPerformanceCategory(base_models.EyaDefBaseModel):
    """Plant performance loss assessment category."""

    label: enums.PlantPerformanceCategoryLabel = pdt.Field(
        ...,
        description="Label of the plant performance loss category.",
    )
    subcategories: list[PlantPerformanceSubcategory] = pdt.Field(
        ...,
        description=(
            "Plant performance loss assessment subcategories that fall under "
            "the category. The subcategory objects include details and results "
            "at the subcategory level."
        ),
    )
    category_results: list[Result] = pdt.Field(
        ...,
        description=(
            "Plant performance assessment category results as dimensionless loss "
            "factors (efficiencies)."
        ),
    )
