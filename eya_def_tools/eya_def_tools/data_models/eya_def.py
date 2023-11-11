"""Top level pydantic data model for the IEC 61400-15-2 EYA DEF.

"""

import datetime as dt
import uuid as uuid_
from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.eya_def_header import (
    Alpha2CountryCode,
    ReportContributor,
    comments_field,
    confidentiality_classification_field,
    contract_reference_field,
    contributors_field,
    description_field,
    document_id_field,
    document_version_field,
    epsg_srid_field,
    issue_date_field,
    issuing_organisations_field,
    project_country_field,
    project_name_field,
    receiving_organisations_field,
    schema_uri_field,
    title_field,
    uri_field,
    uuid_field,
)
from eya_def_tools.data_models.general import Organisation
from eya_def_tools.data_models.measurement_station import MeasurementStationMetadata
from eya_def_tools.data_models.reference_met_data import ReferenceMeteorologicalDataset
from eya_def_tools.data_models.reference_wind_farm import ReferenceWindFarm
from eya_def_tools.data_models.scenario import Scenario
from eya_def_tools.data_models.turbine_model import TurbineModelSpecifications
from eya_def_tools.data_models.wind_farm import WindFarmConfiguration
from eya_def_tools.data_models.wind_resource import WindResourceAssessment
from eya_def_tools.utils import reference_utils


class EyaDefDocument(EyaDefBaseModel):
    """IEC 61400-15-2 EYA DEF top-level data model."""

    model_config = pdt.ConfigDict(
        # The model config ``extra="allow"`` is equivalent of the JSON
        # Schema specification ``"additionalProperties": true``, which
        # is used only at the top level to allow further metadata fields
        extra="allow",
        # As a default, infinity of nan float values are not permitted
        allow_inf_nan=False,
        json_schema_extra={
            "$id": reference_utils.get_json_schema_uri().unicode_string(),
            "$version": reference_utils.get_json_schema_version(),
            "title": "IEC 61400-15-2 EYA DEF Schema",
        },
    )

    uri: Optional[pdt.AnyUrl] = uri_field
    schema_uri: pdt.AnyUrl = schema_uri_field
    uuid: Optional[uuid_.UUID] = uuid_field
    title: str = title_field
    description: Optional[str] = description_field
    comments: Optional[str] = comments_field
    project_name: str = project_name_field
    project_country: Alpha2CountryCode = project_country_field
    document_id: Optional[str] = document_id_field
    document_version: Optional[str] = document_version_field
    issue_date: dt.date = issue_date_field
    contributors: list[ReportContributor] = contributors_field
    issuing_organisations: list[Organisation] = issuing_organisations_field
    receiving_organisations: Optional[
        list[Organisation]
    ] = receiving_organisations_field
    contract_reference: Optional[str] = contract_reference_field
    confidentiality_classification: Optional[str] = confidentiality_classification_field
    epsg_srid: int = epsg_srid_field
    wind_farms: list[WindFarmConfiguration] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "List of all wind farms considered in the EYA. This should comprise "
            "internal, external and future wind farms, including those used as "
            "reference wind farms in the wind resource assessment, if any. If "
            "different configurations are assessed for one or more internal "
            "and/or future wind farms in different scenarios, a wind farm object "
            "must be completed for each unique configuration, with the relevant "
            "configurations for each scenario referenced by wind farm ID."
        ),
    )
    measurement_stations: Optional[list[MeasurementStationMetadata]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "List of measurement station metadata documents according to the IEA "
            "Wind Task 43 WRA Data Model, including all measurement stations "
            "relevant to the EYA, if any. It is recommended that one metadata "
            "document be completed for each measurement station, although the "
            "WRA Data Model allows for grouping multiple measurement stations "
            "into a single document."
        ),
    )
    reference_wind_farms: Optional[list[ReferenceWindFarm]] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "List of metadata documents for the reference operational wind farms "
            "relevant to the EYA, if any. One metadata document shall be completed "
            "for each relevant reference operational wind farm."
        ),
    )
    reference_meteorological_datasets: Optional[
        list[ReferenceMeteorologicalDataset | MeasurementStationMetadata]
    ] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "List of metadata documents for reference meteorological datasets "
            "used in the long-term prediction process of the EYA, which may "
            "include details of for example ground-based meteorological stations, "
            "reanalysis datasets and mesoscale model datasets used as long-term"
            "references."
        ),
    )
    wind_resource_assessments: list[WindResourceAssessment] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "List of wind resource assessments, including results, at the "
            "measurement station locations."
        ),
    )
    turbine_models: Optional[list[TurbineModelSpecifications]] = pdt.Field(
        default=None,
        min_length=1,
        description="List of wind turbine model specifications.",
    )
    scenarios: list[Scenario] = pdt.Field(
        default=...,
        min_length=1,
        description="List of energy yield assessment scenarios.",
    )
