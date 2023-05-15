"""Pydantic data models relating to reference meteorological data.

Reference meteorological data includes reanalysis datasets, mesoscale
model datasets and measurement datasets from off-site ground-based
meteorological stations.

On-site wind measurement station metadata should be represented using
the IEA Task 43 WRA data model. See the module ``measurement_station``.

"""


import pydantic as pdt

from eya_def_tools.data_models.base_models import EyaDefBaseModel
from eya_def_tools.data_models.fields import comments_field, description_field
from eya_def_tools.data_models.spatial import Location


class ReferenceMeteorologicalDataset(EyaDefBaseModel):
    """Metadata for a reference meteorological dataset.

    The schema describes a dataset at a single horizontal spatial
    location. Separate data model instances need to be used to describe
    data at different location from the same source dataset (e.g.
    different grid cells from a reanalysis dataset).
    """

    reference_meteorological_dataset_id: str = pdt.Field(
        ...,
        description=(
            "Unique ID for the reference meteorological dataset within "
            "the EYA DEF document."
        ),
        examples=["ERA5_1.23_4.56", "WRF_r0245_a"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    location: Location = pdt.Field(
        ...,
        description="The horizontal spatial location of the meteorological data.",
    )

    # TODO - complete reference meteorological dataset metadata schema
