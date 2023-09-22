"""Data models relating to reference wind farm specifications.

"""

import datetime as dt
from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.enums import (
    DataSourceType,
    OperationalDataLevel,
    OperationalDataType,
    StatisticType,
    TimeResolution,
)
from eya_def_tools.data_models.general_metadata import Organisation
from eya_def_tools.data_models.result import Result


class ReferenceWindFarmDataVariable(EyaDefBaseModel):
    """Reference wind farm operational data variable."""

    label: str = pdt.Field(
        default=...,
        description=(
            "Label of the data variable. This is currently free text but should "
            "be replaced by a list of enum options."
        ),
        examples=["active_power", "wind_speed", "energy_output"],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the data variable.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the data variable.",
    )
    data_level: OperationalDataLevel = pdt.Field(
        default=...,
        description=(
            "Whether the operational data variable is provided for each individual "
            "wind turbine ('turbine_level'), is aggregated at the wind farm level "
            "('wind_farm_level') or corresponds to a different ('other') unit "
            "such as an environmental measurement station."
        ),
    )
    statistic_types: list[StatisticType] = pdt.Field(
        default=...,
        description=(
            "A list of the types of statistics included for this data variable."
        ),
    )
    measurement_point: Optional[str] = pdt.Field(
        default=None,
        description=(
            "Optional clarification of the point of measurement, such as the "
            "location of the energy meter for metered production."
        ),
        examples=[
            "Energy meter at point of common coupling with the grid",
            "Low voltage (LV) side of wind turbine transformer",
        ],
    )
    raw_data_recovery_rate: Optional[list[Result]] = pdt.Field(
        default=None,
        description="Dimensionless raw data recovery rate for the variable.",
    )


class ReferenceWindFarmDataset(EyaDefBaseModel):
    """Reference wind farm operational dataset."""

    label: Optional[str] = pdt.Field(
        default=...,
        description="Label of the reference wind farm dataset.",
        examples=["Seasonal distribution of net energy."],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the dataset.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the dataset.",
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
    data_source_type: DataSourceType = pdt.Field(
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
        description=(
            "A list of the types of data variables included in this dataset and "
            "used in the assessment. For a large dataset (such as a full wind turbine "
            "SCADA dataset) this field should not include all the variables but only "
            "the ones that were used in the analysis."
        ),
    )
    time_resolution: TimeResolution = pdt.Field(
        default=...,
        description="Time resolution of the data.",
    )
    data_period_start_date: dt.date = pdt.Field(
        default=...,
        description=(
            "Start of the data period in the ISO 8601 standard format for a "
            "calendar date, i.e. YYYY-MM-DD."
        ),
        examples=["2015-10-20"],
    )
    data_period_end_date: dt.date = pdt.Field(
        default=...,
        description=(
            "End of the data period in the ISO 8601 standard format for a "
            "calendar date, i.e. YYYY-MM-DD."
        ),
        examples=["2021-11-30"],
    )


class ReferenceWindFarm(EyaDefBaseModel):
    """Reference wind farm."""

    id: str = pdt.Field(
        default=...,
        description=(
            "Unique ID for the reference wind farm within the EYA DEF document."
        ),
        examples=["fe1dba61-d6d6-45ef-beb4-ff569660fb14", "PharaohWindFarmPhIV"],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional description of the reference wind farm.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the reference wind farm.",
    )
    wind_farm_id: str = pdt.Field(
        default=...,
        description=(
            "The ID of the wind farm in the 'wind_farms' section of the top-level "
            "of the EYA DEF document, containing the configuration data for the "
            "reference wind farm."
        ),
    )
    datasets: list[ReferenceWindFarmDataset] = pdt.Field(
        default=...,
        description=(
            "List of metadata documents describing the operational datasets from "
            "the reference wind farm that were used in the EYA."
        ),
    )
