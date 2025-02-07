"""Data models for wind farm and turbine configurations."""

import datetime as dt
from enum import StrEnum, auto

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.spatial import Location


class OperationalRestriction(EyaDefBaseModel):
    """Specifications of a restriction that limits power output.

    In the current draft of the schema, 'label', 'description' and
    'comments' fields are available to describe the restriction with
    free text. This is intended to be expanded into a more comprehensive
    data model.
    """

    label: str = pdt.Field(
        default=...,
        min_length=1,
        description="Short label to indicate the type of operational restriction.",
        examples=["WSM curtailment", "MEC curtailment"],
    )
    description: str = pdt.Field(
        default=...,
        min_length=1,
        description="Description of the operational restriction.",
    )
    comments: str | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the operational restriction, which should not be empty if the field is included."
        ),
    )
    start_datetime: dt.datetime | None = pdt.Field(
        default=None,
        description=(
            "Optional operational restriction start datetime in the "
            "ISO 8601 standard format with the 'T' required between "
            "the calendar date and time, i.e. YYYY-MM-DDThh:mm:ss. In "
            "cases where the time is not relevant (i.e. only the date "
            "is relevant), hours, minutes and seconds shall all be set "
            "to zero. If using the time part, the timezone of the data "
            "must be consistent with the UTC offset specified for the "
            "EYA DEF document."
        ),
        examples=["2023-11-24T05:02:00", "2023-11-01T00:00:00"],
    )
    end_datetime: dt.datetime | None = pdt.Field(
        default=None,
        description=(
            "Optional operational restriction end datetime in the "
            "ISO 8601 standard format with the 'T' required between "
            "the calendar date and time, i.e. YYYY-MM-DDThh:mm:ss. In "
            "cases where the time is not relevant (i.e. only the date "
            "is relevant), hours, minutes and seconds shall all be set "
            "to zero. If using the time part, the timezone of the data "
            "must be consistent with the UTC offset specified for the "
            "EYA DEF document."
        ),
        examples=["2024-12-24T23:15:00", "2024-12-31T00:00:00"],
    )


class TurbineConfiguration(EyaDefBaseModel):
    """Specification of all details for a turbine configuration."""

    id: str = pdt.Field(
        default=...,
        min_length=1,
        description="Unique identifier of the turbine.",
        examples=["b55caeac-f152-4b13-8217-3fddeab792cf", "T1-scenario-1"],
    )
    label: str | None = pdt.Field(
        default=None,
        min_length=1,
        description="Label of the turbine, if different from the 'id'.",
        examples=["T1", "WTG02", "WEA_003"],
    )
    description: str | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the turbine, which should not be empty if the field is included."
        ),
    )
    comments: str | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the turbine, which should not be empty if the field is included."
        ),
    )
    location: Location = pdt.Field(
        default=...,
        description="The horizontal spatial location of the turbine.",
    )
    ground_level_altitude: float = pdt.Field(
        default=...,
        allow_inf_nan=False,
        description="The ground level altitude (base elevation) of the turbine (in m).",
    )
    hub_height: float = pdt.Field(
        default=...,
        allow_inf_nan=False,
        description="The hub height of the turbine above ground level (in m).",
    )
    turbine_model: str = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "The unique identifier for the model of the turbine, which "
            "should correspond to the value of the field 'model_name' "
            "under 'turbine' in the IEC 61400-16 Power Curve Schema."
        ),
        examples=["GT 3.45-117", "XYZ/200/20MW"],
    )
    baseline_operating_mode: str = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "The unique identifier for the baseline operating mode of "
            "the turbine (the operating mode used in the calculation "
            "of gross energy yield), which should correspond to the "
            "value of the field 'label' under 'power_curves' and "
            "'operating_modes' in the IEC 61400-16 Power Curve Schema."
        ),
        examples=["standard", "PO1", "N/14"],
    )

    assessment_period_start_date: dt.date | None = pdt.Field(
        default=None,
        description=(
            "Optional assessment period start date of the individual "
            "turbine in the ISO 8601 standard format for a calendar "
            "date, i.e. YYYY-MM-DD."
        ),
        examples=["2026-01-01", "2017-04-01"],
    )
    assessment_period_end_date: dt.date | None = pdt.Field(
        default=None,
        description=(
            "Optional assessment period end date of the individual "
            "turbine in the ISO 8601 standard format for a calendar "
            "date, i.e. YYYY-MM-DD."
        ),
        examples=["2051-03-31", "2025-12-31"],
    )
    restrictions: list[OperationalRestriction] | None = pdt.Field(
        default=None,
        min_length=1,
        description="List of operational restrictions at the turbine level.",
    )


class WindFarmRelevance(StrEnum):
    """The relevance of a wind farm in the context of an EYA."""

    INTERNAL = auto()
    EXTERNAL = auto()
    FUTURE = auto()


class WindFarmConfiguration(EyaDefBaseModel):
    """A collection of wind turbines considered as one unit (plant)."""

    id: str = pdt.Field(
        default=...,
        min_length=1,
        description="Unique identifier of the wind farm.",
        examples=["8994452f-731b-4342-9418-571920e44484"],
    )
    label: str = pdt.Field(
        default=...,
        min_length=1,
        description="Label or name of the wind farm.",
        examples=["Barefoot Wind Farm", "Project Summit Phase III"],
    )
    abbreviation: str | None = pdt.Field(
        default=None,
        min_length=1,
        description="Optional abbreviated label of the wind farm.",
        examples=["BWF", "Summit PhIII"],
    )
    description: str | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the wind farm, which should not be empty if the field is included."
        ),
    )
    comments: str | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the wind farm, which should not be empty if the field is included."
        ),
    )
    turbines: list[TurbineConfiguration] = pdt.Field(
        default=...,
        min_length=1,
        description="List of specifications for constituent turbines.",
    )
    relevance: WindFarmRelevance = pdt.Field(
        default=...,
        description=(
            "The relevance of the wind farm for the assessment ('internal', 'external' or 'future')."
        ),
    )
    assessment_period_start_date: dt.date = pdt.Field(
        default=...,
        description=(
            "The assessment period start date of the wind farm in "
            "the ISO 8601 standard format for a calendar date, i.e. "
            "YYYY-MM-DD."
        ),
        examples=["2026-01-01", "2017-04-01"],
    )
    assessment_period_end_date: dt.date = pdt.Field(
        default=...,
        description=(
            "The assessment period end date of the wind farm in the "
            "ISO 8601 standard format for a calendar date, i.e. "
            "YYYY-MM-DD."
        ),
        examples=["2051-03-31", "2025-12-31"],
    )
    installed_capacity: pdt.PositiveFloat = pdt.Field(
        default=...,
        description=(
            "The maximum production (in MW) of the wind farm under "
            "typical conditions. If there are features in place to "
            "increase power output beyond the stated nameplate power "
            "of the turbines (e.g. so-called power boost solutions), "
            "the wind farm installed capacity should correspond to "
            "that increased power, insofar as it is reached under "
            "typical conditions and not only in rare exceptions."
        ),
        examples=[12.3, 2345.67],
    )
    export_capacity: pdt.PositiveFloat | None = pdt.Field(
        default=None,
        description=(
            "Optional specification of the maximum permanently "
            "transmittable power (in MW) from the wind farm at the "
            "grid connection, or equivalent, if known. If not included "
            "it shall be assumed that the wind farm can transmit the "
            "full produced output."
        ),
        examples=[11.3, 2332.0],
    )
    restrictions: list[OperationalRestriction] | None = pdt.Field(
        default=None,
        min_length=1,
        description="List of operational restrictions at the wind farm level.",
    )

    @property
    def capacity(self) -> float:
        """The wind farm capacity (in MW).

        The capacity is the lesser of the ``installed_capacity`` (the
        maximum permanently transmittable power at the grid connection
        or equivalent) and the ``export_capacity`` (the maximum
        production under typical conditions).
        """
        return (
            min(self.installed_capacity, self.export_capacity)
            if self.export_capacity is not None
            else self.installed_capacity
        )

    @property
    def assessment_period_length(self) -> float:
        """The length of the operational lifetime in years."""
        return (
            self.assessment_period_end_date - self.assessment_period_start_date
        ).total_seconds() / (60.0 * 60.0 * 24.0 * 365.24)
