"""Pydantic data models for report metadata.

"""

import datetime as dt
from typing import Literal

import pydantic as pdt

from eya_def_tools.data_models.base_models import EyaDefBaseModel
from eya_def_tools.data_models.fields import comments_field, description_field
from eya_def_tools.data_models.spatial import CoordinateReferenceSystem


class ReportContributor(EyaDefBaseModel):
    """Contributor to an energy yield assessment."""

    name: str = pdt.Field(
        ...,
        description="Name of the contributor.",
        examples=["Joan Miro", "Andrei Tarkovsky"],
    )
    email_address: pdt.EmailStr | None = pdt.Field(
        None,
        description="Email address of the contributor.",
        examples=["j.miro@art.cat", "andrei.tarkovsky@cinema.com"],
    )
    contributor_type: Literal["author", "verifier", "approver", "other"] = pdt.Field(
        ..., description="Type of contributor."
    )
    contribution_comments: str | None = pdt.Field(
        None,
        description="Comments to clarify contribution.",
        examples=["Second author"],
    )
    completion_date: dt.date | None = pdt.Field(
        None,
        description="Contribution completion date (format YYYY-MM-DD).",
        examples=["2022-10-04"],
    )


class Organisation(EyaDefBaseModel):
    """Issuing or receiving organisation of an energy yield assessment."""

    name: str = pdt.Field(
        ...,
        description="Entity name of the organisation.",
        examples=["The Torre Egger Consultants Limited", "Miranda Investments Limited"],
    )
    abbreviation: str | None = pdt.Field(
        None,
        description="Abbreviated name of the organisation.",
        examples=["Torre Egger", "Miranda"],
    )
    address: str | None = pdt.Field(
        None,
        description="Address of the organisation.",
        examples=["5 Munro Road, Summit Centre, Sgurrsville, G12 0YE, UK"],
    )
    contact_name: str | None = pdt.Field(
        None,
        description="Name(s) of contact person(s) in the organisation.",
        examples=["Luis Bunuel", "Miles Davis, John Coltrane"],
    )


class ReportMetadata(EyaDefBaseModel):
    """Collection of metadata fields for an EYA report."""

    title: str = pdt.Field(
        ...,
        description="Title of the energy assessment report.",
        examples=["Energy yield assessment of the Barefoot Wind Farm"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    project_name: str = pdt.Field(
        ...,
        description="Name of the project under assessment.",
        examples=["Barefoot Wind Farm"],
    )
    document_id: str | None = pdt.Field(
        None,
        title="Document ID",
        description=(
            "The ID of the report document; not including the version "
            "when 'document_version' is used."
        ),
        examples=["C385945/A/UK/R/002", "0345.923454.0001"],
    )
    document_version: str | None = pdt.Field(
        None,
        description="Version of the report document, also known as revision.",
        examples=["1.2.3", "A", "Rev. A"],
    )
    issue_date: dt.date = pdt.Field(
        ...,
        description=(
            "Report issue date in the ISO 8601 standard format for a "
            "calendar date, i.e. YYYY-MM-DD."
        ),
        examples=["2022-10-05"],
    )
    contributors: list[ReportContributor] = pdt.Field(
        ...,
        description="List of report contributors (e.g. author and verifier)",
    )
    issuing_organisations: list[Organisation] = pdt.Field(
        ...,
        description="The organisation(s) issuing the report (e.g. consultant).",
    )
    receiving_organisations: list[Organisation] | None = pdt.Field(
        None,
        description=(
            "The organisation(s) receiving the report (e.g. client), if relevant."
        ),
    )
    contract_reference: str | None = pdt.Field(
        None,
        description=(
            "Reference to contract between the issuing and receiving "
            "organisations that governs the energy yield assessment."
        ),
        examples=["Contract ID.: P-MIR-00239432-0001-C, dated 2022-11-30"],
    )
    confidentiality_classification: str | None = pdt.Field(
        None,
        description="Confidentiality classification of the report.",
        examples=["Strictly confidential", "Commercial in confidence", "Public"],
    )
    coordinate_reference_system: CoordinateReferenceSystem = pdt.Field(
        ...,
        description="Coordinate reference system used for all location data.",
    )
