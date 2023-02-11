"""Pydantic data models relating to calculation model specifications.

"""

import pydantic as pdt

from eya_def_tools.data_models.base_models import EyaDefBaseModel
from eya_def_tools.data_models.fields import comments_field, description_field


# TODO add input data sources specification
class CalculationModelSpecification(EyaDefBaseModel):
    """Specification of a model used in an energy assessment."""

    name: str = pdt.Field(
        ...,
        description="Name of the model.",
        examples=["WAsP", "VORTEX BLOCKS", "DNV CFD", "VENTOS/M"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
