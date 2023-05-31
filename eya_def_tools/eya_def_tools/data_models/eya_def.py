"""Top level pydantic data model for the IEC 61400-15-2 EYA DEF.

"""

from __future__ import annotations

import datetime as dt
from typing import Any, Type

import pydantic as pdt

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.eya_def_header import (
    confidentiality_classification_field,
    contract_reference_field,
    contributors_field,
    document_id_field,
    document_version_field,
    issue_date_field,
    issuing_organisations_field,
    json_uri_field,
    project_county_field,
    project_name_field,
    receiving_organisations_field,
    title_field,
)
from eya_def_tools.data_models.generic_fields import comments_field, description_field
from eya_def_tools.data_models.measurement_station import MeasurementStationMetadata
from eya_def_tools.data_models.reference_met_data import ReferenceMeteorologicalDataset
from eya_def_tools.data_models.reference_wind_farm import ReferenceWindFarm
from eya_def_tools.data_models.report_metadata import Organisation, ReportContributor
from eya_def_tools.data_models.scenario import Scenario
from eya_def_tools.data_models.spatial import CoordinateReferenceSystem
from eya_def_tools.data_models.turbine_model import TurbineModel
from eya_def_tools.data_models.wind_resource import WindResourceAssessment
from eya_def_tools.utils import pydantic_json_schema_utils, reference_utils


class EyaDefDocument(EyaDefBaseModel):
    """IEC 61400-15-2 EYA DEF top-level data model."""

    class Config:
        """``EyaDef`` data model configurations."""

        # Equivalent of ``"additionalProperties": true``, which is used
        # only at the top level to allow further metadata fields
        extra = pdt.Extra.allow

        @staticmethod
        def schema_extra(schema: dict[str, Any], model: Type[EyaDefDocument]) -> None:
            """Additional items for the model schema."""
            EyaDefBaseModel.Config.schema_extra(schema=schema, model=model)
            schema.update(
                {
                    "$schema": reference_utils.get_json_schema_reference_uri(),
                    "$id": reference_utils.get_json_schema_uri(),
                    "$version": reference_utils.get_json_schema_version(),
                    "title": "IEC 61400-15-2 EYA DEF Schema",
                    "additionalProperties": True,
                }
            )

    json_uri: str | None = json_uri_field
    title: str = title_field
    description: str | None = description_field
    comments: str | None = comments_field
    project_name: str = project_name_field
    project_county: str = project_county_field
    document_id: str | None = document_id_field
    document_version: str | None = document_version_field
    issue_date: dt.date = issue_date_field
    contributors: list[ReportContributor] = contributors_field
    issuing_organisations: list[Organisation] = issuing_organisations_field
    receiving_organisations: list[Organisation] | None = receiving_organisations_field
    contract_reference: str | None = contract_reference_field
    confidentiality_classification: str | None = confidentiality_classification_field
    coordinate_reference_system: CoordinateReferenceSystem = pdt.Field(
        ...,
        description="Coordinate reference system used for all location data.",
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

        # Remove ``$id`` from ``properties`` since this definition is
        # inherent in JSON Schema and only needed by the pydantic model
        if "$id" in schema["properties"]:
            del schema["properties"]["$id"]

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
