"""Top level pydantic data model for the IEC 61400-15-2 EYA DEF.

"""

from __future__ import annotations

from typing import Any, Type

import pydantic as pdt

from eya_def_tools.data_models.base_models import BaseModelWithRefs
from eya_def_tools.data_models.measurement_station import MeasurementStationMetadata
from eya_def_tools.data_models.reference_met_data import ReferenceMeteorologicalDataset
from eya_def_tools.data_models.reference_wind_farm import ReferenceWindFarm
from eya_def_tools.data_models.report_metadata import ReportMetadata
from eya_def_tools.data_models.scenario import Scenario
from eya_def_tools.data_models.turbine_model import TurbineModel
from eya_def_tools.data_models.wind_resource import WindResourceAssessment
from eya_def_tools.utils import pydantic_json_schema_utils, reference_utils


class EyaDef(BaseModelWithRefs):
    """IEC 61400-15-2 EYA DEF energy yield assessment data model."""

    class Config:
        """``EyaDef`` data model configurations."""

        @staticmethod
        def schema_extra(schema: dict[str, Any], model: Type[EyaDef]) -> None:
            """Additional items for the model schema."""
            BaseModelWithRefs.Config.schema_extra(schema=schema, model=model)
            schema.update(
                {
                    "$schema": reference_utils.get_json_schema_reference_uri(),
                    "$id": reference_utils.get_json_schema_uri(),
                    "$version": reference_utils.get_json_schema_version(),
                    "title": "IEC 61400-15-2 EYA DEF Schema",
                    "additionalProperties": False,
                }
            )

    json_uri: str | None = pdt.Field(
        None,
        title="ID",
        description="Unique URI of the JSON document.",
        examples=[
            "https://foo.com/api/eya?id=8f46a815-8b6d-4870-8e92-c031b20320c6.json"
        ],
        alias="$id",
    )
    report_metadata: ReportMetadata = pdt.Field(
        ...,
        description="Metadata fields for the EYA report.",
    )
    measurement_stations: list[MeasurementStationMetadata] | None = pdt.Field(
        None,
        description=(
            "List of measurement station metadata JSON document(s) "
            "according to the IEA Task 43 WRA Data Model, for all "
            "station datasets used in the EYA."
        ),
    )
    reference_wind_farms: list[ReferenceWindFarm] | None = pdt.Field(
        None,
        description="List of reference operational wind farms used in the EYA.",
    )
    reference_meteorological_datasets: (
        list[ReferenceMeteorologicalDataset] | None
    ) = pdt.Field(
        None,
        description="List of reference meteorological datasets used in the EYA.",
    )
    wind_resource_assessments: list[WindResourceAssessment] | None = pdt.Field(
        None,
        description=(
            "List of wind resource assessments, including results, at "
            "the measurement station locations."
        ),
    )
    turbine_models: list[TurbineModel] | None = pdt.Field(
        None,
        description="List of wind turbine model specifications.",
    )
    scenarios: list[Scenario] | None = pdt.Field(
        None,
        description="List of energy yield assessment scenarios.",
    )

    @pdt.validator("measurement_stations", each_item=True)
    def cast_measurement_stations(cls, v: Any) -> MeasurementStationMetadata:
        """Cast ``measurement_stations`` as ``MeasurementStationMetadata``.

        :param v: each value passed in the ``measurement_stations`` list
            to the ``EyaDef`` constructor
        :return: the value of ``v`` cast as ``MeasurementStationMetadata``
        """
        return MeasurementStationMetadata(v)

    @classmethod
    def final_json_schema(cls) -> dict[str, Any]:
        """Get a json schema representation of the top-level data model."""
        schema = cls.schema(by_alias=True)

        # Remove redundant ``allOf`` elements
        pydantic_json_schema_utils.reduce_json_schema_all_of(schema)

        # Move description and comments field to the definitions section
        defined_field_dict = {
            "description": "DescriptionField",
            "comments": "CommentsField",
        }
        pydantic_json_schema_utils.move_field_to_definitions(
            schema=schema, defined_field_dict=defined_field_dict
        )

        # Move single use JSON Schema definitions to where they are used
        pydantic_json_schema_utils.reduce_json_schema_single_use_definitions(
            schema=schema
        )

        return schema
