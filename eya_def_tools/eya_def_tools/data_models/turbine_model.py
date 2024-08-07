"""Data models for wind turbine model specifications.

"""

from typing import Annotated, Any, Final

import pydantic as pdt

from eya_def_tools.constants import ALL_OF_TAG
from eya_def_tools.data_models.general import NonEmptyStr

IEC61400_16_POWER_CURVE_DATA_MODEL_SCHEMA_URI: Final[str] = (
    "https://raw.githubusercontent.com/octue/power-curve-schema/"
    "main/power-curve-schema/schema.json"
)


TurbineModelSpecifications = Annotated[
    dict[NonEmptyStr, Any],
    pdt.WithJsonSchema(
        json_schema={
            ALL_OF_TAG: [{"ref": IEC61400_16_POWER_CURVE_DATA_MODEL_SCHEMA_URI}],
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
