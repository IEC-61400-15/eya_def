"""Data models relating to assessment process descriptions.

"""

from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.general import NonEmptyStr


class AssessmentProcessDescription(EyaDefBaseModel):
    """Description of a process used in an energy yield assessment."""

    label: NonEmptyStr = pdt.Field(
        default=...,
        description="Label or name of the process or model.",
        examples=["WAsP", "VORTEX BLOCKS", "DNV CFD", "VENTOS/M"],
    )
    description: NonEmptyStr = pdt.Field(
        default=...,
        description="Description of the assessment process or model.",
    )
    comments: Optional[NonEmptyStr] = pdt.Field(
        default=None,
        description=(
            "Optional comments on the assessment process or model, "
            "which should not be empty if the field is included."
        ),
    )
