"""General type and class definitions for the EYA DEF schema.

"""

from __future__ import annotations

from enum import StrEnum, auto
from typing import Annotated, Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel

NonEmptyStr = Annotated[str, pdt.Field(min_length=1)]


start_date_field = pdt.Field(
    default=...,
    description=(
        "Start of the data period in the ISO 8601 standard format for a "
        "calendar date, i.e. YYYY-MM-DD."
    ),
    examples=["2015-10-20"],
)

end_date_field = pdt.Field(
    default=...,
    description=(
        "End of the data period in the ISO 8601 standard format for a "
        "calendar date, i.e. YYYY-MM-DD."
    ),
    examples=["2021-11-30"],
)


class Organisation(EyaDefBaseModel):
    """Basic metadata to describe an organisation.

    This model is for example used for issuing and receiving
    organisations of an energy yield assessment.
    """

    name: str = pdt.Field(
        default=...,
        min_length=1,
        description="Entity name of the organisation.",
        examples=["The Torre Egger Consultants Limited", "Miranda Investments Limited"],
    )
    abbreviation: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description="Abbreviated name of the organisation.",
        examples=["Torre Egger", "Miranda"],
    )
    address: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description="Address of the organisation.",
        examples=["5 Munro Road, Summit Centre, Sgurrsville, G12 0YE, UK"],
    )
    contact_name: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description="Name(s) of contact person(s) in the organisation.",
        examples=["Luis Bunuel", "Miles Davis, John Coltrane"],
    )


class AssessmentBasis(StrEnum):
    """Basis on which an EYA or WRA component has been assessed."""

    TIME_SERIES_CALCULATION = auto()
    DISTRIBUTION_CALCULATION = auto()
    OTHER_CALCULATION = auto()
    PROJECT_SPECIFIC_ASSUMPTION = auto()
    REGIONAL_ASSUMPTION = auto()
    GENERIC_ASSUMPTION = auto()
    NOT_CONSIDERED = auto()


class MeasurementQuantity(StrEnum):
    """Quantity of a measurement."""

    AIR_DENSITY = auto()
    ANNUAL_ENERGY_PRODUCTION = auto()
    DATA_AVAILABILITY = auto()
    DISTANCE = auto()
    EFFICIENCY = auto()
    ENERGY = auto()
    POWER = auto()
    PROBABILITY = auto()
    RELATIVE_ENERGY_UNCERTAINTY = auto()
    RELATIVE_WIND_SPEED_UNCERTAINTY = auto()
    ROTOR_SPEED = auto()
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
            case MeasurementQuantity.DATA_AVAILABILITY:
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
            case MeasurementQuantity.ROTOR_SPEED:
                return MeasurementUnit.RPM
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
    """Standard unit in which a quantity is measured."""

    DEGREE = auto()
    DEGREE_CELSIUS = "degree_C"
    GIGAWATT_HOUR = "GW h"
    GIGAWATT_HOUR_PER_ANNUM = "GW h year-1"
    HOUR = "h"
    KILOGRAM_PER_CUBIC_METRE = "kg m-3"
    MEGAWATT = "MW"
    METRE = "m"
    METRE_PER_SECOND = "m s-1"
    ONE = "1"  # Applies to all dimensionless quantities
    RPM = auto()


class TimeMeasurementUnit(StrEnum):
    """Unit in which time is measured where several units are supported.

    The standard unit for reporting the quantity of time within the EYA
    DEF is hours. The different time measurement units are used for
    example to describe the time resolution of meteorological reference
    input data.
    """

    YEAR = auto()
    MONTH = auto()
    DAY = auto()
    HOUR = auto()
    MINUTE = auto()
    SECOND = auto()


class TimeResolution(EyaDefBaseModel):
    """Resolution of time series data."""

    value: float = pdt.Field(
        default=...,
        description=(
            "The value of the time resolution in the specified unit. "
            "For example, for 10-minute resolution, the value is "
            "'10.0' and the unit is 'minute'"
        ),
        examples=[0.5, 1.0, 10.0],
    )
    unit: TimeMeasurementUnit = pdt.Field(
        default=...,
        description=(
            "The measurement unit of time in which the time resolution " "is specified."
        ),
    )


class TimeVariabilityType(StrEnum):
    """Type of time variability considered for an assessment element."""

    STATIC_PROCESS = auto()
    ANNUAL_VARIABLE = auto()

    OTHER = auto()
