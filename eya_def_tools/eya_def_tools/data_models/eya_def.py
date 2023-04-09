"""Top level pydantic data model for the IEC 61400-15-2 EYA DEF.

"""

from __future__ import annotations

import datetime as dt
from typing import Any, Type

import pydantic as pdt

from eya_def_tools.data_models import base_models
from eya_def_tools.data_models.fields import comments_field, description_field
from eya_def_tools.data_models.measurement_station import MeasurementStationMetadata
from eya_def_tools.data_models.organisation import Organisation
from eya_def_tools.data_models.reference_wind_farm import ReferenceWindFarm
from eya_def_tools.data_models.report_metadata import ReportContributor
from eya_def_tools.data_models.scenario import Scenario
from eya_def_tools.data_models.spatial import CoordinateReferenceSystem
from eya_def_tools.data_models.turbine_model import TurbineModel
from eya_def_tools.data_models.wind_resource import WindResourceAssessment
from eya_def_tools.utils.pydantic_json_schema_utils import (
    move_field_to_definitions,
    reduce_json_schema_all_of,
    reduce_json_schema_single_use_definitions,
)
from eya_def_tools.utils.reference_utils import (
    get_json_schema_reference_uri,
    get_json_schema_uri,
    get_json_schema_version,
)


class EyaDef(base_models.BaseModelWithRefs):
    """IEC 61400-15-2 EYA DEF energy yield assessment data model."""

    class Config:
        """``EyaDef`` data model configurations."""

        @staticmethod
        def schema_extra(schema: dict[str, Any], model: Type[EyaDef]) -> None:
            """Additional items for the model schema."""
            base_models.BaseModelWithRefs.Config.schema_extra(
                schema=schema, model=model
            )
            schema.update(
                {
                    "$schema": get_json_schema_reference_uri(),
                    "$id": get_json_schema_uri(),
                    "$version": get_json_schema_version(),
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
    title: str = pdt.Field(
        ...,
        description="Title of the energy assessment report.",
        examples=["Energy yield assessment of the Barefoot Wind Farm"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    project_name: str = pdt.Field(
        ...,
        description="Name of the project under assessment.",
        examples=["Barefoot Wind Farm"],
    )
    document_id: str | None = pdt.Field(
        None,
        title="Document ID",
        description=(
            "The ID of the report document; not including the version "
            "when 'document_version' is used."
        ),
        examples=["C385945/A/UK/R/002", "0345.923454.0001"],
    )
    document_version: str | None = pdt.Field(
        None,
        description="Version of the report document, also known as revision.",
        examples=["1.2.3", "A", "Rev. A"],
    )
    issue_date: dt.date = pdt.Field(
        ...,
        description=(
            "Report issue date in the ISO 8601 standard format for a "
            "calendar date, i.e. YYYY-MM-DD."
        ),
        examples=["2022-10-05"],
    )
    contributors: list[ReportContributor] = pdt.Field(
        ..., description="List of report contributors (e.g. author and verifier)"
    )
    issuing_organisations: list[Organisation] = pdt.Field(
        ..., description="The organisation(s) issuing the report (e.g. consultant)."
    )
    receiving_organisations: list[Organisation] | None = pdt.Field(
        None,
        description=(
            "The organisation(s) receiving the report (e.g. client), if relevant."
        ),
    )
    contract_reference: str | None = pdt.Field(
        None,
        description=(
            "Reference to contract between the issuing and receiving "
            "organisations that governs the energy yield assessment."
        ),
        examples=["Contract ID.: P-MIR-00239432-0001-C, dated 2022-11-30"],
    )
    confidentiality_classification: str | None = pdt.Field(
        None,
        description="Confidentiality classification of the report.",
        examples=["Strictly confidential", "Commercial in confidence", "Public"],
    )
    coordinate_reference_system: CoordinateReferenceSystem = pdt.Field(
        ..., description="Coordinate reference system used for all location data."
    )
    measurement_stations: list[MeasurementStationMetadata] = pdt.Field(
        [],  # TODO update to required when example is included
        description=(
            "List of measurement station metadata JSON document(s) "
            "according to the IEA Task 43 WRA Data Model."
        ),
    )
    reference_wind_farms: list[ReferenceWindFarm] | None = pdt.Field(
        None, description="List of reference operational wind farms."
    )
    wind_resource_assessments: list[WindResourceAssessment] | None = pdt.Field(
        None,
        description=(
            "List of wind resource assessments, including results, at "
            "the measurement station locations."
        ),
    )
    turbine_models: list[TurbineModel] | None = pdt.Field(
        None, description="List of wind turbine model specifications."
    )
    scenarios: list[Scenario] | None = pdt.Field(
        None, description="List of energy yield assessment scenarios."
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
        reduce_json_schema_all_of(schema)

        # Move description and comments field to the definitions section
        defined_field_dict = {
            "description": "DescriptionField",
            "comments": "CommentsField",
        }
        move_field_to_definitions(schema=schema, defined_field_dict=defined_field_dict)

        # Move single use JSON Schema definitions to where they are used
        reduce_json_schema_single_use_definitions(schema=schema)

        return schema
