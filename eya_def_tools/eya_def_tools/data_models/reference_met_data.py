"""Data models relating to reference meteorological data.

Reference meteorological data includes reanalysis datasets, mesoscale
model datasets and measurement datasets from off-site ground-based
meteorological stations.

"""

import datetime as dt
from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.general import (
    TimeResolution,
    end_date_field,
    start_date_field,
)
from eya_def_tools.data_models.spatial import IdLocation


class ReferenceMeteorologicalDatasetMetadata(EyaDefBaseModel):
    """Metadata for a reference meteorological dataset."""

    id: str = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Unique ID for the reference meteorological dataset within "
            "the EYA DEF document."
        ),
        examples=["ERA5", "WRF_MERRA2_r0245_a"],
    )
    description: str = pdt.Field(
        default=...,
        min_length=1,
        description="Description of the meteorological dataset.",
        examples=[
            "The ERA5 reanalysis dataset.",
            "In-house WRF simulation seeded with MERRA2 reanalysis.",
        ],
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the meteorological dataset, which "
            "should not be empty if the field is included."
        ),
    )
    locations: list[IdLocation] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "The horizontal spatial location(s) of the meteorological "
            "data, with each location item including an ID for "
            "referencing in addition to the spatial coordinates. Where "
            "a large number of locations have been used (i.e. a large "
            "grid) and it is not relevant to include all, a subset can "
            "be included here and elaborated upon in the comments. All "
            "locations for which results are presented must be "
            "included."
        ),
    )
    time_resolution: TimeResolution = pdt.Field(
        default=...,
        description="Time resolution of the reference meteorological data.",
    )
    start_date: dt.date = start_date_field
    end_date: dt.date = end_date_field
