"""Enum class definitions for the EYA DEF schema.

"""

from __future__ import annotations

from enum import StrEnum, auto


class AssessmentBasis(StrEnum):
    """Basis on which an EYA or WRA component has been assessed."""

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


class DataSourceType(StrEnum):
    """Type of data source."""

    PRIMARY = auto()
    REPORT = auto()
    OTHER_SECONDARY = auto()


class MeasurementUnit(StrEnum):
    """Unit in which a quantity is measured."""

    DIMENSIONLESS = "1"
    KILOWATT = "kW"
    MEGAWATT_HOUR = "MW h"
    MEGAWATT_HOUR_PER_ANNUM = "MW h year-1"
    METRE_PER_SECOND = "m s-1"


class OperationalDataLevel(StrEnum):
    """Level of data from an operational wind farm."""

    TURBINE_LEVEL = auto()
    WIND_FARM_LEVEL = auto()
    OTHER = auto()


class OperationalDataType(StrEnum):
    """Type of data from an operational wind farm."""

    ENVIRONMENTAL_MEASUREMENT = auto()
    METERED = auto()
    SCADA = auto()
    OTHER = auto()


class PlantPerformanceCategoryLabel(StrEnum):
    """Category labels in the plant performance assessment."""

    TURBINE_INTERACTION = auto()
    AVAILABILITY = auto()
    ELECTRICAL = auto()
    TURBINE_PERFORMANCE = auto()
    ENVIRONMENTAL = auto()
    CURTAILMENT = auto()
    OTHER = auto()


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

    @classmethod
    def subcategory_to_category_map(
        cls,
    ) -> dict[PlantPerformanceSubcategoryLabel, PlantPerformanceCategoryLabel]:
        """Dictionary mapping each subcategory to the parent category."""
        return {
            PlantPerformanceSubcategoryLabel.INTERNAL_TURBINE_INTERACTION: (
                PlantPerformanceCategoryLabel.TURBINE_INTERACTION
            ),
            PlantPerformanceSubcategoryLabel.EXTERNAL_TURBINE_INTERACTION: (
                PlantPerformanceCategoryLabel.TURBINE_INTERACTION
            ),
            PlantPerformanceSubcategoryLabel.FUTURE_TURBINE_INTERACTION: (
                PlantPerformanceCategoryLabel.TURBINE_INTERACTION
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
            PlantPerformanceSubcategoryLabel.ASYMMETRIC_EFFECTS: (
                PlantPerformanceCategoryLabel.OTHER
            ),
            PlantPerformanceSubcategoryLabel.UPSIDE_SCENARIOS: (
                PlantPerformanceCategoryLabel.OTHER
            ),
            PlantPerformanceSubcategoryLabel.OTHER: (
                PlantPerformanceCategoryLabel.OTHER
            ),
        }

    @property
    def category(self) -> PlantPerformanceCategoryLabel:
        """Get the category corresponding to the component.

        :return: The ``PlantPerformanceCategoryLabel`` that the
            component label belongs to.
        """
        return self.subcategory_to_category_map()[self]


class ReportContributorType(StrEnum):
    """Type of contributor to an EYA report."""

    AUTHOR = auto()
    VERIFIER = auto()
    APPROVER = auto()

    OTHER = auto()


class ResultsDimension(StrEnum):
    """Dimension along which results are assigned."""

    HEIGHT = auto()
    HOUR = auto()
    MEASUREMENT = auto()
    MONTH = auto()
    TURBINE = auto()
    YEAR = auto()


class ResultsQuantity(StrEnum):
    """Quantity of a set of results."""

    AIR_DENSITY = auto()
    DATA_RECOVERY_RATE = auto()
    DISTANCE = auto()
    ENERGY = auto()
    POWER = auto()
    POWER_LAW_WIND_SHEAR_EXPONENT = auto()
    TEMPERATURE = auto()
    TIME = auto()
    WIND_FROM_DIRECTION = auto()
    WIND_SPEED = auto()

    @classmethod
    def results_quantity_to_unit_map(cls) -> dict[ResultsQuantity, MeasurementUnit]:
        return {}

    @property
    def measurement_unit(self) -> MeasurementUnit:
        """The measurement unit of the quantity."""
        return self.results_quantity_to_unit_map()[self]


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


class TimeVariabilityType(StrEnum):
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


class WindResourceAssessmentStepType(StrEnum):
    """Type of step in a wind resource assessment.

    The scope of this enum is limited to the assessment of wind resource
    at the measurement locations and therefore does not cover the
    horizontal extrapolation.
    """

    DATA_FILTERING = auto()
    TURBINE_INTERACTION_CORRECTION = auto()
    MEASUREMENT_STRUCTURE_RELATED_CORRECTION = auto()
    TERRAIN_RELATED_CORRECTION = auto()
    ONSITE_DATA_SYNTHESIS = auto()
    LONG_TERM_PREDICTION = auto()
    VERTICAL_EXTRAPOLATION = auto()
    MODEL_CALIBRATION = auto()

    OTHER = auto()
