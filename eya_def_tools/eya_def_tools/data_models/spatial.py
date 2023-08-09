"""Data models for spatial data.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.generic_fields import comments_field, description_field


class Location(EyaDefBaseModel):
    """Specification of a horizontal location in space."""

    location_id: str | None = pdt.Field(
        None,
        description="Unique identifier of the location.",
        examples=["ee15ff84-6733-4858-9656-ba995d9b1022", "WTG02-loc1"],
    )
    label: str | None = pdt.Field(
        None,
        description="Label of the location.",
        examples=[
            "T1",
            "WTG02-loc1",
            "WEA_003/R2",
        ],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    x: float = pdt.Field(
        ...,
        description="Location x-coordinate (typically easing).",
        examples=[419665.0],
    )
    y: float = pdt.Field(
        ...,
        description="Location y-coordinate (typically northing).",
        examples=[6195240.0],
    )
