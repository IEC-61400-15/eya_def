"""Data models relating to reference wind farm specifications.

"""

import datetime as dt
from enum import StrEnum, auto
from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.dataset import BasicStatisticType, Dataset
from eya_def_tools.data_models.general import (
    NonEmptyStr,
    Organisation,
    TimeResolution,
    data_period_end_date_field,
    data_period_start_date_field,
)


class OperationalDataLevel(StrEnum):
    """Level of data from an operational wind farm."""

    TURBINE_LEVEL = auto()
    WIND_FARM_LEVEL = auto()
    OTHER = auto()


class ReferenceWindFarmDataVariable(EyaDefBaseModel):
    """Reference wind farm operational data variable."""

    label: NonEmptyStr = pdt.Field(
        default=...,
        description=(
            "Label of the data variable. This is currently free text "
            "but should be replaced by a list of enum options."
        ),
        examples=["active_power", "wind_speed", "energy_output"],
    )
    description: Optional[NonEmptyStr] = pdt.Field(
        default=None,
        description=(
            "Optional description of the data variable, which should "
            "not be empty if the field is included. This may include "
            "clarification of the point of measurement, where relevant."
        ),
    )
    comments: Optional[NonEmptyStr] = pdt.Field(
        default=None,
        description=(
            "Optional comments on the data variable, which should not "
            "be empty if the field is included."
        ),
    )
    data_level: OperationalDataLevel = pdt.Field(
        default=...,
        description=(
            "Whether the operational data variable is provided for "
            "each individual wind turbine ('turbine_level'), is "
            "aggregated at the wind farm level ('wind_farm_level') or "
            "corresponds to a different ('other') unit such as an "
            "environmental measurement station."
        ),
    )
    statistic_types: Optional[list[BasicStatisticType]] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Optional list of the types of statistics included for "
            "the data variable."
        ),
    )
    raw_data_availability: Optional[list[Dataset]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Dimensionless raw data availability (also known as data "
            "recovery rate) for the variable. More than one dataset "
            "may be included if reporting data availability at "
            "different time resolutions or at both wind farm and "
            "turbine level."
        ),
    )


class OperationalDataType(StrEnum):
    """Type of data from an operational wind farm."""

    SCADA = auto()
    METERED = auto()
    ENVIRONMENTAL_MEASUREMENT = auto()

    OTHER = auto()


class OperationalDataSourceType(StrEnum):
    """Type of data source."""

    # TODO these definitions need to be made clearer
    PRIMARY = auto()
    OPERATIONAL_REPORT = auto()
    OTHER_SECONDARY = auto()


class ReferenceWindFarmDataset(EyaDefBaseModel):
    """Reference wind farm operational dataset."""

    label: Optional[NonEmptyStr] = pdt.Field(
        default=...,
        description=(
            "Optional label of the reference wind farm dataset, which "
            "should not be empty if the field is included."
        ),
        examples=["Seasonal distribution of net energy."],
    )
    description: Optional[NonEmptyStr] = pdt.Field(
        default=None,
        description=(
            "Optional description of the dataset, which should not be "
            "empty if the field is included."
        ),
    )
    comments: Optional[NonEmptyStr] = pdt.Field(
        default=None,
        description=(
            "Optional comments on the dataset, which should not be "
            "empty if the field is included."
        ),
    )
    data_supplier_organisation: Organisation = pdt.Field(
        default=...,
        description="The organisation that supplied the data.",
    )
    data_type: OperationalDataType = pdt.Field(
        default=...,
        description=(
            "The type of data in the operational data, categorised as 'scada' for "
            "data from a Supervisory Control and Data Acquisition (SCADA) system, "
            "'metered' for data from a production meter, 'environmental_measurement' "
            "for data from an (on-site) environmental measurement station such as a "
            "meteorological mast or a remote sensing device (RSD) and 'other' for any "
            "other type of unit."
        ),
    )
    data_source_type: OperationalDataSourceType = pdt.Field(
        default=...,
        description=(
            "The type of the operational data source. Primary data, such as primary "
            "SCADA data, comes directly from the source without processing. Report "
            "data refers to data extracted from report document, such as monthly "
            "operational reports. Other secondary data comprises all other data "
            "source categories, such as secondary SCADA data provided in processed "
            "(harmonised) form by a data management service provider."
        ),
    )
    used_data_variables: list[ReferenceWindFarmDataVariable] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "A list of the types of data variables included in this dataset and "
            "used in the assessment. For a large dataset (such as a full wind turbine "
            "SCADA dataset) this field should not include all the variables but only "
            "the ones that were used in the analysis."
        ),
    )
    time_resolution: TimeResolution = pdt.Field(
        default=...,
        description="Time resolution of the operational data.",
    )
    data_period_start_date: dt.date = data_period_start_date_field
    data_period_end_date: dt.date = data_period_end_date_field


class ReferenceWindFarm(EyaDefBaseModel):
    """Reference wind farm."""

    id: NonEmptyStr = pdt.Field(
        default=...,
        description=(
            "Unique ID for the reference wind farm within the EYA DEF document."
        ),
        examples=["fe1dba61-d6d6-45ef-beb4-ff569660fb14", "PharaohWindFarmPhIV"],
    )
    description: Optional[NonEmptyStr] = pdt.Field(
        default=None,
        description=(
            "Optional description of the reference wind farm, which "
            "should not be empty if the field is included."
        ),
    )
    comments: Optional[NonEmptyStr] = pdt.Field(
        default=None,
        description=(
            "Optional comments on the reference wind farm, which "
            "should not be empty if the field is included."
        ),
    )
    wind_farm_id: NonEmptyStr = pdt.Field(
        default=...,
        description=(
            "The ID of the wind farm in the 'wind_farms' section of the top-level "
            "of the EYA DEF document, containing the configuration data for the "
            "reference wind farm."
        ),
    )
    datasets: list[ReferenceWindFarmDataset] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "List of metadata documents describing the operational datasets from "
            "the reference wind farm that were used in the EYA."
        ),
    )
