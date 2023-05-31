"""Pydantic data models for report metadata.

"""

import datetime as dt

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.enums import ReportContributorType


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
    contributor_type: ReportContributorType = pdt.Field(
        ...,
        description="Type of contributor.",
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
