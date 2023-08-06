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


class MeasurementQuantity(StrEnum):
    """Quantity of a measurement."""

    AIR_DENSITY = auto()
    ANNUAL_ENERGY_PRODUCTION = auto()
    DATA_RECOVERY_RATE = auto()
    DISTANCE = auto()
    EFFICIENCY = auto()
    ENERGY = auto()
    POWER = auto()
    PROBABILITY = auto()
    RELATIVE_ENERGY_UNCERTAINTY = auto()
    RELATIVE_WIND_SPEED_UNCERTAINTY = auto()
    WIND_SHEAR_EXPONENT = auto()
    TEMPERATURE = auto()
    TIME = auto()
    TURBULENCE_INTENSITY = auto()
    WIND_FROM_DIRECTION = auto()
    WIND_SPEED = auto()

    @property
    def measurement_unit(self) -> MeasurementUnit:
        """The measurement unit of the quantity."""
        match self:
            case MeasurementQuantity.AIR_DENSITY:
                return MeasurementUnit.KILOGRAM_PER_CUBIC_METRE
            case MeasurementQuantity.ANNUAL_ENERGY_PRODUCTION:
                return MeasurementUnit.GIGAWATT_HOUR_PER_ANNUM
            case MeasurementQuantity.DATA_RECOVERY_RATE:
                return MeasurementUnit.ONE
            case MeasurementQuantity.DISTANCE:
                return MeasurementUnit.METRE
            case MeasurementQuantity.EFFICIENCY:
                return MeasurementUnit.ONE
            case MeasurementQuantity.ENERGY:
                return MeasurementUnit.GIGAWATT_HOUR
            case MeasurementQuantity.POWER:
                return MeasurementUnit.MEGAWATT
            case MeasurementQuantity.PROBABILITY:
                return MeasurementUnit.ONE
            case MeasurementQuantity.RELATIVE_ENERGY_UNCERTAINTY:
                return MeasurementUnit.ONE
            case MeasurementQuantity.RELATIVE_WIND_SPEED_UNCERTAINTY:
                return MeasurementUnit.ONE
            case MeasurementQuantity.WIND_SHEAR_EXPONENT:
                return MeasurementUnit.ONE
            case MeasurementQuantity.TEMPERATURE:
                return MeasurementUnit.DEGREE_CELSIUS
            case MeasurementQuantity.TIME:
                return MeasurementUnit.HOUR
            case MeasurementQuantity.TURBULENCE_INTENSITY:
                return MeasurementUnit.ONE
            case MeasurementQuantity.WIND_FROM_DIRECTION:
                return MeasurementUnit.DEGREE
            case MeasurementQuantity.WIND_SPEED:
                return MeasurementUnit.METRE_PER_SECOND


class MeasurementUnit(StrEnum):
    """Unit in which a quantity is measured."""

    DEGREE = "degree"
    DEGREE_CELSIUS = "degree_C"
    MEGAWATT = "MW"
    GIGAWATT_HOUR = "GW h"
    GIGAWATT_HOUR_PER_ANNUM = "GW h year-1"
    HOUR = "h"
    KILOGRAM_PER_CUBIC_METRE = "kg m-3"
    METRE = "m"
    METRE_PER_SECOND = "m s-1"
    ONE = "1"  # Applies to all dimensionless quantities


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
    WIND_FROM_DIRECTION = auto()
    WIND_SPEED = auto()
    YEAR = auto()


class StatisticType(StrEnum):
    """Type of statistical measure or parameter reported in a result."""

    MEAN = auto()
    MEDIAN = auto()
    STANDARD_DEVIATION = auto()
    MINIMUM = auto()
    MAXIMUM = auto()
    INTER_ANNUAL_VARIABILITY = auto()
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


class WindFarmRelevance(StrEnum):
    """The relevance of a wind farm in the context of an EYA."""

    INTERNAL = auto()
    EXTERNAL = auto()
    FUTURE = auto()


class WindUncertaintyCategoryLabel(StrEnum):
    """Category labels in the wind uncertainty assessment."""

    HISTORICAL_WIND_RESOURCE = auto()
    EVALUATION_PERIOD_ANNUAL_VARIABILITY = auto()  # Project evaluation period
    MEASUREMENT_UNCERTAINTY = auto()
    HORIZONTAL_EXTRAPOLATION = auto()
    VERTICAL_EXTRAPOLATION = auto()

    # TODO - do we also need an "OTHER" category


class WindUncertaintySubcategoryLabel(StrEnum):
    """Subcategory labels in the wind uncertainty assessment."""

    # Historical wind resource
    LONG_TERM_PERIOD_REPRESENTATIVENESS = auto()
    REFERENCE_DATA_CONSISTENCY = auto()
    LONG_TERM_ADJUSTMENT = auto()
    WIND_SPEED_DISTRIBUTION_UNCERTAINTY = auto()
    ON_SITE_DATA_SYNTHESIS = auto()
    MEASURED_DATA_REPRESENTATIVENESS = auto()

    # Project evaluation period annual variability
    WIND_SPEED_VARIABILITY = auto()
    CLIMATE_CHANGE = auto()
    PLANT_PERFORMANCE = auto()  # TODO clarify distinction to energy uncertainty

    # Measurement uncertainty
    WIND_SPEED_MEASUREMENT = auto()
    WIND_DIRECTION_MEASUREMENT = auto()  # TODO clarify conversion to wind speed
    OTHER_ATMOSPHERIC_PARAMETERS = auto()  # TODO clarify conversion to wind speed
    DATA_INTEGRITY = auto()  # Includes data integrity and documentation

    # Horizontal extrapolation
    MODEL_INPUTS = auto()
    MODEL_SENSITIVITY = auto()  # Covering model stress tests
    MODEL_APPROPRIATENESS = auto()

    # Vertical extrapolation
    MODEL_UNCERTAINTY = auto()
    EXCESS_PROPAGATED_UNCERTAINTY = auto()  # Propagated from measurement uncertainty

    # TODO - do we also need an "OTHER" subcategory

    @property
    def category(self) -> WindUncertaintyCategoryLabel:
        """The category parent corresponding to the subcategory."""
        match self:
            case WindUncertaintySubcategoryLabel.LONG_TERM_PERIOD_REPRESENTATIVENESS:
                return WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE
            case WindUncertaintySubcategoryLabel.REFERENCE_DATA_CONSISTENCY:
                return WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE
            case WindUncertaintySubcategoryLabel.LONG_TERM_ADJUSTMENT:
                return WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE
            case WindUncertaintySubcategoryLabel.WIND_SPEED_DISTRIBUTION_UNCERTAINTY:
                return WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE
            case WindUncertaintySubcategoryLabel.ON_SITE_DATA_SYNTHESIS:
                return WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE
            case WindUncertaintySubcategoryLabel.MEASURED_DATA_REPRESENTATIVENESS:
                return WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE
            case WindUncertaintySubcategoryLabel.WIND_SPEED_VARIABILITY:
                return WindUncertaintyCategoryLabel.EVALUATION_PERIOD_ANNUAL_VARIABILITY
            case WindUncertaintySubcategoryLabel.CLIMATE_CHANGE:
                return WindUncertaintyCategoryLabel.EVALUATION_PERIOD_ANNUAL_VARIABILITY
            case WindUncertaintySubcategoryLabel.PLANT_PERFORMANCE:
                return WindUncertaintyCategoryLabel.EVALUATION_PERIOD_ANNUAL_VARIABILITY
            case WindUncertaintySubcategoryLabel.WIND_SPEED_MEASUREMENT:
                return WindUncertaintyCategoryLabel.MEASUREMENT_UNCERTAINTY
            case WindUncertaintySubcategoryLabel.WIND_DIRECTION_MEASUREMENT:
                return WindUncertaintyCategoryLabel.MEASUREMENT_UNCERTAINTY
            case WindUncertaintySubcategoryLabel.OTHER_ATMOSPHERIC_PARAMETERS:
                return WindUncertaintyCategoryLabel.MEASUREMENT_UNCERTAINTY
            case WindUncertaintySubcategoryLabel.DATA_INTEGRITY:
                return WindUncertaintyCategoryLabel.MEASUREMENT_UNCERTAINTY
            case WindUncertaintySubcategoryLabel.MODEL_INPUTS:
                return WindUncertaintyCategoryLabel.HORIZONTAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.MODEL_SENSITIVITY:
                return WindUncertaintyCategoryLabel.HORIZONTAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.MODEL_APPROPRIATENESS:
                return WindUncertaintyCategoryLabel.HORIZONTAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.MODEL_UNCERTAINTY:
                return WindUncertaintyCategoryLabel.VERTICAL_EXTRAPOLATION
            case WindUncertaintySubcategoryLabel.EXCESS_PROPAGATED_UNCERTAINTY:
                return WindUncertaintyCategoryLabel.VERTICAL_EXTRAPOLATION
