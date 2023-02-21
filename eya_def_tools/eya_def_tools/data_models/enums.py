"""Enum class definitions for the EYA DEF schema.

"""

from __future__ import annotations

from enum import StrEnum, auto


class AssessmentBasis(StrEnum):
    """Basis on which a component has been assessed."""

    TIMESERIES_CALCULATION = auto()
    DISTRIBUTION_CALCULATION = auto()
    OTHER_CALCULATION = auto()
    PROJECT_SPECIFIC_ESTIMATE = auto()
    REGIONAL_ASSUMPTION = auto()
    GENERIC_ASSUMPTION = auto()
    NOT_CONSIDERED = auto()
    OTHER = auto()


class AssessmentPeriod(StrEnum):
    """Period of or in time that a set of results are applicable."""

    LIFETIME = auto()
    ANY_ONE_YEAR = auto()
    ONE_OPERATIONAL_YEAR = auto()
    OTHER = auto()


class MeasurementUnit(StrEnum):
    """Unit in which a quantity is measured."""

    DIMENSIONLESS = "1"
    KILOWATT = "kW"
    MEGAWATT_HOUR = "MW h"
    MEGAWATT_HOUR_PER_ANNUM = "MW h year-1"
    METRE_PER_SECOND = "m s-1"


class OperationalDataType(StrEnum):
    """Type of data from an operational wind farm."""

    PRIMARY_SCADA = auto()
    SECONDARY_SCADA = auto()
    METERED_PRODUCTION = auto()


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


class PlantPerformanceSubcategoryLabel(StrEnum):
    """Subcategory labels in the plant performance assessment."""

    # Wakes
    INTERNAL_WAKES = auto()
    EXTERNAL_WAKES = auto()
    FUTURE_WAKES = auto()

    # Blockage
    INTERNAL_BLOCKAGE = auto()
    EXTERNAL_BLOCKAGE = auto()
    FUTURE_BLOCKAGE = auto()

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
    OTHER = auto()

    def category(self) -> PlantPerformanceCategoryLabel:
        """Get the category corresponding to the component.

        :return: The ``PlantPerformanceCategoryLabel`` that the
            component label belongs to.
        """
        component_to_category_map: dict[
            PlantPerformanceSubcategoryLabel, PlantPerformanceCategoryLabel
        ] = {
            PlantPerformanceSubcategoryLabel.INTERNAL_WAKES: (
                PlantPerformanceCategoryLabel.WAKES
            ),
            PlantPerformanceSubcategoryLabel.EXTERNAL_WAKES: (
                PlantPerformanceCategoryLabel.WAKES
            ),
            PlantPerformanceSubcategoryLabel.FUTURE_WAKES: (
                PlantPerformanceCategoryLabel.WAKES
            ),
            PlantPerformanceSubcategoryLabel.INTERNAL_BLOCKAGE: (
                PlantPerformanceCategoryLabel.BLOCKAGE
            ),
            PlantPerformanceSubcategoryLabel.EXTERNAL_BLOCKAGE: (
                PlantPerformanceCategoryLabel.BLOCKAGE
            ),
            PlantPerformanceSubcategoryLabel.FUTURE_BLOCKAGE: (
                PlantPerformanceCategoryLabel.BLOCKAGE
            ),
            PlantPerformanceSubcategoryLabel.TURBINE_AVAILABILITY: (
                PlantPerformanceCategoryLabel.AVAILABILITY
            ),
            PlantPerformanceSubcategoryLabel.BOP_AVAILABILITY: (
                PlantPerformanceCategoryLabel.AVAILABILITY
            ),
            PlantPerformanceSubcategoryLabel.GRID_AVAILABILITY: (
                PlantPerformanceCategoryLabel.AVAILABILITY
            ),
            PlantPerformanceSubcategoryLabel.ELECTRICAL_EFFICIENCY: (
                PlantPerformanceCategoryLabel.ELECTRICAL
            ),
            PlantPerformanceSubcategoryLabel.FACILITY_PARASITIC_CONSUMPTION: (
                PlantPerformanceCategoryLabel.ELECTRICAL
            ),
            PlantPerformanceSubcategoryLabel.SUB_OPTIMAL_PERFORMANCE: (
                PlantPerformanceCategoryLabel.TURBINE_PERFORMANCE
            ),
            PlantPerformanceSubcategoryLabel.GENERIC_POWER_CURVE_ADJUSTMENT: (
                PlantPerformanceCategoryLabel.TURBINE_PERFORMANCE
            ),
            PlantPerformanceSubcategoryLabel.SITE_SPECIFIC_POWER_CURVE_ADJUSTMENT: (
                PlantPerformanceCategoryLabel.TURBINE_PERFORMANCE
            ),
            PlantPerformanceSubcategoryLabel.HIGH_WIND_HYSTERESIS: (
                PlantPerformanceCategoryLabel.TURBINE_PERFORMANCE
            ),
            PlantPerformanceSubcategoryLabel.ICING: (
                PlantPerformanceCategoryLabel.ENVIRONMENTAL
            ),
            PlantPerformanceSubcategoryLabel.DEGRADATION: (
                PlantPerformanceCategoryLabel.ENVIRONMENTAL
            ),
            PlantPerformanceSubcategoryLabel.EXTERNAL_CONDITIONS: (
                PlantPerformanceCategoryLabel.ENVIRONMENTAL
            ),
            PlantPerformanceSubcategoryLabel.EXPOSURE_CHANGES: (
                PlantPerformanceCategoryLabel.ENVIRONMENTAL
            ),
            PlantPerformanceSubcategoryLabel.LOAD_CURTAILMENT: (
                PlantPerformanceCategoryLabel.CURTAILMENT
            ),
            PlantPerformanceSubcategoryLabel.GRID_CURTAILMENT: (
                PlantPerformanceCategoryLabel.CURTAILMENT
            ),
            PlantPerformanceSubcategoryLabel.ENVIRONMENTAL_CURTAILMENT: (
                PlantPerformanceCategoryLabel.CURTAILMENT
            ),
            PlantPerformanceSubcategoryLabel.OPERATIONAL_STRATEGIES: (
                PlantPerformanceCategoryLabel.CURTAILMENT
            ),
            PlantPerformanceSubcategoryLabel.OTHER: PlantPerformanceCategoryLabel.OTHER,
        }
        return component_to_category_map[self]


class ResultsDimension(StrEnum):
    """Dimension along which results are assigned."""

    HEIGHT = auto()
    HOUR = auto()
    MEASUREMENT = auto()
    MONTH = auto()
    TURBINE = auto()
    YEAR = auto()


class StatisticType(StrEnum):
    """Type of statistical measure or parameter reported in a result."""

    MEAN = auto()
    MEDIAN = auto()
    STANDARD_DEVIATION = auto()
    MINIMUM = auto()
    MAXIMUM = auto()
    P10 = auto()
    P25 = auto()
    P75 = auto()
    P90 = auto()
    P99 = auto()


class TimeResolution(StrEnum):
    """Resolution of time series data."""

    TEN_MINUTELY = "10-minutely"
    HOURLY = auto()
    DAILY = auto()
    MONTHLY = auto()


class VariabilityType(StrEnum):
    """Type of time variability considered for an assessment element."""

    STATIC_PROCESS = auto()
    ANNUAL_VARIABLE = auto()
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
