"""Model field definitions for the EYA DEF data model.

"""


import pydantic as pdt

description_field: str | None = pdt.Field(
    None,
    description="Description of the data object.",
)


comments_field: str | None = pdt.Field(
    None,
    description="Comments on the data object.",
)
