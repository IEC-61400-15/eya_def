"""General type and class definitions for the EYA DEF schema."""

from __future__ import annotations

import datetime
from enum import StrEnum, auto
from typing import Annotated, Literal, TypeAlias

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel

NonEmptyStr = Annotated[str, pdt.StringConstraints(min_length=1)]


StartDateField: datetime.date = pdt.Field(
    default=...,
    description=(
        "Start of the data period in the ISO 8601 standard format for a calendar date, i.e. YYYY-MM-DD."
    ),
    examples=["2015-10-20"],
)

EndDateField: datetime.date = pdt.Field(
    default=...,
    description=(
        "End of the data period in the ISO 8601 standard format for a calendar date, i.e. YYYY-MM-DD."
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
    abbreviation: str | None = pdt.Field(
        default=None,
        min_length=1,
        description="Abbreviated name of the organisation.",
        examples=["Torre Egger", "Miranda"],
    )
    address: str | None = pdt.Field(
        default=None,
        min_length=1,
        description="Address of the organisation.",
        examples=["5 Munro Road, Summit Centre, Sgurrsville, G12 0YE, UK"],
    )
    contact_name: str | None = pdt.Field(
        default=None,
        min_length=1,
        description="Name(s) of contact person(s) in the organisation.",
        examples=["Luis Bunuel", "Miles Davis, John Coltrane"],
    )


AssessmentComponentBasis = Literal[
    "time_series_calculation",
    "distribution_calculation",
    "other_calculation",
    "project_specific_assumption",
    "regional_assumption",
    "generic assumption",
    "not_considered",
]


AssessorType = Literal[
    "issuing_organisation",
    "receiving_organisation",
    "commissioning_organisation",
    "other_organisation",
]

IsVerifiedByIssuingOrganisationField: bool = pdt.Field(
    default=...,
    description=(
        "Whether an assessment component provided by a receiving "
        "organisation, commissioning organisation or other "
        "organisation (e.g. independent third party) has been verified "
        "by the issuing organisation(s) of the EYA."
    ),
)


class IssuingOrganisationAssessmentComponentProvenance(EyaDefBaseModel):
    """Provenance of a component assessed by the issuing organisation."""

    assessor_type: Literal["issuing_organisation"] = pdt.Field(
        default="issuing_organisation",
        description=(
            "Type of organisation that undertook the assessment of the "
            "EYA or WRA component, which must be one of the options "
            "'issuing_organisation', 'receiving_organisation', "
            "'commissioning_organisation' and 'other_organisation'. "
            "The value 'issuing_organisation' means that the component "
            "has been assessed by the organisation(s) having "
            "undertaken and issued the EYA."
        ),
    )


class FirstPartyAssessmentComponentProvenance(EyaDefBaseModel):
    """First party provenance of an EYA or WRA component.

    First party in this context means an organisation receiving and/or
    having commissioned the EYA report.
    """

    assessor_type: Literal["receiving_organisation", "commissioning_organisation"] = (
        pdt.Field(
            default="receiving_organisation",
            description=(
                "Type of organisation that undertook the assessment of the "
                "EYA or WRA component, which must be one of the options "
                "'issuing_organisation', 'receiving_organisation', "
                "'commissioning_organisation' and 'other_organisation'. "
                "The value 'commissioning_organisation' should be used "
                "only when the commissioning organisation is not also a "
                "receiving organisation."
            ),
        )
    )
    is_verified_by_issuing_organisation: bool = IsVerifiedByIssuingOrganisationField


class OtherOrganisationAssessmentComponentProvenance(EyaDefBaseModel):
    """Provenance of a component assessed by another organisation."""

    assessor_type: Literal["other_organisation"] = pdt.Field(
        default="other_organisation",
        description=(
            "Type of organisation that undertook the assessment of the "
            "EYA or WRA component, which must be one of the options "
            "'issuing_organisation', 'receiving_organisation', "
            "'commissioning_organisation' and 'other_organisation'. "
            "The value 'other_organisation' should be used for "
            "independent third parties or any other organisation that "
            "has not issued, received or commissioned the EYA."
        ),
    )
    assessor_organisations: list[Organisation] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Specification of the other (third party) organisation(s) that undertook the assessment of the component."
        ),
    )
    is_verified_by_issuing_organisation: bool = IsVerifiedByIssuingOrganisationField


AnyAssessmentComponentProvenance: TypeAlias = (
    IssuingOrganisationAssessmentComponentProvenance
    | FirstPartyAssessmentComponentProvenance
    | OtherOrganisationAssessmentComponentProvenance
)


def get_default_assessment_component_provenance() -> (
    IssuingOrganisationAssessmentComponentProvenance
):
    return IssuingOrganisationAssessmentComponentProvenance()


class MeasurementQuantity(StrEnum):
    """Quantity of a measurement."""

    AIR_DENSITY = auto()
    AMBIENT_TURBULENCE_INTENSITY = auto()
    ANNUAL_ENERGY_PRODUCTION = auto()
    DATA_AVAILABILITY = auto()
    DISPLACEMENT_HEIGHT = auto()
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
    WIND_FROM_DIRECTION = auto()
    WIND_SPEED = auto()

    @property
    def measurement_unit(self) -> MeasurementUnit:
        """The measurement unit of the quantity."""
        match self:
            case MeasurementQuantity.AIR_DENSITY:
                return MeasurementUnit.KILOGRAM_PER_CUBIC_METRE
            case MeasurementQuantity.AMBIENT_TURBULENCE_INTENSITY:
                return MeasurementUnit.ONE
            case MeasurementQuantity.ANNUAL_ENERGY_PRODUCTION:
                return MeasurementUnit.GIGAWATT_HOUR_PER_ANNUM
            case MeasurementQuantity.DATA_AVAILABILITY:
                return MeasurementUnit.ONE
            case MeasurementQuantity.DISPLACEMENT_HEIGHT:
                return MeasurementUnit.METRE
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
        allow_inf_nan=False,
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
            "The measurement unit of time in which the time resolution is specified."
        ),
    )


class TimeVariabilityType(StrEnum):
    """Type of time variability considered for an assessment element."""

    STATIC = auto()
    VARIABLE = auto()
