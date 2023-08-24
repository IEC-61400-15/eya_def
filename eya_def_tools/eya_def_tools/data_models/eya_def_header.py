"""Module for top-level metadata fields for an EYA DEF document.

"""

import datetime as dt
import uuid as uuid_
from enum import StrEnum
from typing import Optional, Type

import pycountry
import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.general_metadata import Organisation, ReportContributor
from eya_def_tools.utils import reference_utils

Alpha2CountryCode: Type[StrEnum] = StrEnum(  # type: ignore
    "Alpha2CountryCode",
    {country.alpha_2: country.alpha_2 for country in pycountry.countries},
)


uri_field: Optional[pdt.AnyUrl] = pdt.Field(
    default=None,
    title="URI",
    description=(
        "URI of the EYA DEF JSON document, which should have the field "
        "name '$id' in the JSON document."
    ),
    examples=["https://foo.com/api/eya?id=8f46a815-8b6d-4870-8e92-c031b20320c6.json"],
    alias="$id",
)

schema_uri_field: pdt.AnyUrl = pdt.Field(
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

uuid_field: Optional[uuid_.UUID] = pdt.Field(
    default=None,
    title="UUID",
    description="UUID of the EYA DEF JSON document.",
    examples=["8f46a815-8b6d-4870-8e92-c031b20320c6"],
)

title_field: str = pdt.Field(
    default=...,
    min_length=1,  # Value should not be empty
    description="Title of the energy yield assessment (EYA) report.",
    examples=["Energy yield assessment of the Barefoot Wind Farm"],
)

description_field: Optional[str] = pdt.Field(
    default=None,
    min_length=1,  # Value should not be empty if the field is included
    description="Optional description of the energy yield assessment (EYA) report.",
    examples=["An updated document to incorporate the latest measurement data."],
)

comments_field: Optional[str] = pdt.Field(
    default=None,
    min_length=1,  # Value should not be empty if the field is included
    description="Optional comments on the energy yield assessment (EYA) report.",
    examples=[
        "Report labelled as draft. To be finalised following review by all parties."
    ],
)

project_name_field: str = pdt.Field(
    default=...,
    min_length=1,  # Value should not be empty
    description="Name of the project under assessment.",
    examples=["Barefoot Wind Farm"],
)

project_country_field: Alpha2CountryCode = pdt.Field(
    default=...,
    description=(
        "The ISO 3166-1 alpha-2 two-letter code of the country where "
        "the project under assessment is located."
    ),
)

document_id_field: Optional[str] = pdt.Field(
    default=None,
    min_length=1,  # Value should not be empty if the field is included
    title="Document ID",
    description=(
        "The ID of the report document; not including the version "
        "when 'document_version' is used. This will typically follow "
        "the convention of the document management system of the "
        "issuing organisation(s)."
    ),
    examples=["C385945/A/UK/R/002", "0345.923454.0001"],
)

document_version_field: Optional[str] = pdt.Field(
    default=None,
    min_length=1,  # Value should not be empty if the field is included
    description=(
        "Version of the report document, also known as revision. As "
        "with the 'document_id', this will typically follow the "
        "document versioning convention of the document management "
        "system of the issuing organisation(s)."
    ),
    examples=["1.2.3", "A", "Rev. A"],
)

issue_date_field: dt.date = pdt.Field(
    default=...,
    description=(
        "Report issue date in the ISO 8601 standard format for a "
        "calendar date, i.e. YYYY-MM-DD."
    ),
    examples=["2022-10-05"],
)

contributors_field: list[ReportContributor] = pdt.Field(
    default=...,
    description="List of report contributors (e.g. author and verifier)",
)

issuing_organisations_field: list[Organisation] = pdt.Field(
    default=...,
    description="The organisation(s) issuing the report (e.g. consultant).",
)

receiving_organisations_field: Optional[list[Organisation]] = pdt.Field(
    default=None,
    description=(
        "The organisation(s) receiving the report (e.g. client), if relevant."
    ),
)

contract_reference_field: Optional[str] = pdt.Field(
    default=None,
    description=(
        "Reference to contract between the issuing and receiving "
        "organisations that governs the energy yield assessment "
        "(EYA) report document, if relevant."
    ),
    examples=["Contract ID.: P-MIR-00239432-0001-C, dated 2022-11-30"],
)

confidentiality_classification_field: Optional[str] = pdt.Field(
    default=None,
    description="Confidentiality classification of the report document, if relevant.",
    examples=["Strictly confidential", "Commercial in confidence", "Public"],
)

epsg_srid_field: int = pdt.Field(
    default=...,
    description=(
        "EPSG Spatial Reference System Identifier (SRID) for the "
        "Coordinate Reference System (CRS) used for all spatial data "
        "(e.g. turbine locations) in the EYA DEF JSON document. All "
        "location coordinates must be reported in the same CRS, which "
        "must be one that has an EPSG code. If different CRSs are used "
        "the data must be converted to be consistent with the EPSG "
        "code specified here."
    ),
    examples=[27700, 3006],
)


class EyaDefHeader(EyaDefBaseModel):
    """Collection of top-level header fields for an EYA DEF document.

    This model is identical to the subset of top-level header (metadata)
    fields defined on the ``EyaDefDocument`` model.
    """

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
