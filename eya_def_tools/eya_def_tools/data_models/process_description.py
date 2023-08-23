"""Data models relating to assessment process descriptions.

"""

from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel


class AssessmentProcessDescription(EyaDefBaseModel):
    """Description of a process used in an energy yield assessment."""

    label: str = pdt.Field(
        default=...,
        description="Label or name of the process or model.",
        examples=["WAsP", "VORTEX BLOCKS", "DNV CFD", "VENTOS/M"],
    )
    description: str = pdt.Field(
        default=...,
        min_length=1,  # Value should not be empty
        description="Description of the assessment process or model.",
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,  # Value should not be empty if the field is included
        description="Optional comments on the plant performance loss subcategory.",
    )
