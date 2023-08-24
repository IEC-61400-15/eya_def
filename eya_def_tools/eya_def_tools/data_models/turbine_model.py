"""Data models for wind turbine model specifications.

"""

from typing import Any

import pydantic as pdt
from typing_extensions import Annotated

# IEC61400_16_POWER_CURVE_DATA_MODEL_SCHEMA_URI: Final[str] = (
#     "https://raw.githubusercontent.com/path-to-schema.schema.json"
# )
# TODO update once draft of IEC-61400-16 data model is ready


TurbineModelSpecifications = Annotated[
    dict[str, Any],
    pdt.WithJsonSchema(
        json_schema={
            # "allOf": [{"ref": IEC61400_16_POWER_CURVE_DATA_MODEL_SCHEMA_URI}],
            "type": "object",  # TODO TEMPORARY PLACEHOLDER
            "properties": {},  # TODO TEMPORARY PLACEHOLDER
            "title": "Turbine Model Specifications",
            "description": (
                "Wind turbine performance specifications according to "
                "the IEC-61400-16 data model."
            ),
            "examples": ["https://foo.com/bar/example_wtg_model.json"],
        },
        mode="validation",
    ),
]
