"""Model field definitions for the EYA DEF schema.

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
