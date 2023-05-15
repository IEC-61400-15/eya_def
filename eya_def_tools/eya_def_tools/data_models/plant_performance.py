"""Pydantic data models relating to plant performance loss assessments.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_models import EyaDefBaseModel
from eya_def_tools.data_models.enums import (
    AssessmentBasis,
    PlantPerformanceCategoryLabel,
    PlantPerformanceSubcategoryLabel,
    TimeVariabilityType,
)
from eya_def_tools.data_models.fields import comments_field, description_field
from eya_def_tools.data_models.process_description import AssessmentProcessDescription
from eya_def_tools.data_models.result import Result


class PlantPerformanceSubcategoryElement(EyaDefBaseModel):
    """Plant performance loss assessment subcategory element."""

    label: str = pdt.Field(
        ...,
        description="Label of the plant performance loss subcategory element.",
    )
    description: str | None = description_field
    comments: str | None = comments_field
    basis: AssessmentBasis = pdt.Field(
        ...,
        description=(
            "Basis of plant performance loss subcategory element assessment. The "
            "basis describes the level of detail of the calculation or estimate "
            "used in the assessment of the element."
        ),
    )
    variability: TimeVariabilityType = pdt.Field(
        ...,
        description=(
            "Considered variability in the plant performance loss subcategory element."
        ),
    )
    is_independent: bool = pdt.Field(
        True,
        description=(
            "Whether the plant performance loss subcategory element is independent "
            "of all other elements."
        ),
    )
    assessment_process_descriptions: (
        list[AssessmentProcessDescription] | None
    ) = pdt.Field(
        None,
        description=(
            "Description of calculation processes used in the assessment of "
            "the plant performance loss subcategory element."
        ),
    )
    # TODO consider if we want to keep a flag to mark the assessment of a
    #      plant performance subcategory element as preliminary
    # is_preliminary: bool = pdt.Field(
    #     False,
    #     description=(
    #         "Whether the assessment of the plant performance loss assessment "
    #         "subcategory element should be marked as preliminary."
    #     ),
    # )
    element_results: list[Result] = pdt.Field(
        ...,
        description=(
            "Plant performance assessment subcategory element result(s) as "
            "dimensionless loss factors (efficiencies)."
        ),
    )


class PlantPerformanceSubcategory(EyaDefBaseModel):
    """Plant performance loss assessment subcategory."""

    label: PlantPerformanceSubcategoryLabel = pdt.Field(
        ...,
        description="Label of the plant performance loss subcategory.",
    )
    basis: AssessmentBasis = pdt.Field(
        ...,
        description=(
            "Basis of plant performance loss subcategory assessment. The basis "
            "describes the level of detail of the calculation or estimate used "
            "in the assessment of the subcategory."
        ),
    )
    variability: TimeVariabilityType = pdt.Field(
        ...,
        description="Considered variability in the plant performance loss subcategory.",
    )
    assessment_process_descriptions: (
        list[AssessmentProcessDescription] | None
    ) = pdt.Field(
        None,
        description=(
            "Description of calculation processes used in the assessment of "
            "the plant performance loss subcategory."
        ),
    )
    # TODO consider if we want to keep a flag to mark the assessment of a
    #      plant performance subcategory as preliminary
    # is_preliminary: bool = pdt.Field(
    #     False,
    #     description=(
    #         "Whether the assessment of the plant performance loss assessment "
    #         "subcategory should be marked as preliminary."
    #     ),
    # )
    elements: list[PlantPerformanceSubcategoryElement] | None = pdt.Field(
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
    subcategory_results: list[Result] = pdt.Field(
        ...,
        description=(
            "Plant performance assessment subcategory result(s) as dimensionless "
            "loss factors (efficiencies)."
        ),
    )


class PlantPerformanceCategory(EyaDefBaseModel):
    """Plant performance loss assessment category."""

    label: PlantPerformanceCategoryLabel = pdt.Field(
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
            "Plant performance assessment category result(s) as dimensionless loss "
            "factors (efficiencies)."
        ),
    )
