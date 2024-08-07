"""References to the IEA Task 43 WRA Data Model.

"""

from typing import Any, Final

import pydantic as pdt
from typing_extensions import Annotated

from eya_def_tools.constants import ALL_OF_TAG
from eya_def_tools.data_models.general import NonEmptyStr

IEA43_WRA_DATA_MODEL_SCHEMA_URI: Final[str] = (
    "https://raw.githubusercontent.com/IEA-Task-43/digital_wra_data_standard/"
    "master/schema/iea43_wra_data_model.schema.json"
)


WraDataModelDocument = Annotated[
    dict[NonEmptyStr, Any],
    pdt.WithJsonSchema(
        json_schema={
            ALL_OF_TAG: [{"ref": IEA43_WRA_DATA_MODEL_SCHEMA_URI}],
            "title": "Wind Dataset Metadata",
            "description": (
                "A wind dataset metadata document according to the IEA "
                "Wind Task 43 WRA Data Model JSON Schema."
            ),
            "examples": ["https://foo.com/bar/example_iea43.json"],
        },
        mode="validation",
    ),
]
