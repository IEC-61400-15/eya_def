"""References to the IEA Task 43 WRA Data Model."""

from collections.abc import Mapping
from typing import Annotated, Any, Final

import jsonschema
import pydantic as pdt

from eya_def_tools.constants import ALL_OF_TAG, EXTERNAL_REFERENCE_TAG
from eya_def_tools.data_models.general import NonEmptyStr
from eya_def_tools.utils import loading_utils

IEA43_WRA_DATA_MODEL_SCHEMA_URI: Final[str] = (
    "https://raw.githubusercontent.com/IEA-Task-43/digital_wra_data_standard/"
    "master/schema/iea43_wra_data_model.schema.json"
)

IEA43_WRA_DATA_MODEL_SCHEMA: Final[Mapping[str, Any]] = loading_utils.load_json_schema(
    json_schema_uri=IEA43_WRA_DATA_MODEL_SCHEMA_URI,
)


def json_schema_validate_wra_data_model_document(
    value: dict[str, Any],
) -> dict[str, Any]:
    jsonschema.validate(instance=value, schema=IEA43_WRA_DATA_MODEL_SCHEMA)

    return value


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
                "A wind dataset metadata document according to the IEA Wind Task 43 WRA Data Model JSON Schema."
            ),
            "examples": [
                "https://raw.githubusercontent.com/IEA-Task-43/"
                "digital_wra_data_standard/master/demo_data/iea43_wra_data_model.json"
            ],
        },
        mode="validation",
    ),
    pdt.BeforeValidator(json_schema_validate_wra_data_model_document),
]
