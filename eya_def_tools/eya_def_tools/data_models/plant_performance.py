"""Data models relating to plant performance loss assessments.

"""

from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.enums import (
    AssessmentBasis,
    PlantPerformanceCategoryLabel,
    PlantPerformanceSubcategoryLabel,
    TimeVariabilityType,
)
from eya_def_tools.data_models.process_description import AssessmentProcessDescription
from eya_def_tools.data_models.result import Result


class PlantPerformanceResults(EyaDefBaseModel):
    """Plant performance loss assessment results."""

    efficiency: list[Result] = pdt.Field(
        default=...,
        description=(
            "Dimensionless plant performance efficiency (loss factor) results."
        ),
    )


class PlantPerformanceSubcategoryElement(EyaDefBaseModel):
    """Plant performance loss assessment subcategory element."""

    label: str = pdt.Field(
        default=...,
        description="Label of the plant performance loss subcategory element.",
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description=(
            "Optional description of the plant performance loss subcategory element."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description=(
            "Optional comments on the plant performance loss subcategory element."
        ),
    )
    basis: AssessmentBasis = pdt.Field(
        default=...,
        description=(
            "Basis of plant performance loss subcategory element assessment. The "
            "basis describes the level of detail of the calculation or estimate "
            "used in the assessment of the element."
        ),
    )
    variability: TimeVariabilityType = pdt.Field(
        default=...,
        description=(
            "Considered variability in the plant performance loss subcategory element."
        ),
    )
    is_independent: bool = pdt.Field(
        default=True,
        description=(
            "Whether the plant performance loss subcategory element is independent "
            "of all other elements."
        ),
    )
    assessment_process_descriptions: (
        Optional[list[AssessmentProcessDescription]]
    ) = pdt.Field(
        default=None,
        description=(
            "Description of calculation processes used in the assessment of "
            "the plant performance loss subcategory element."
        ),
    )
    results: PlantPerformanceResults = pdt.Field(
        default=...,
        description="Plant performance assessment subcategory element results.",
    )


class PlantPerformanceSubcategory(EyaDefBaseModel):
    """Plant performance loss assessment subcategory."""

    label: PlantPerformanceSubcategoryLabel = pdt.Field(
        default=...,
        description="Label of the plant performance loss subcategory.",
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the plant performance loss subcategory.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the plant performance loss subcategory.",
    )
    basis: AssessmentBasis = pdt.Field(
        default=...,
        description=(
            "Basis of plant performance loss subcategory assessment. The basis "
            "describes the level of detail of the calculation or estimate used "
            "in the assessment of the subcategory."
        ),
    )
    variability: TimeVariabilityType = pdt.Field(
        default=...,
        description="Considered variability in the plant performance loss subcategory.",
    )
    assessment_process_descriptions: (
        Optional[list[AssessmentProcessDescription]]
    ) = pdt.Field(
        default=None,
        description=(
            "Description of calculation processes used in the assessment of "
            "the plant performance loss subcategory."
        ),
    )
    elements: Optional[list[PlantPerformanceSubcategoryElement]] = pdt.Field(
        default=None,
        description=(
            "Plant performance loss assessment elements that fall under the "
            "subcategory. The element objects include details and results "
            "at the element level. A breakdown of plant performance loss "
            "subcategories into elements is optional and can be included only "
            "for a subset of the subcategories, as relevant. Whereas the "
            "categories and subcategories are fixed, the user may freely "
            "define element labels."
        ),
    )
    results: PlantPerformanceResults = pdt.Field(
        default=...,
        description="Plant performance assessment subcategory results.",
    )


class PlantPerformanceCategory(EyaDefBaseModel):
    """Plant performance loss assessment category."""

    label: PlantPerformanceCategoryLabel = pdt.Field(
        default=...,
        description="Label of the plant performance loss category.",
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the plant performance loss category.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the plant performance loss category.",
    )
    subcategories: list[PlantPerformanceSubcategory] = pdt.Field(
        default=...,
        description=(
            "Plant performance loss assessment subcategories that fall under "
            "the category. The subcategory objects include details and results "
            "at the subcategory level."
        ),
    )
    results: PlantPerformanceResults = pdt.Field(
        default=...,
        description="Plant performance assessment category results.",
    )


class PlantPerformanceAssessment(EyaDefBaseModel):
    """Plant performance loss assessment broken into categories."""

    categories: list[PlantPerformanceCategory] = pdt.Field(
        default=...,
        description="Plant performance loss assessment categories including results.",
    )
    results: PlantPerformanceResults = pdt.Field(
        default=...,
        description="Overall plant performance loss assessment results.",
    )
