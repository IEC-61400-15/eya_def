"""Data models for spatial data.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel


class Location(EyaDefBaseModel):
    """Specification of a horizontal location in space."""

    x: float = pdt.Field(
        ...,
        description="Location x-coordinate (typically easting).",
        examples=[419665.0],
    )
    y: float = pdt.Field(
        ...,
        description="Location y-coordinate (typically northing).",
        examples=[6195240.0],
    )
