"""Data models for spatial data.

"""

from typing import Annotated

import pydantic as pdt
import pyproj
from pydantic.functional_validators import AfterValidator
from pyproj.exceptions import CRSError

from eya_def_tools.data_models.base_model import EyaDefBaseModel


class Location(EyaDefBaseModel):
    """Specification of a horizontal location in space."""

    x: float = pdt.Field(
        ...,
        allow_inf_nan=False,
        description="Location x-coordinate (typically easting).",
        examples=[419665.0],
    )
    y: float = pdt.Field(
        ...,
        allow_inf_nan=False,
        description="Location y-coordinate (typically northing).",
        examples=[6195240.0],
    )


def _validate_epsg(value: int) -> int:
    try:
        _ = pyproj.CRS.from_epsg(code=value)
    except CRSError:
        raise ValueError(f"Invalid EPSG SRID code {value}.")

    return value


EpsgSrid = Annotated[int, AfterValidator(_validate_epsg)]
