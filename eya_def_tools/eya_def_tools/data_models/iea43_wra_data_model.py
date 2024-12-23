"""References to the IEA Task 43 WRA Data Model.

"""

from typing import Any, Final

import pydantic as pdt
from typing_extensions import Annotated

from eya_def_tools.constants import ALL_OF_TAG, EXTERNAL_REFERENCE_TAG
from eya_def_tools.data_models.general import NonEmptyStr

IEA43_WRA_DATA_MODEL_SCHEMA_URI: Final[str] = (
    "https://raw.githubusercontent.com/IEA-Task-43/digital_wra_data_standard/"
    "master/schema/iea43_wra_data_model.schema.json"
)


WraDataModelDocument = Annotated[
    dict[NonEmptyStr, Any],
    pdt.WithJsonSchema(
        json_schema={
            # External reference tag used temporarily to avoid conflict
            # with Pydantic's internal reference resolution process; it
            # needs to be replaced by the regular reference tag
            # subsequently when generating the final JSON Schema string
            ALL_OF_TAG: [{EXTERNAL_REFERENCE_TAG: IEA43_WRA_DATA_MODEL_SCHEMA_URI}],
            "title": "Wind Dataset Metadata",
            "description": (
                "A wind dataset metadata document according to the IEA "
                "Wind Task 43 WRA Data Model JSON Schema."
            ),
            "examples": [
                "https://raw.githubusercontent.com/IEA-Task-43/"
                "digital_wra_data_standard/master/demo_data/iea43_wra_data_model.json"
            ],
        },
        mode="validation",
    ),
]
