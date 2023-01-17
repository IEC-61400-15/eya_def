"""Pydantic data models relating to measurement stations.

"""

from eya_def_tools.data_models.base_models import EyaDefBaseModel, JsonPointerRef


class MeasurementStationMetadata(JsonPointerRef):
    """Measurement metadata according to the IEA Task 43 WRA data model."""

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(
            **{
                "$ref": (
                    "https://raw.githubusercontent.com/IEA-Task-43/"
                    "digital_wra_data_standard/master/schema/"
                    "iea43_wra_data_model.schema.json"
                ),
                "description": (
                    "A measurement metadata JSON document according to "
                    "the IEA Task 43 WRA Data Model."
                ),
                "examples": ["https://foo.com/bar/example_iea43.json"],
            }
        )
        if "type" in field_schema.keys():
            del field_schema["type"]


class MeasurementStationBasis(EyaDefBaseModel):
    """Measurement station basis in a wind resource assessment."""

    # TODO - placeholder to be implemented
    pass
