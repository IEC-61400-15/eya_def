"""Pydantic data models relating to reference wind farm specifications.

"""

import datetime as dt

import pydantic as pdt

from eya_def_tools.data_models.base_models import EyaDefBaseModel
from eya_def_tools.data_models.enums import (
    DataSourceType,
    OperationalDataLevel,
    OperationalDataType,
    TimeResolution,
)
from eya_def_tools.data_models.organisation import Organisation
from eya_def_tools.data_models.wind_farm import WindFarmConfiguration


class ReferenceWindFarmDataset(EyaDefBaseModel):
    """Reference wind farm operational dataset metadata."""

    data_supplier_organisation: Organisation = pdt.Field(
        ...,
        description="The organisation that supplied the data.",
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
    data_level: OperationalDataLevel = pdt.Field(
        ...,
        description=(
            "Whether the operational data is provided for each individual wind "
            "turbine, is aggregated at the wind farm level or corresponds to "
            "a different ('other') unit such as an environmental measurement "
            "station."
        ),
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
    wind_farm_configuration: WindFarmConfiguration = pdt.Field(
        ...,
        description="The configuration data for the reference wind farm.",
    )
    datasets: list[ReferenceWindFarmDataset] = pdt.Field(
        ...,
        description="Metadata for the operational dataset.",
    )


class ReferenceWindFarmBasis(EyaDefBaseModel):
    """Reference wind farm basis in a wind resource assessment."""

    reference_wind_farm_ids: list[str] = pdt.Field(
        ...,
        description=(
            "List of the IDs of all reference wind farms used in the assessment."
        ),
    )
