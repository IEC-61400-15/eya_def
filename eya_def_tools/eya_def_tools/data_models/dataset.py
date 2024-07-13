"""Data models for representations of datasets within the EYA DEF.

These data models are mainly used for representing results from the wind
resource and energy yield assessment, but can also be used for in other
contexts.

"""

import datetime
from enum import StrEnum, auto
from typing import Annotated, Literal, Optional, TypeAlias

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.general import NonEmptyStr

DatasetValue: TypeAlias = float

DatasetValueCoordinates: TypeAlias = list[int | float | NonEmptyStr]

DatasetValuesWithCoordinates = Annotated[
    list[tuple[DatasetValueCoordinates, DatasetValue]],
    pdt.Field(min_length=1),
]


class StatisticType(StrEnum):
    """Type of statistic using standardised label."""

    # Simple statistic types with no further required parameters
    SUM = auto()
    MEAN = auto()
    MEDIAN = auto()
    STANDARD_DEVIATION = auto()
    MINIMUM = auto()
    MAXIMUM = auto()
    INTER_ANNUAL_VARIABILITY = auto()
    SAMPLE_COUNT = auto()

    # Statistic types that require further parameters
    EXCEEDANCE_LEVEL = auto()


SimpleStatisticType: TypeAlias = Literal[
    StatisticType.SUM,
    StatisticType.MEAN,
    StatisticType.MEDIAN,
    StatisticType.STANDARD_DEVIATION,
    StatisticType.MINIMUM,
    StatisticType.MAXIMUM,
    StatisticType.INTER_ANNUAL_VARIABILITY,
    StatisticType.SAMPLE_COUNT,
]


TimeFrameStartDateField: Optional[datetime.date] = pdt.Field(
    default=None,
    description=(
        "Optional specification of the start date of the time frame "
        "(period) to which the statistic applies. When not specified, "
        "it shall be assumed that the time frame start date is the "
        "start of the full period of the relevant context (e.g. the "
        "full assessment period). The time frame can for example be "
        "used to specify that a certain uncertainty standard deviation "
        "value applies from the second through the tenth year of wind "
        "farm operation."
    ),
)

TimeFrameEndDateField: Optional[datetime.date] = pdt.Field(
    default=None,
    description=(
        "Optional specification of the end date of the time frame "
        "(period) to which the statistic applies. When not specified, "
        "it shall be assumed that the time frame end date is the "
        "end of the full period of the relevant context (e.g. the "
        "full assessment period)."
    ),
)

ReturnPeriodField: Optional[pdt.PositiveFloat] = pdt.Field(
    default=None,
    description=(
        "Optional specification of the return period in years, to be "
        "included when relevant to the statistic in question. It may "
        "for example specify a 1-year or 10-year return period for a "
        "the standard deviation of an uncertainty distribution or "
        "certain probability of exceedance level."
    ),
    examples=[1.0, 10.0],
)


class SimpleStatistic(EyaDefBaseModel):
    """Specification of a statistic that only requires type definition."""

    statistic_type: SimpleStatisticType = pdt.Field(
        default=...,
        description=(
            "Specification of the type of statistic, using the "
            "standardised naming conventions."
        ),
    )
    time_frame_start_date: Optional[datetime.date] = TimeFrameStartDateField
    time_frame_end_date: Optional[datetime.date] = TimeFrameEndDateField
    return_period: Optional[pdt.PositiveFloat] = ReturnPeriodField


class ExceedanceLevelStatistic(EyaDefBaseModel):
    """Specification of a probability of exceedance level statistic."""

    statistic_type: Literal[StatisticType.EXCEEDANCE_LEVEL] = pdt.Field(
        default=StatisticType.EXCEEDANCE_LEVEL,
        description=(
            "Specification of the type of statistic, using the "
            "standardised naming conventions. For an exceedance level "
            "statistic, the type must always be 'exceedance_level'."
        ),
    )
    probability: float = pdt.Field(
        default=...,
        ge=0.0,
        le=1.0,
        allow_inf_nan=False,
        description=(
            "The dimensionless probability of exceedance level (i.e. "
            "probability value between 0.0 and 1.0) of the statistic."
        ),
        examples=[0.25, 0.75, 0.9, 0.99],
    )
    time_frame_start_date: Optional[datetime.date] = TimeFrameStartDateField
    time_frame_end_date: Optional[datetime.date] = TimeFrameEndDateField
    return_period: Optional[pdt.PositiveFloat] = ReturnPeriodField

    @property
    def p_value_str(self) -> str:
        return f"P{self.probability * 100.0:.1f}"


AnyStatisticType: TypeAlias = SimpleStatistic | ExceedanceLevelStatistic


class DatasetStatistic(EyaDefBaseModel):
    """Dataset values for one specific statistic type."""

    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the dataset statistic, which "
            "should not be empty if the field is included."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the dataset statistic, which should "
            "not be empty if the field is included."
        ),
    )
    statistic: AnyStatisticType = pdt.Field(
        default=...,
        discriminator="statistic_type",
        description=(
            "Specification of the statistic that the element of the "
            "dataset corresponds to."
        ),
    )
    values: float | DatasetValuesWithCoordinates = pdt.Field(
        default=...,
        description=(
            "Dataset value(s) as a single number or one or more "
            "values at coordinates. If more than one value is included "
            "the values must be represented together with coordinates. "
            "A single value can be included either with or without "
            "coordinates. The coordinates must correspond to and be "
            "listed the same order as the dimensions specified for the "
            "dataset."
        ),
    )


class DatasetDimension(StrEnum):
    """Dimension along which dataset values are assigned."""

    MINUTE = auto()
    HOUR = auto()
    DAY = auto()
    MONTH = auto()
    YEAR = auto()

    WIND_SPEED = auto()
    WIND_FROM_DIRECTION = auto()

    WIND_DATASET_ID = auto()  # Measurement station or reference dataset
    POINT_ID = auto()  # Measurement point
    HEIGHT = auto()  # Measurement height or turbine hub height

    WIND_FARM_ID = auto()
    TURBINE_ID = auto()

    OPERATIONAL_DATASET_ID = auto()  # E.g. 10-minute SCADA

    VARIABLE_ID = auto()  # Measurement or operational data variable


class Dataset(EyaDefBaseModel):
    """Collection of labelled data for one specific quantity.

    The data is labelled by specifying dimensions and including
    coordinates along the dimensions for each data value.
    """

    label: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional label of the dataset, which should not be empty "
            "if the field is included."
        ),
        examples=["Seasonal distribution of net energy"],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the dataset, which should not be "
            "empty if the field is included."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the dataset, which should not be "
            "empty if the field is included."
        ),
    )
    dimensions: Optional[list[DatasetDimension]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Dimensions along which the dataset is binned. All "
            "statistics within the same dataset object must have the "
            "same dimensions. The dimensions must correspond to and be "
            "listed in the same order as the coordinates for the "
            "values of all statistics. A dataset without dimensions "
            "can only have a single value for each statistic."
        ),
        examples=[
            [DatasetDimension.TURBINE_ID, DatasetDimension.YEAR],
            [DatasetDimension.WIND_DATASET_ID, DatasetDimension.HEIGHT],
        ],
    )
    statistics: list[DatasetStatistic] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "List of dataset statistic objects that each include data "
            "values for a specific statistic type. For example, there "
            "may be two statistics, one for mean values and one for "
            "standard deviation values."
        ),
    )
