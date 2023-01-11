"""Enum class definitions for the EYA DEF data model.

"""

from __future__ import annotations

from enum import StrEnum, auto


class PlantPerformanceCategoryLabel(StrEnum):
    """Category labels in the plant performance assessment."""

    WAKES = auto()
    BLOCKAGE = auto()
    AVAILABILITY = auto()
    ELECTRICAL = auto()
    TURBINE_PERFORMANCE = auto()
    ENVIRONMENTAL = auto()
    CURTAILMENT = auto()
    OTHER = auto()

    def is_turbine_interaction(self) -> bool:
        """Whether the label enum corresponds to turbine interaction.

        See also ``turbine_interaction_category_labels``.
        """
        if self in self.turbine_interaction_category_labels():
            return True
        else:
            return False

    @classmethod
    def turbine_interaction_category_labels(
        cls,
    ) -> tuple[PlantPerformanceCategoryLabel, ...]:
        """Get the label enums that correspond to turbine interaction.

        Turbine interaction is a 'super-category' that includes both
        wakes and blockage.
        """
        return cls.WAKES, cls.BLOCKAGE


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


class WindFarmRelevance(StrEnum):
    """The relevance of a wind farm in the context of an EYA."""

    INTERNAL = auto()
    EXTERNAL = auto()
    FUTURE = auto()
