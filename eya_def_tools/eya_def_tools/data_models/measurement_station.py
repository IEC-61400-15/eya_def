"""Data models relating to measurement station metadata.

"""

from typing import Any, Final

from eya_def_tools.data_models.base_model import JsonPointerRef

IEA43_WRA_DATA_MODEL_SCHEMA_URI: Final[str] = (
    "https://raw.githubusercontent.com/IEA-Task-43/digital_wra_data_standard/"
    "master/schema/iea43_wra_data_model.schema.json"
)


class MeasurementStationMetadata(JsonPointerRef):
    """Measurement metadata according to the IEA Task 43 WRA data model."""

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update(
            **{
                "$ref": IEA43_WRA_DATA_MODEL_SCHEMA_URI,
                "description": (
                    "A measurement metadata JSON document according to "
                    "the IEA Task 43 WRA Data Model."
                ),
                "examples": ["https://foo.com/bar/example_iea43.json"],
            }
        )
        if "type" in field_schema.keys():
            del field_schema["type"]
