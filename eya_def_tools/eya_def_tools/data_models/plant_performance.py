"""Data models relating to plant performance loss assessments.

"""

from __future__ import annotations

from enum import StrEnum, auto
from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.dataset import Dataset
from eya_def_tools.data_models.general import (
    AnyAssessmentComponentProvenance,
    AssessmentComponentBasis,
    TimeVariabilityType,
    get_default_assessment_component_provenance,
)


class PlantPerformanceResults(EyaDefBaseModel):
    """Plant performance loss assessment results."""

    efficiency: list[Dataset] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Dimensionless plant performance efficiency (loss factor) "
            "results. The first standard dataset should have no "
            "binning dimension (i.e. correspond to the overall value "
            "for the wind farm(s) under assessment). Datasets with "
            "results binned by turbine should also be included where "
            "the efficiency is predicted at the turbine level, such as "
            "for the turbine interaction losses. Further results with "
            "other dimensions may also be included. All datasets "
            "should include the 'mean' and 'standard_deviation', "
            "statistics, where the former represents the central "
            "estimate and the latter the standard deviation of the "
            "associated uncertainty distribution. For the overall "
            "plant performance efficiency estimate at the wind farm "
            "level (i.e. the result dataset without binning), the "
            "statistic 'inter_annual_variability' must also be "
            "included. The inter-annual variability may optionally "
            "also be included for some or all of the other datasets."
        ),
    )


class PlantPerformanceSubcategoryElement(EyaDefBaseModel):
    """Plant performance loss assessment subcategory element."""

    label: str = pdt.Field(
        default=...,
        min_length=1,
        description="Label of the plant performance loss subcategory element.",
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the plant performance loss "
            "subcategory element, which should not be empty if the "
            "field is included."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the plant performance loss "
            "subcategory element, which should not be empty if the "
            "field is included."
        ),
    )
    basis: AssessmentComponentBasis = pdt.Field(
        default=...,
        description=(
            "Basis of the plant performance loss subcategory element "
            "assessment. The basis describes the method and level of "
            "detail of the calculation or assumption used in the "
            "assessment of the element."
        ),
    )
    provenance: AnyAssessmentComponentProvenance = pdt.Field(
        default_factory=get_default_assessment_component_provenance,
        discriminator="assessor_type",
        description=(
            "Provenance of the plant performance loss subcategory "
            "element assessment, including specification of the "
            "assessor type (issuing organisation, receiving "
            "organisation, commissioning organisation or other "
            "organisation), and if relevant also the assessor "
            "organisation and status of verification. Where the "
            "specification of the provenance is omitted, it shall be "
            "assumed that the assessor is the issuing organisation(s) "
            "of the EYA. Further details can be included in the "
            "description and comment fields of the plant performance "
            "subcategory element."
        ),
    )
    variability: TimeVariabilityType = pdt.Field(
        default=...,
        description=(
            "Considered variability in the plant performance loss "
            "subcategory element."
        ),
    )
    is_statistically_independent: bool = pdt.Field(
        default=True,
        description=(
            "Whether the plant performance loss subcategory element is "
            "statistically independent of all other elements."
        ),
    )
    results: PlantPerformanceResults = pdt.Field(
        default=...,
        description="Plant performance assessment subcategory element results.",
    )


class PlantPerformanceSubcategoryLabel(StrEnum):
    """Subcategory labels in the plant performance assessment."""

    # Turbine interaction
    INTERNAL_TURBINE_INTERACTION = auto()
    EXTERNAL_TURBINE_INTERACTION = auto()
    FUTURE_TURBINE_INTERACTION = auto()

    # Availability
    TURBINE_AVAILABILITY = auto()
    BOP_AVAILABILITY = auto()
    GRID_AVAILABILITY = auto()

    # Electrical
    ELECTRICAL_EFFICIENCY = auto()
    FACILITY_PARASITIC_CONSUMPTION = auto()

    # Turbine performance
    SUB_OPTIMAL_PERFORMANCE = auto()
    GENERIC_POWER_CURVE_ADJUSTMENT = auto()
    SITE_SPECIFIC_POWER_CURVE_ADJUSTMENT = auto()
    HIGH_WIND_HYSTERESIS = auto()

    # Environmental
    ICING = auto()
    DEGRADATION = auto()
    EXTERNAL_CONDITIONS = auto()
    EXPOSURE_CHANGES = auto()

    # Curtailment
    LOAD_CURTAILMENT = auto()
    GRID_CURTAILMENT = auto()
    ENVIRONMENTAL_CURTAILMENT = auto()
    OPERATIONAL_STRATEGIES = auto()

    # Other
    ASYMMETRIC_EFFECTS = auto()
    UPSIDE_SCENARIOS = auto()
    OTHER = auto()

    @property
    def category(self) -> PlantPerformanceCategoryLabel:
        """The category parent corresponding to the subcategory."""
        match self:
            case PlantPerformanceSubcategoryLabel.INTERNAL_TURBINE_INTERACTION:
                return PlantPerformanceCategoryLabel.TURBINE_INTERACTION
            case PlantPerformanceSubcategoryLabel.EXTERNAL_TURBINE_INTERACTION:
                return PlantPerformanceCategoryLabel.TURBINE_INTERACTION
            case PlantPerformanceSubcategoryLabel.FUTURE_TURBINE_INTERACTION:
                return PlantPerformanceCategoryLabel.TURBINE_INTERACTION
            case PlantPerformanceSubcategoryLabel.TURBINE_AVAILABILITY:
                return PlantPerformanceCategoryLabel.AVAILABILITY
            case PlantPerformanceSubcategoryLabel.BOP_AVAILABILITY:
                return PlantPerformanceCategoryLabel.AVAILABILITY
            case PlantPerformanceSubcategoryLabel.GRID_AVAILABILITY:
                return PlantPerformanceCategoryLabel.AVAILABILITY
            case PlantPerformanceSubcategoryLabel.ELECTRICAL_EFFICIENCY:
                return PlantPerformanceCategoryLabel.ELECTRICAL
            case PlantPerformanceSubcategoryLabel.FACILITY_PARASITIC_CONSUMPTION:
                return PlantPerformanceCategoryLabel.ELECTRICAL
            case PlantPerformanceSubcategoryLabel.SUB_OPTIMAL_PERFORMANCE:
                return PlantPerformanceCategoryLabel.TURBINE_PERFORMANCE
            case PlantPerformanceSubcategoryLabel.GENERIC_POWER_CURVE_ADJUSTMENT:
                return PlantPerformanceCategoryLabel.TURBINE_PERFORMANCE
            case PlantPerformanceSubcategoryLabel.SITE_SPECIFIC_POWER_CURVE_ADJUSTMENT:
                return PlantPerformanceCategoryLabel.TURBINE_PERFORMANCE
            case PlantPerformanceSubcategoryLabel.HIGH_WIND_HYSTERESIS:
                return PlantPerformanceCategoryLabel.TURBINE_PERFORMANCE
            case PlantPerformanceSubcategoryLabel.ICING:
                return PlantPerformanceCategoryLabel.ENVIRONMENTAL
            case PlantPerformanceSubcategoryLabel.DEGRADATION:
                return PlantPerformanceCategoryLabel.ENVIRONMENTAL
            case PlantPerformanceSubcategoryLabel.EXTERNAL_CONDITIONS:
                return PlantPerformanceCategoryLabel.ENVIRONMENTAL
            case PlantPerformanceSubcategoryLabel.EXPOSURE_CHANGES:
                return PlantPerformanceCategoryLabel.ENVIRONMENTAL
            case PlantPerformanceSubcategoryLabel.LOAD_CURTAILMENT:
                return PlantPerformanceCategoryLabel.CURTAILMENT
            case PlantPerformanceSubcategoryLabel.GRID_CURTAILMENT:
                return PlantPerformanceCategoryLabel.CURTAILMENT
            case PlantPerformanceSubcategoryLabel.ENVIRONMENTAL_CURTAILMENT:
                return PlantPerformanceCategoryLabel.CURTAILMENT
            case PlantPerformanceSubcategoryLabel.OPERATIONAL_STRATEGIES:
                return PlantPerformanceCategoryLabel.CURTAILMENT
            case PlantPerformanceSubcategoryLabel.ASYMMETRIC_EFFECTS:
                return PlantPerformanceCategoryLabel.OTHER
            case PlantPerformanceSubcategoryLabel.UPSIDE_SCENARIOS:
                return PlantPerformanceCategoryLabel.OTHER
            case PlantPerformanceSubcategoryLabel.OTHER:
                return PlantPerformanceCategoryLabel.OTHER


class PlantPerformanceSubcategory(EyaDefBaseModel):
    """Plant performance loss assessment subcategory."""

    label: PlantPerformanceSubcategoryLabel = pdt.Field(
        default=...,
        description="Label of the plant performance loss subcategory.",
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the plant performance loss "
            "subcategory, which should not be empty if the field is "
            "included."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the plant performance loss "
            "subcategory, which should not be empty if the field is "
            "included."
        ),
    )
    basis: AssessmentComponentBasis = pdt.Field(
        default=...,
        description=(
            "Basis upon which the plant performance loss subcategory "
            "has been assessed. The basis describes the method and "
            "level of detail of the calculation or assumption used in "
            "the assessment of the subcategory."
        ),
    )
    provenance: AnyAssessmentComponentProvenance = pdt.Field(
        default_factory=get_default_assessment_component_provenance,
        discriminator="assessor_type",
        description=(
            "Provenance of the plant performance loss subcategory "
            "assessment, including specification of the assessor type "
            "(issuing organisation, receiving organisation, "
            "commissioning organisation or other organisation), and if "
            "relevant also the assessor organisation and status of "
            "verification. Where the specification of the provenance "
            "is omitted, it shall be assumed that the assessor is the "
            "issuing organisation(s) of the EYA. Further details can "
            "be included in the description and comment fields of the "
            "plant performance subcategory."
        ),
    )
    variability: TimeVariabilityType = pdt.Field(
        default=...,
        description="Considered variability in the plant performance loss subcategory.",
    )
    elements: Optional[list[PlantPerformanceSubcategoryElement]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional plant performance loss assessment elements that "
            "fall under the subcategory. The element objects include "
            "details and results at the element level. A breakdown of "
            "plant performance loss subcategories into elements is "
            "optional and can be included only for a subset of the "
            "subcategories, as relevant. Whereas the categories and "
            "subcategories are fixed, the user may freely define "
            "element labels."
        ),
    )
    results: PlantPerformanceResults = pdt.Field(
        default=...,
        description="Plant performance assessment subcategory results.",
    )


class PlantPerformanceCategoryLabel(StrEnum):
    """Category labels in the plant performance assessment."""

    TURBINE_INTERACTION = auto()
    AVAILABILITY = auto()
    ELECTRICAL = auto()
    TURBINE_PERFORMANCE = auto()
    ENVIRONMENTAL = auto()
    CURTAILMENT = auto()
    OTHER = auto()


class PlantPerformanceCategory(EyaDefBaseModel):
    """Plant performance loss assessment category."""

    label: PlantPerformanceCategoryLabel = pdt.Field(
        default=...,
        description="Label of the plant performance loss category.",
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the plant performance loss "
            "category, which should not be empty if the field is "
            "included."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the plant performance loss category, "
            "which should not be empty if the field is included."
        ),
    )
    subcategories: list[PlantPerformanceSubcategory] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Plant performance loss assessment subcategories that fall "
            "under the category. The subcategory objects include "
            "details and results at the subcategory level."
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
        min_length=1,
        description="Plant performance loss assessment categories including results.",
    )
    results: PlantPerformanceResults = pdt.Field(
        default=...,
        description="Overall plant performance loss assessment results.",
    )
