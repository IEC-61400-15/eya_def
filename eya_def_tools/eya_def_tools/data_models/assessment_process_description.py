"""Pydantic data models relating to assessment process descriptions.

"""

import pydantic as pdt

from eya_def_tools.data_models import base_models
from eya_def_tools.data_models.fields import comments_field, description_field


# TODO add input data sources specification
class AssessmentProcessDescription(base_models.EyaDefBaseModel):
    """Description of a process used in an energy yield assessment."""

    name: str = pdt.Field(
        ...,
        description="Name of the process or model use in the process.",
        examples=["WAsP", "VORTEX BLOCKS", "DNV CFD", "VENTOS/M"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
