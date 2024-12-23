"""References to the IEC 61400-16 Power Curve Schema.

"""

from collections.abc import Mapping
from typing import Annotated, Any, Final

import jsonschema
import pydantic as pdt

from eya_def_tools.constants import ALL_OF_TAG, EXTERNAL_REFERENCE_TAG
from eya_def_tools.data_models.general import NonEmptyStr
from eya_def_tools.utils import loading_utils

IEC61400_16_POWER_CURVE_SCHEMA_SCHEMA_URI: Final[str] = (
    "https://raw.githubusercontent.com/octue/power-curve-schema/"
    "main/power-curve-schema/schema.json"
)

IEC61400_16_POWER_CURVE_SCHEMA_SCHEMA: Final[Mapping[str, Any]] = (
    loading_utils.load_json_schema(
        json_schema_uri=IEC61400_16_POWER_CURVE_SCHEMA_SCHEMA_URI,
    )
)


def json_schema_validate_power_curve_document(value: dict[str, Any]) -> dict[str, Any]:
    jsonschema.validate(instance=value, schema=IEC61400_16_POWER_CURVE_SCHEMA_SCHEMA)

    return value


PowerCurveDocument = Annotated[
    dict[NonEmptyStr, Any],
    pdt.WithJsonSchema(
        json_schema={
            # External reference tag used temporarily to avoid conflict
            # with Pydantic's internal reference resolution process; it
            # needs to be replaced by the regular reference tag
            # subsequently when generating the final JSON Schema string
            ALL_OF_TAG: [
                {EXTERNAL_REFERENCE_TAG: IEC61400_16_POWER_CURVE_SCHEMA_SCHEMA_URI}
            ],
            "title": "Power Curve Document",
            "description": (
                "A document specifying power curves and associated "
                "information for a turbine model according to the "
                "IEC 61400-16 Power Curve Schema."
            ),
            "examples": [
                "https://raw.githubusercontent.com/octue/power-curve-schema/"
                "main/power-curve-schema/examples/generic-274-20.json"
            ],
        },
        mode="validation",
    ),
    pdt.BeforeValidator(json_schema_validate_power_curve_document),
]
