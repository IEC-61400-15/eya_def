"""Enum class definitions for the EYA DEF data model.

"""

from enum import StrEnum, auto


class PlantPerformanceCategoryLabel(StrEnum):
    """Category labels in the plant performance assessment."""

    TURBINE_INTERACTION = auto()
    AVAILABILITY = auto()
    ELECTRICAL = auto()
    TURBINE_PERFORMANCE = auto()
    ENVIRONMENTAL = auto()
    CURTAILMENT = auto()
    OTHER = auto()


class ComponentAssessmentBasis(StrEnum):
    """Basis of plant performance assessment component."""

    TIMESERIES_CALCULATION = auto()
    DISTRIBUTION_CALCULATION = auto()
    OTHER_CALCULATION = auto()
    PROJECT_SPECIFIC_ESTIMATE = auto()
    REGIONAL_ASSUMPTION = auto()
    GENERIC_ASSUMPTION = auto()
    NOT_CONSIDERED = auto()
    OTHER = auto()


class ComponentVariabilityType(StrEnum):
    """Variability type of plant performance assessment component."""

    STATIC_PROCESS = auto()
    ANNUAL_VARIABLE = auto()
    OTHER = auto()


class ResultsApplicabilityType(StrEnum):
    """Period of or in time that a set of results are applicable."""

    LIFETIME = auto()
    ANY_ONE_YEAR = auto()
    ONE_OPERATIONAL_YEAR = auto()
    OTHER = auto()


class UncertaintyCategoryLabel(StrEnum):
    """Category labels in the wind resource uncertainty assessment."""

    MEASUREMENT = auto()
    HISTORICAL = auto()
    VERTICAL = auto()
    HORIZONTAL = auto()
    OTHER = auto()
