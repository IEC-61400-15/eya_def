"""Data models for spatial data.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.general import ValidFloat


class Location(EyaDefBaseModel):
    """Specification of a horizontal location in space."""

    x: ValidFloat = pdt.Field(
        ...,
        description="Location x-coordinate (typically easing).",
        examples=[419665.0],
    )
    y: ValidFloat = pdt.Field(
        ...,
        description="Location y-coordinate (typically northing).",
        examples=[6195240.0],
    )
