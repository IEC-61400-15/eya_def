"""Data models for spatial data.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel

x_field: float = pdt.Field(
    ...,
    description="Location x-coordinate (typically easting).",
    examples=[419665.0],
)

y_field: float = pdt.Field(
    ...,
    description="Location y-coordinate (typically northing).",
    examples=[6195240.0],
)


class Location(EyaDefBaseModel):
    """Specification of a horizontal location in space."""

    x: float = x_field
    y: float = y_field


class IdLocation(EyaDefBaseModel):
    """Specification of a horizontal location in space with an ID."""

    id: str = pdt.Field(
        default=...,
        min_length=1,
        description="Unique ID for the location within the EYA DEF document.",
        examples=["r4853", "E1.23_N4.56", "c11f0e96-5ba3-416d-a51b-274e7e29c7e5"],
    )
    x: float = x_field
    y: float = y_field
