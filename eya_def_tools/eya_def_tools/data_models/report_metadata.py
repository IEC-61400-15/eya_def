"""Pydantic data models for report metadata.

"""

import datetime as dt
from typing import Literal

import pydantic as pdt

from eya_def_tools.data_models.base_models import EyaDefBaseModel


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
