"""References to the IEC 61400-16 Power Curve Schema.

"""

from typing import Annotated, Any, Final

import pydantic as pdt

from eya_def_tools.constants import ALL_OF_TAG, EXTERNAL_REFERENCE_TAG
from eya_def_tools.data_models.general import NonEmptyStr

IEC61400_16_POWER_CURVE_SCHEMA_SCHEMA_URI: Final[str] = (
    "https://raw.githubusercontent.com/octue/power-curve-schema/"
    "main/power-curve-schema/schema.json"
)


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
]
