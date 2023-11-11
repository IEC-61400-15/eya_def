"""Data models for representations of datasets within the EYA DEF.

These data models are mainly used for representing results from the wind
resource and energy yield assessment, but can also be used for in other
contexts.

"""

from enum import StrEnum, auto
from typing import Annotated, Optional, TypeAlias

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.general import NonEmptyStr

DatasetValue: TypeAlias = float
DatasetValueCoordinates: TypeAlias = list[int | float | NonEmptyStr]
DatasetValuesWithCoordinates = Annotated[
    list[tuple[DatasetValueCoordinates, DatasetValue]],
    pdt.Field(min_length=1),
]


class BasicStatisticType(StrEnum):
    """Statistic type that can be specified by a single label."""

    SUM = auto()
    MEAN = auto()
    MEDIAN = auto()
    STANDARD_DEVIATION = auto()
    MINIMUM = auto()
    MAXIMUM = auto()
    INTER_ANNUAL_VARIABILITY = auto()


class ExceedanceLevelStatisticType(EyaDefBaseModel):
    """Probability of exceedance level statistic type."""

    exceedance_level: float = pdt.Field(
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

    @property
    def p_value_str(self) -> str:
        return f"P{self.exceedance_level * 100.0:.1f}"


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
    statistic_type: BasicStatisticType | ExceedanceLevelStatisticType = pdt.Field(
        default=...,
        description=(
            "Type of statistic that the component of the dataset "
            "contains. All values must correspond to this statistic."
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


class AssessmentPeriod(StrEnum):
    """Period of or in time that a dataset is applicable."""

    LIFETIME = auto()
    ANY_ONE_YEAR = auto()
    ONE_OPERATIONAL_YEAR = auto()
    OTHER = auto()


class DatasetDimension(StrEnum):
    """Dimension along which dataset values are assigned."""

    HEIGHT = auto()

    HOUR = auto()
    DAY = auto()
    MONTH = auto()
    YEAR = auto()

    MEASUREMENT_ID = auto()
    TURBINE_ID = auto()

    WIND_SPEED = auto()
    WIND_FROM_DIRECTION = auto()


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
        examples=["Seasonal distribution of net energy."],
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
    assessment_period: Optional[AssessmentPeriod] = pdt.Field(
        default=None,
        description=(
            "Optional period of or in time that has been assessed and "
            "for which the dataset is applicable. This field is to be "
            "included only when relevant."
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
            [DatasetDimension.MEASUREMENT_ID, DatasetDimension.HEIGHT],
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
