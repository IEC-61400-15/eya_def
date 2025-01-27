"""Module for top-level metadata fields for an EYA DEF document.

"""

import datetime as dt
import uuid as uuid_
from enum import StrEnum, auto
from typing import Optional, Type

import pycountry
import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.general import Organisation
from eya_def_tools.data_models.spatial import EpsgSrid
from eya_def_tools.utils import reference_utils

Alpha2CountryCode: Type[StrEnum] = StrEnum(  # type: ignore
    "Alpha2CountryCode",
    {country.alpha_2: country.alpha_2 for country in pycountry.countries},
)


class ReportContributorType(StrEnum):
    """Type of contributor to an EYA report."""

    AUTHOR = auto()
    VERIFIER = auto()
    APPROVER = auto()

    OTHER = auto()


class ReportContributor(EyaDefBaseModel):
    """Contributor to an energy yield assessment."""

    name: str = pdt.Field(
        default=...,
        min_length=1,
        description="Name of the contributor.",
        examples=["Joan Miro", "Andrei Tarkovsky"],
    )
    email_address: Optional[pdt.EmailStr] = pdt.Field(
        default=None,
        description=(
            "Optional email address of the contributor, which should "
            "not be empty if the field is included."
        ),
        examples=["j.miro@art.cat", "andrei.tarkovsky@cinema.com"],
    )
    contributor_type: ReportContributorType = pdt.Field(
        default=...,
        description="Type of contributor.",
    )
    contribution_comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments to clarify contribution, which should "
            "not be empty if the field is included."
        ),
        examples=["Second author"],
    )
    completion_date: Optional[dt.date] = pdt.Field(
        default=None,
        description="Optional contribution completion date (format YYYY-MM-DD).",
        examples=["2022-10-04"],
    )


UriField: Optional[pdt.AnyUrl] = pdt.Field(
    default=None,
    title="URI",
    description=(
        "Optional URI of the EYA DEF JSON document, which should have "
        "the field name '$id' in the JSON document."
    ),
    examples=["https://foo.com/api/eya?id=8f46a815-8b6d-4870-8e92-c031b20320c6.json"],
    alias="$id",
)

SchemaUriField: pdt.AnyUrl = pdt.Field(
    default=reference_utils.get_json_schema_uri(),
    title="EYA DEF JSON Schema URI",
    description=(
        "URI of the EYA DEF JSON Schema, which should have the field "
        "name '$schema' in the JSON document. It is assumed to be the "
        "latest published version if not included."
    ),
    examples=[
        "https://raw.githubusercontent.com/IEC-61400-15/eya_def/"
        "blob/main/iec_61400-15-2_eya_def.schema.json"
    ],
    alias="$schema",
)

UuidField: Optional[uuid_.UUID] = pdt.Field(
    default=None,
    title="UUID",
    description="Optional UUID of the EYA DEF document.",
    examples=["8f46a815-8b6d-4870-8e92-c031b20320c6"],
)

TitleField: str = pdt.Field(
    default=...,
    min_length=1,
    description="Title of the energy yield assessment (EYA) report.",
    examples=["Energy yield assessment of the Barefoot Wind Farm"],
)

DescriptionField: Optional[str] = pdt.Field(
    default=None,
    min_length=1,
    description=(
        "Optional description of the energy yield assessment (EYA) "
        "report, which should not be empty if the field is included."
    ),
    examples=["An updated document to incorporate the latest measurement data."],
)

CommentsField: Optional[str] = pdt.Field(
    default=None,
    min_length=1,
    description=(
        "Optional comments on the energy yield assessment (EYA) "
        "report, which should not be empty if the field is included."
    ),
    examples=[
        "Report labelled as draft. To be finalised following review by all parties."
    ],
)

ProjectNameField: str = pdt.Field(
    default=...,
    min_length=1,
    description="Name of the project under assessment.",
    examples=["Barefoot Wind Farm"],
)

ProjectCountryField: Alpha2CountryCode = pdt.Field(
    default=...,
    description=(
        "The ISO 3166-1 alpha-2 two-letter code of the country where "
        "the project under assessment is located."
    ),
)

DocumentIdField: Optional[str] = pdt.Field(
    default=None,
    min_length=1,
    title="Document ID",
    description=(
        "Optional ID of the report document; not including the version "
        "when 'document_version' is used. This will typically follow "
        "the convention of the document management system of the "
        "issuing organisation(s). The field should not be empty if it "
        "is included."
    ),
    examples=["C385945/A/UK/R/002", "0345.923454.0001"],
)

DocumentVersionField: Optional[str] = pdt.Field(
    default=None,
    min_length=1,
    description=(
        "Optional version of the report document, also known as "
        "revision. As with the 'document_id', this will typically "
        "follow the document versioning convention of the document "
        "management system of the issuing organisation(s). The field "
        "should not be empty if it is included."
    ),
    examples=["1.2.3", "A", "Rev. A"],
)

IssueDateField: dt.date = pdt.Field(
    default=...,
    description=(
        "Report issue date in the ISO 8601 standard format for a "
        "calendar date, i.e. YYYY-MM-DD."
    ),
    examples=["2022-10-05"],
)

ContributorsField: list[ReportContributor] = pdt.Field(
    default=...,
    min_length=1,
    description="List of report contributors (e.g. author and verifier)",
)

IssuingOrganisationsField: list[Organisation] = pdt.Field(
    default=...,
    min_length=1,
    description="The organisation(s) issuing the report (e.g. consultant).",
)

ReceivingOrganisationsField: Optional[list[Organisation]] = pdt.Field(
    default=None,
    min_length=1,
    description=(
        "Optional specification of the organisation(s) receiving the "
        "report (e.g. client), if relevant."
    ),
)

CommissioningOrganisationsField: Optional[list[Organisation]] = pdt.Field(
    default=None,
    min_length=1,
    description=(
        "Optional specification of the organisation(s) having "
        "commissioned the report, if relevant. This is to be included "
        "only if not identical to the receiving  organisation(s). "
        "Whenever receiving organisation(s) are specified and "
        "commissioning organisation(s) are not, is shall be assumed "
        "they are the same. As an example, the commissioning "
        "organisation could be a project developer and the receiving "
        "organisation a financing bank."
    ),
)

ContractReferenceField: Optional[str] = pdt.Field(
    default=None,
    min_length=1,
    description=(
        "Optional reference to contract between the issuing and "
        "receiving organisations that governs the energy yield "
        "assessment (EYA) report document, if relevant. The field "
        "should not be empty if it is included."
    ),
    examples=["Contract ID.: P-MIR-00239432-0001-C, dated 2022-11-30"],
)

ConfidentialityClassificationField: Optional[str] = pdt.Field(
    default=None,
    min_length=1,
    description=(
        "Optional confidentiality classification of the report "
        "document, if relevant. The field should not be empty if it "
        "is included."
    ),
    examples=["Strictly confidential", "Commercial in confidence", "Public"],
)

EpsgSridField: EpsgSrid = pdt.Field(
    default=...,
    description=(
        "EPSG Spatial Reference System Identifier (SRID) for the "
        "Coordinate Reference System (CRS) used for all spatial data "
        "(e.g. turbine locations) in the EYA DEF document. All "
        "location coordinates must be reported in this one CRS, which "
        "must have an EPSG code. If different CRSs are used, the data "
        "must be converted to be consistent with the EPSG code "
        "specified here."
    ),
    examples=[27700, 3006],
)

UtcOffsetField: float = pdt.Field(
    default=...,
    allow_inf_nan=False,
    description=(
        "The offset in hours of the local time zone used for the EYA "
        "relative to Coordinated Universal Time (UTC). It is applied "
        "to UTC time to convert it to local time, hence positive for "
        "time zones ahead of UTC and negative for time zones behind "
        "UTC (e.g. -6.0 for MST and 9.5 for ACST). All data where the "
        "time zone is relevant (e.g. hourly time series and diurnal "
        "profiles) must be consistent with this one UTC offset."
    ),
    examples=[-6.0, 0.0, 1.0, 9.5],
)


class EyaDefHeader(EyaDefBaseModel):
    """Collection of top-level header fields for an EYA DEF document.

    This model is identical to the subset of top-level header (metadata)
    fields defined on the ``EyaDefDocument`` model.
    """

    uri: Optional[pdt.AnyUrl] = UriField
    schema_uri: pdt.AnyUrl = SchemaUriField
    uuid: Optional[uuid_.UUID] = UuidField
    title: str = TitleField
    description: Optional[str] = DescriptionField
    comments: Optional[str] = CommentsField
    project_name: str = ProjectNameField
    project_country: Alpha2CountryCode = ProjectCountryField
    document_id: Optional[str] = DocumentIdField
    document_version: Optional[str] = DocumentVersionField
    issue_date: dt.date = IssueDateField
    contributors: list[ReportContributor] = ContributorsField
    issuing_organisations: list[Organisation] = IssuingOrganisationsField
    receiving_organisations: Optional[list[Organisation]] = ReceivingOrganisationsField
    commissioning_organisations: Optional[list[Organisation]] = (
        CommissioningOrganisationsField
    )
    contract_reference: Optional[str] = ContractReferenceField
    confidentiality_classification: Optional[str] = ConfidentialityClassificationField
    epsg_srid: EpsgSrid = EpsgSridField
    utc_offset: float = UtcOffsetField
