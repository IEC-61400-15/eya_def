"""Pydantic data models relating to plant performance loss assessments.

"""

import pydantic as pdt

from eya_def_tools.data_models import assessment_process_description as eya_prcs_desc
from eya_def_tools.data_models import assessment_results, base_models, enums


class PlantPerformanceSubcategory(base_models.EyaDefBaseModel):
    """Plant performance loss assessment subcategory."""

    label: enums.PlantPerformanceSubcategoryLabel = pdt.Field(
        ..., description="Label of the plant performance category."
    )
    basis: enums.AssessmentBasis = pdt.Field(
        ..., description="Basis of plant performance element assessment."
    )
    variability: enums.VariabilityType = pdt.Field(
        ..., description="Considered variability in plant performance element."
    )
    assessment_processes: list[
        eya_prcs_desc.AssessmentProcessDescription
    ] | None = pdt.Field(None, description="Calculation models used in the assessment.")
    results: assessment_results.Result = pdt.Field(
        ..., description="Plant performance assessment subcategory results."
    )


class PlantPerformanceCategory(base_models.EyaDefBaseModel):
    """Plant performance loss assessment category."""

    label: enums.PlantPerformanceCategoryLabel = pdt.Field(
        ..., description="Label of the plant performance category."
    )
    subcategories: list[PlantPerformanceSubcategory] = pdt.Field(
        ...,
        description=(
            "Plant performance assessment subcategories that fall under the category."
        ),
    )
    category_results: list[assessment_results.Result] = pdt.Field(
        ..., description="Category level assessment results."
    )
