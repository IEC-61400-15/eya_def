"""Top level pydantic data model for the IEC 61400-15-2 EYA DEF."""

import datetime as dt
import uuid as uuid_

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.eya_def_header import (
    Alpha2CountryCode,
    CommentsField,
    CommissioningOrganisationsField,
    ConfidentialityClassificationField,
    ContractReferenceField,
    ContributorsField,
    DescriptionField,
    DocumentIdField,
    DocumentVersionField,
    EpsgSridField,
    IssueDateField,
    IssuingOrganisationsField,
    ProjectCountryField,
    ProjectNameField,
    ReceivingOrganisationsField,
    ReportContributor,
    SchemaUriField,
    TitleField,
    UriField,
    UtcOffsetField,
    UuidField,
)
from eya_def_tools.data_models.general import Organisation
from eya_def_tools.data_models.iea43_wra_data_model import WraDataModelDocument
from eya_def_tools.data_models.power_curve_schema import PowerCurveDocument
from eya_def_tools.data_models.reference_wind_farm import ReferenceWindFarm
from eya_def_tools.data_models.scenario import Scenario
from eya_def_tools.data_models.spatial import EpsgSrid
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

    uri: pdt.AnyUrl | None = UriField
    schema_uri: pdt.AnyUrl = SchemaUriField
    uuid: uuid_.UUID | None = UuidField
    title: str = TitleField
    description: str | None = DescriptionField
    comments: str | None = CommentsField
    project_name: str = ProjectNameField
    project_country: Alpha2CountryCode = ProjectCountryField
    document_id: str | None = DocumentIdField
    document_version: str | None = DocumentVersionField
    issue_date: dt.date = IssueDateField
    contributors: list[ReportContributor] = ContributorsField
    issuing_organisations: list[Organisation] = IssuingOrganisationsField
    receiving_organisations: list[Organisation] | None = ReceivingOrganisationsField
    commissioning_organisations: list[Organisation] | None = (
        CommissioningOrganisationsField
    )
    contract_reference: str | None = ContractReferenceField
    confidentiality_classification: str | None = ConfidentialityClassificationField
    epsg_srid: EpsgSrid = EpsgSridField
    utc_offset: float = UtcOffsetField
    wind_farms: list[WindFarmConfiguration] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "List of all wind farms considered in the EYA. This should "
            "comprise internal, external and future wind farms, "
            "including those used as reference wind farms in the wind "
            "resource assessment, if any. If different configurations "
            "are assessed for one or more internal and/or future wind "
            "farms in different scenarios, a wind farm object must be "
            "completed for each unique configuration, with the "
            "relevant configurations for each scenario referenced by "
            "wind farm ID."
        ),
    )
    measurement_stations: list[WraDataModelDocument] | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional list of measurement station metadata documents "
            "according to the IEA Wind Task 43 WRA Data Model, "
            "including all measurement stations relevant to the EYA, "
            "if any. It is recommended that one metadata document be "
            "completed for each measurement station, although the WRA "
            "Data Model allows for grouping multiple measurement "
            "stations into a single document."
        ),
    )
    reference_wind_farms: list[ReferenceWindFarm] | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional list of metadata documents for the reference "
            "operational wind farms relevant to the EYA, if any. One "
            "metadata document shall be completed for each relevant "
            "reference operational wind farm."
        ),
    )
    reference_meteorological_datasets: list[WraDataModelDocument] | None = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional list of metadata documents that describe the "
            "reference meteorological datasets used in the long-term "
            "prediction process of the EYA and/or used as input wind "
            "resource data for calibration against reference "
            "operational data. Reference datasets may include "
            "ground-based meteorological (met) stations, reanalysis "
            "datasets and mesoscale model datasets. The IEA Wind Task "
            "43 WRA Data Model schema shall be used. One metadata "
            "document shall be completed for each relevant reference "
            "meteorological dataset."
        ),
    )
    wind_resource_assessments: list[WindResourceAssessment] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "List of wind resource assessments, including results, at "
            "the measurement station locations."
        ),
    )
    power_curves: list[PowerCurveDocument] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "List of documents specifying power curves and associated "
            "information according to the IEC 61400-16 Power Curve "
            "Schema, covering all relevant turbine models."
        ),
    )
    scenarios: list[Scenario] = pdt.Field(
        default=...,
        min_length=1,
        description="List of energy yield assessment scenarios.",
    )
