"""Module for top-level metadata fields for an EYA DEF document.

"""

import datetime as dt
from enum import StrEnum

import pycountry
import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.generic_fields import comments_field, description_field
from eya_def_tools.data_models.report_metadata import Organisation, ReportContributor

Alpha2CountryCode: StrEnum = StrEnum(  # type: ignore
    "Alpha2CountryCode",
    {country.alpha_2: country.alpha_2 for country in pycountry.countries},
)


json_uri_field: str | None = pdt.Field(
    None,
    title="ID",
    description="Unique URI of the JSON document.",
    examples=["https://foo.com/api/eya?id=8f46a815-8b6d-4870-8e92-c031b20320c6.json"],
    alias="$id",
)

title_field: str = pdt.Field(
    ...,
    description="Title of the energy assessment report.",
    examples=["Energy yield assessment of the Barefoot Wind Farm"],
)

project_name_field: str = pdt.Field(
    ...,
    description="Name of the project under assessment.",
    examples=["Barefoot Wind Farm"],
)

project_county_field: Alpha2CountryCode = pdt.Field(
    ...,
    description=(
        "The ISO 3166-1 alpha-2 two-letter country code of the country "
        "where the project under assessment is located."
    ),
)

document_id_field: str | None = pdt.Field(
    None,
    title="Document ID",
    description=(
        "The ID of the report document; not including the version "
        "when 'document_version' is used."
    ),
    examples=["C385945/A/UK/R/002", "0345.923454.0001"],
)

document_version_field: str | None = pdt.Field(
    None,
    description="Version of the report document, also known as revision.",
    examples=["1.2.3", "A", "Rev. A"],
)

issue_date_field: dt.date = pdt.Field(
    ...,
    description=(
        "Report issue date in the ISO 8601 standard format for a "
        "calendar date, i.e. YYYY-MM-DD."
    ),
    examples=["2022-10-05"],
)

contributors_field: list[ReportContributor] = pdt.Field(
    ...,
    description="List of report contributors (e.g. author and verifier)",
)

issuing_organisations_field: list[Organisation] = pdt.Field(
    ...,
    description="The organisation(s) issuing the report (e.g. consultant).",
)

receiving_organisations_field: list[Organisation] | None = pdt.Field(
    None,
    description=(
        "The organisation(s) receiving the report (e.g. client), if relevant."
    ),
)

contract_reference_field: str | None = pdt.Field(
    None,
    description=(
        "Reference to contract between the issuing and receiving "
        "organisations that governs the energy yield assessment."
    ),
    examples=["Contract ID.: P-MIR-00239432-0001-C, dated 2022-11-30"],
)

confidentiality_classification_field: str | None = pdt.Field(
    None,
    description="Confidentiality classification of the report.",
    examples=["Strictly confidential", "Commercial in confidence", "Public"],
)


class EyaDefHeader(EyaDefBaseModel):
    """Collection of top-level metadata fields for an EYA DEF document."""

    json_uri: str | None = json_uri_field
    title: str = title_field
    description: str | None = description_field
    comments: str | None = comments_field
    project_name: str = project_name_field
    project_county: Alpha2CountryCode = project_county_field
    document_id: str | None = document_id_field
    document_version: str | None = document_version_field
    issue_date: dt.date = issue_date_field
    contributors: list[ReportContributor] = contributors_field
    issuing_organisations: list[Organisation] = issuing_organisations_field
    receiving_organisations: list[Organisation] | None = receiving_organisations_field
    contract_reference: str | None = contract_reference_field
    confidentiality_classification: str | None = confidentiality_classification_field
