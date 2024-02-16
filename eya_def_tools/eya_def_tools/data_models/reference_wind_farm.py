"""Data models relating to reference wind farm specifications.

"""

import datetime as dt
from enum import StrEnum, auto
from typing import Literal, Optional, TypeAlias

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.dataset import BasicStatisticType
from eya_def_tools.data_models.general import (
    Organisation,
    TimeResolution,
    end_date_field,
    start_date_field,
)


class OperationalDataLevel(StrEnum):
    """Level of data from an operational wind farm."""

    # The turbine level is where the data is directly attributable to
    # a specific turbine (e.g. individual turbine SCADA data)
    TURBINE_LEVEL = auto()

    # The wind farm level is where the data is directly attributable to
    # the wind farm as a whole (e.g. energy at a metering point of
    # output for all turbines combined)
    WIND_FARM_LEVEL = auto()

    # Other data levels, where the data is neither directly attributable
    # to a turbine nor to the wind farm (e.g. data from a meteorological
    # measurement station)
    OTHER = auto()


class OperationalDataType(StrEnum):
    """Type of data from an operational wind farm."""

    # Type for all unprocessed datasets comprising a single data source
    SCADA = auto()
    METERED = auto()
    ENVIRONMENTAL_MEASUREMENT = auto()

    # Type for all derived (aggregated and/or processed) datasets such
    # as operational reports and databases with aggregate
    DERIVED = auto()


class OperationalDataSourceType(StrEnum):
    """Type of data source from an operational wind farm."""

    PRIMARY = auto()  # For example primary SCADA data
    SECONDARY = auto()  # For example secondary SCADA data


class OperationalDataVariableType(StrEnum):
    """Type of operational data variable.

    The terms comprise a subset of the ASPECT taxonomy, together with
    some additional terms.
    """

    # From the ASPECT taxonomy:
    ACTIVE_POWER = auto()
    AIR_PRESSURE = auto()
    AIR_TEMPERATURE = auto()
    APPARENT_POWER = auto()
    PITCH_ANGLE = auto()
    RAIN_STATUS = auto()
    RAINFALL_AMOUNT = auto()
    RAINFALL_RATE = auto()
    REACTIVE_POWER = auto()
    RELATIVE_HUMIDITY = auto()
    ROTOR_SPEED = auto()
    ROTOR_STATUS = auto()
    WIND_FROM_DIRECTION = auto()
    WIND_SPEED = auto()
    YAW_ANGLE = auto()

    # Additional terms:
    ALARM_STATUS = auto()
    EVENT_STATUS = auto()
    POWER_LIMITATION = auto()
    ENERGY_OUTPUT = auto()
    AVAILABILITY = auto()
    PRODUCTION_LOSS = auto()
    DATA_AVAILABILITY = auto()


class SingleSourceDatasetClassification(EyaDefBaseModel):
    """Classification of an operational dataset from a single source."""

    data_type: Literal[
        OperationalDataType.SCADA,
        OperationalDataType.METERED,
        OperationalDataType.ENVIRONMENTAL_MEASUREMENT,
    ] = pdt.Field(
        default=...,
        description=(
            "The type of operational data, categorised as 'scada' for "
            "data from a Supervisory Control and Data Acquisition "
            "(SCADA) system, 'metered' for data from a production "
            "meter and 'environmental_measurement' for data from an "
            "(on-site) environmental measurement station such as a "
            "meteorological mast or a remote sensing device (RSD)."
        ),
    )
    data_source_type: OperationalDataSourceType = pdt.Field(
        default=...,
        description=(
            "The type of the operational data source. Primary data, "
            "such as primary SCADA data, comes directly from the "
            "source without any intermediary. Secondary data covers "
            "all other types of data sources, where the data does not "
            "come directly from the source, such as secondary SCADA "
            "data provided in harmonised form by a data management "
            "service provider."
        ),
    )


class DerivedDatasetClassification(EyaDefBaseModel):
    """Classification of a derived operational dataset."""

    data_type: Literal[OperationalDataType.DERIVED] = pdt.Field(
        default=OperationalDataType.DERIVED,
        description=(
            "The type of operational data, categorised as 'derived' "
            "for all derived operational datasets (e.g. operational "
            "reports or databases with aggregate data). Details of "
            "the data type shall be included in the description of "
            "the operational dataset, including the type of derived "
            "dataset (e.g. an operational report), who produced it "
            "(e.g. the turbine OEM) and any relevant details known "
            "about how the data were processed."
        ),
    )
    data_source_type: Literal[OperationalDataSourceType.SECONDARY] = pdt.Field(
        default=OperationalDataSourceType.SECONDARY,
        description="The data source type, which for derived data is 'secondary'.",
    )


DatasetClassification: TypeAlias = (
    SingleSourceDatasetClassification | DerivedDatasetClassification
)


class OperationalDataVariable(EyaDefBaseModel):
    """Reference wind farm operational data variable."""

    variable_type: OperationalDataVariableType = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "The type of operational data variable, selected from the "
            "standardised terms based on the ASPECT taxonomy."
        ),
        examples=["active_power", "wind_speed"],
    )
    label: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional label of the data variable, which should not be "
            "empty if the field is included. This can be used to "
            "provide the label assigned to the variable in the dataset "
            "(e.g. field of column name), but does not need to."
        ),
        examples=["Bld1PitchAngle"],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the data variable, which should "
            "not be empty if the field is included. This may include "
            "clarification of the point of measurement, where relevant."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
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
            "corresponding to or aggregated to the wind farm level "
            "('wind_farm_level') or corresponds to a different "
            "('other') level such as an environmental measurement "
            "station."
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
    time_resolution: Optional[TimeResolution] = pdt.Field(
        default=None,
        description=(
            "Optional specification of the time resolution for the "
            "variable, in case that is different from the dataset main "
            "time resolution."
        ),
    )


class OperationalDatasetMetadata(EyaDefBaseModel):
    """Metadata for a reference wind farm operational dataset."""

    id: str = pdt.Field(
        default=...,
        min_length=1,
        description="Unique ID of the reference operational wind farm dataset",
        examples=[
            "305f27e4-d51e-44dc-a1b1-e54feea36e17",
            "PharaohWindFarmPhIV_OEM_op_reports",
        ],
    )
    label: Optional[str] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Optional label of the reference wind farm dataset, which "
            "should not be empty if the field is included."
        ),
        examples=["OEM operational reports"],
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
    classification: DatasetClassification = pdt.Field(
        default=...,
        discriminator="data_type",
        description=(
            "Classification of the type of data and the type of "
            "data source. Separate schemas are available to classify "
            "unprocessed datasets from a single source, including "
            "classification of the data type and source, and datasets "
            "that have been derived (aggregated and/or processed, "
            "such as operational reports and national databases), "
            "including only a classification of the data type as "
            "'derived'. For single source data types (e.g. SCADA) "
            "it is meaningful to distinguish between primary and "
            "secondary source types, whereas for a derived data "
            "type the source type is always secondary."
        ),
    )
    supplying_organisation: Organisation = pdt.Field(
        default=...,
        description="The organisation that supplied the data.",
    )
    integrity_verification: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of how the integrity of the data has "
            "been and/or can be verified. This field should not be "
            "empty if it is included. If any measures were undertaken "
            "to verify data integrity, they should always be described "
            "here. When this field is omitted, it shall be interpreted "
            "to mean that data integrity verification was not "
            "undertaken and/or not possible."
        ),
    )
    time_resolution: Optional[TimeResolution] = pdt.Field(
        default=None,
        description=(
            "The main time resolution of the operational data, if "
            "relevant. For example, a SCADA dataset with all main "
            "variables at 10-minute resolution should have the time "
            "resolution specified as such, even when some variables "
            "(e.g. alarm status) do not have a meaningful time "
            "resolution. The time resolution can also be specified "
            "at the variable level, in case of deviations from the "
            "dataset main resolution."
        ),
    )
    start_date: dt.date = start_date_field
    end_date: dt.date = end_date_field
    data_variables: list[OperationalDataVariable] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "A list of the data variables included in the dataset and "
            "used in the assessment. For a large dataset (such as a "
            "full wind turbine SCADA dataset) this field should not "
            "include all the variables but only the ones that were "
            "used in the analysis."
        ),
    )


class ReferenceWindFarm(EyaDefBaseModel):
    """Reference wind farm."""

    id: str = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Unique ID for the reference wind farm within the EYA DEF document."
        ),
        examples=["fe1dba61-d6d6-45ef-beb4-ff569660fb14", "PharaohWindFarmPhIV"],
    )
    description: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional description of the reference wind farm, which "
            "should not be empty if the field is included."
        ),
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the reference wind farm, which "
            "should not be empty if the field is included."
        ),
    )
    wind_farm_id: str = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "The ID of the wind farm in the 'wind_farms' section of "
            "the top-level of the EYA DEF document, containing the "
            "configuration data for the reference wind farm."
        ),
    )
    operational_datasets: list[OperationalDatasetMetadata] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "List of metadata documents describing the operational "
            "datasets from the reference wind farm that were used."
        ),
    )
