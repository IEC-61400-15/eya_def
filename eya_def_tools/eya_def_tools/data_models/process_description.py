"""Pydantic data models relating to assessment process descriptions.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_models import EyaDefBaseModel
from eya_def_tools.data_models.fields import comments_field, description_field


class AssessmentProcessDescription(EyaDefBaseModel):
    """Description of a process used in an energy yield assessment."""

    name: str = pdt.Field(
        ...,
        description="Name of the process or model.",
        examples=["WAsP", "VORTEX BLOCKS", "DNV CFD", "VENTOS/M"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
