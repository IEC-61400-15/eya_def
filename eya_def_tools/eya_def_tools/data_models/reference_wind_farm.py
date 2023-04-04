"""Pydantic data models relating to reference wind farm specifications.

"""

import datetime as dt

import pydantic as pdt

from eya_def_tools.data_models.base_models import EyaDefBaseModel
from eya_def_tools.data_models.enums import OperationalDataType, TimeResolution
from eya_def_tools.data_models.organisation import Organisation
from eya_def_tools.data_models.wind_farm import WindFarmConfiguration


class ReferenceWindFarmDataset(EyaDefBaseModel):
    """Reference wind farm operational dataset metadata."""

    data_supplier_organisation: Organisation = pdt.Field(
        ...,
        description="The organisation that supplied the data.",
    )
    data_type: OperationalDataType = pdt.Field(
        ...,
        description=(
            "The type of the operational data. Primary SCADA data refers to data "
            "originating directly from the turbine OEM SCADA system. Secondary SCADA "
            "data is provided by a data management service provider who has processed "
            "the primary SCADA data and often makes it available in a harmonised "
            "format independent of OEM. Metered production refers to quantities "
            "measured by the project revenue meter."
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


class ReferenceWindFarmReference(EyaDefBaseModel):
    """Reference wind farm basis in a wind resource assessment."""

    reference_wind_farm_ids: list[str] = pdt.Field(
        ...,
        description=(
            "List of the IDs of all reference wind farms used in the assessment."
        ),
    )
