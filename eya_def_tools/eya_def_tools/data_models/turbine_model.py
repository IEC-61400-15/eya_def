"""Data models for wind turbine model specifications.

"""

from typing import Any

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel, JsonPointerRef


class TurbineModelSpecification(JsonPointerRef):
    """Turbine model performance specification reference (PLACEHOLDER)."""

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update(
            **{
                "$ref": "https://foo.bar.com/baz/wtg_model.schema.json",
                "title": "Turbine Model Performance Specification Reference",
                "description": (
                    "Reference to a json document with turbine model "
                    "performance specification (PLACEHOLDER)."
                ),
                "examples": ["https://foo.com/bar/example_wtg_model.json"],
            }
        )
        if "type" in field_schema.keys():
            del field_schema["type"]


# TODO move to using only external schema
class TurbineModel(EyaDefBaseModel):
    """Specification of a wind turbine model."""

    turbine_model_id: str = pdt.Field(
        ...,
        description="Unique identifier of the turbine model.",
        examples=["dbb25743-60f4-4eab-866f-31d5f8af69d6", "XYZ199-8.5MW v004"],
    )
    label: str = pdt.Field(
        ...,
        description="Label of the turbine model.",
        examples=["V172-7.2 MW", "N175/6.X", "SG 6.6-170", "E-175 EP5"],
    )
    perf_spec_ref: TurbineModelSpecification | None = pdt.Field(
        None,
        title="Turbine Model Performance Specification Reference",
        description=(
            "Reference to a json document with turbine model "
            "performance specification (PLACEHOLDER)."
        ),
        examples=["https://foo.com/bar/example_wtg_model.json"],
    )
