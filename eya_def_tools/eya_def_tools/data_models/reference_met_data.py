"""Data models relating to reference meteorological data.

Reference meteorological data includes reanalysis datasets, mesoscale
model datasets and measurement datasets from off-site ground-based
meteorological stations.

On-site wind measurement station metadata should be represented using
the IEA Task 43 WRA data model. See the module ``measurement_station``.

"""

import datetime as dt
from typing import Optional

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.general import (
    TimeResolution,
    data_period_end_date_field,
    data_period_start_date_field,
)
from eya_def_tools.data_models.spatial import Location


class ReferenceMeteorologicalDataset(EyaDefBaseModel):
    """Metadata for a reference meteorological dataset.

    The schema describes a dataset at a single horizontal spatial
    location. Separate data model instances need to be used to describe
    data at different location from the same source dataset (e.g.
    different grid cells from a reanalysis dataset).
    """

    id: str = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "Unique ID for the reference meteorological dataset within "
            "the EYA DEF document."
        ),
        examples=["ERA5_1.23_4.56", "WRF_r0245_a"],
    )
    description: str = pdt.Field(
        default=...,
        min_length=1,
        description="Description of the meteorological dataset.",
        examples=["The ERA5 reanalysis dataset."],
    )
    comments: Optional[str] = pdt.Field(
        default=None,
        min_length=1,
        description=(
            "Optional comments on the meteorological dataset, which "
            "should not be empty if the field is included."
        ),
    )
    locations: list[Location] = pdt.Field(
        default=...,
        min_length=1,
        description=(
            "The horizontal spatial location(s) of the meteorological "
            "data. Where a large number of locations have been used "
            "and it is not practical to include all, a subset can be "
            "included here and elaborated upon in the comments."
        ),
    )
    time_resolution: TimeResolution = pdt.Field(
        default=...,
        description="Time resolution of the reference meteorological data.",
    )
    data_period_start_date: dt.date = data_period_start_date_field
    data_period_end_date: dt.date = data_period_end_date_field
