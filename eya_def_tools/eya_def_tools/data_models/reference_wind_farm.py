"""Pydantic data models relating to reference wind farm specifications.

"""

import datetime as dt

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.enums import (
    DataSourceType,
    OperationalDataLevel,
    OperationalDataType,
    StatisticType,
    TimeResolution,
)
from eya_def_tools.data_models.generic_fields import comments_field, description_field
from eya_def_tools.data_models.report_metadata import Organisation
from eya_def_tools.data_models.result import Result
from eya_def_tools.data_models.wind_farm import WindFarmConfiguration


class ReferenceWindFarmDataVariable(EyaDefBaseModel):
    """Reference wind farm operational data variable metadata."""

    label: str = pdt.Field(
        ...,
        description=(
            "Label of the data variable. This is currently free text but should "
            "be replaced by a list of enum options."
        ),
        examples=["active_power", "wind_speed", "energy_output"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    data_level: OperationalDataLevel = pdt.Field(
        ...,
        description=(
            "Whether the operational data variable is provided for each individual "
            "wind turbine ('turbine_level'), is aggregated at the wind farm level "
            "('wind_farm_level') or corresponds to a different ('other') unit "
            "such as an environmental measurement station."
        ),
    )
    statistic_types: list[StatisticType] = pdt.Field(
        ...,
        description=(
            "A list of the types of statistics included for this data variable."
        ),
    )
    measurement_point: str | None = pdt.Field(
        None,
        description=(
            "Optional clarification of the point of measurement, such as the "
            "location of the energy meter for metered production."
        ),
        examples=[
            "Energy meter at point of common coupling with the grid",
            "Low voltage (LV) side of wind turbine transformer",
        ],
    )
    raw_data_recovery_rate: list[Result] | None = pdt.Field(
        None,
        description="Dimensionless raw data recovery rate for the variable.",
    )


class ReferenceWindFarmDataset(EyaDefBaseModel):
    """Reference wind farm operational dataset metadata."""

    label: str | None = pdt.Field(
        ...,
        description="Label of the reference wind farm dataset.",
        examples=["Seasonal distribution of net energy."],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    data_supplier_organisation: Organisation = pdt.Field(
        ...,
        description="The organisation that supplied the data.",
    )
    data_type: OperationalDataType = pdt.Field(
        ...,
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
        ...,
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
        ...,
        description=(
            "A list of the types of data variables included in this dataset and "
            "used in the assessment. For a large dataset (such as a full wind turbine "
            "SCADA dataset) this field should not include all the variables but only "
            "the ones that were used in the analysis."
        ),
    )
    time_resolution: TimeResolution = pdt.Field(
        ...,
        description="Time resolution of the data.",
    )
    data_period_start_date: dt.date = pdt.Field(
        ...,
        description=(
            "Start of the data period in the ISO 8601 standard format for a "
            "calendar date, i.e. YYYY-MM-DD."
        ),
        examples=["2015-10-20"],
    )
    data_period_end_date: dt.date = pdt.Field(
        ...,
        description=(
            "End of the data period in the ISO 8601 standard format for a "
            "calendar date, i.e. YYYY-MM-DD."
        ),
        examples=["2021-11-30"],
    )


class ReferenceWindFarm(EyaDefBaseModel):
    """Reference wind farm metadata."""

    reference_wind_farm_id: str = pdt.Field(
        ...,
        description=(
            "Unique ID for the reference wind farm within the EYA DEF document."
        ),
        examples=["fe1dba61-d6d6-45ef-beb4-ff569660fb14", "PharaohWindFarmPhIV"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    wind_farm_configuration: WindFarmConfiguration = pdt.Field(
        ...,
        description="The configuration data for the reference wind farm.",
    )
    datasets: list[ReferenceWindFarmDataset] = pdt.Field(
        ...,
        description="Metadata for the operational dataset.",
    )
