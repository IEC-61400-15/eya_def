"""Module for data models of various general metadata.

"""

import datetime as dt
from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.enums import ReportContributorType


class ReportContributor(EyaDefBaseModel):
    """Contributor to an energy yield assessment."""

    name: str = pdt.Field(
        default=...,
        description="Name of the contributor.",
        examples=["Joan Miro", "Andrei Tarkovsky"],
    )
    email_address: Optional[pdt.EmailStr] = pdt.Field(
        default=None,
        description="Email address of the contributor.",
        examples=["j.miro@art.cat", "andrei.tarkovsky@cinema.com"],
    )
    contributor_type: ReportContributorType = pdt.Field(
        default=...,
        description="Type of contributor.",
    )
    contribution_comments: Optional[str] = pdt.Field(
        default=None,
        description="Comments to clarify contribution.",
        examples=["Second author"],
    )
    completion_date: Optional[dt.date] = pdt.Field(
        default=None,
        description="Contribution completion date (format YYYY-MM-DD).",
        examples=["2022-10-04"],
    )


class Organisation(EyaDefBaseModel):
    """Issuing or receiving organisation of an energy yield assessment."""

    name: str = pdt.Field(
        default=...,
        description="Entity name of the organisation.",
        examples=["The Torre Egger Consultants Limited", "Miranda Investments Limited"],
    )
    abbreviation: Optional[str] = pdt.Field(
        default=None,
        description="Abbreviated name of the organisation.",
        examples=["Torre Egger", "Miranda"],
    )
    address: Optional[str] = pdt.Field(
        default=None,
        description="Address of the organisation.",
        examples=["5 Munro Road, Summit Centre, Sgurrsville, G12 0YE, UK"],
    )
    contact_name: Optional[str] = pdt.Field(
        default=None,
        description="Name(s) of contact person(s) in the organisation.",
        examples=["Luis Bunuel", "Miles Davis, John Coltrane"],
    )
