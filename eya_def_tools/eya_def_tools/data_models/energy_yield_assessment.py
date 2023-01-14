"""Top level pydantic data model for the IEC 61400-15-2 EYA DEF.

"""

from __future__ import annotations

import datetime as dt
from typing import Any, Literal, Type

import pydantic as pdt

from eya_def_tools.data_models.base_models import BaseModelWithRefs, JsonPointerRef
from eya_def_tools.data_models.enums import (
    ComponentAssessmentBasis,
    ComponentVariabilityType,
    PlantPerformanceCategoryLabel,
    UncertaintyCategoryLabel,
    WindFarmRelevance,
)
from eya_def_tools.data_models.fields import comments_field, description_field
from eya_def_tools.data_models.results import Results
from eya_def_tools.utils.pydantic_json_schema_utils import (
    add_null_type_to_schema_optional_fields,
    move_field_to_definitions,
    reduce_json_schema_all_of,
)
from eya_def_tools.utils.reference_utils import (
    get_json_schema_reference_uri,
    get_json_schema_uri,
    get_json_schema_version,
)


class CoordinateReferenceSystem(pdt.BaseModel):
    """Specification of a coordinate reference system for GIS data."""

    system_label: str = pdt.Field(
        ...,
        description="Label of the coordinate system.",
        examples=["OSGB36 / British National Grid", "SWEREF99 TM"],
    )
    epsg_srid: int | None = pdt.Field(
        None,
        description="EPSG Spatial Reference System Identifier (SRID).",
        examples=[27700, 3006],
    )
    wkt: str | None = pdt.Field(
        None,
        description="Well-known text (WKT) string definition of the coordinate system.",
    )


class Location(pdt.BaseModel):
    """Specification of a horizontal location in space."""

    location_id: str | None = pdt.Field(
        None,
        description="Unique identifier of the location.",
        examples=["ee15ff84-6733-4858-9656-ba995d9b1022", "WTG02-loc1"],
    )
    label: str | None = pdt.Field(
        None,
        description="Label of the location.",
        examples=[
            "T1",
            "WTG02-loc1",
            "WEA_003/R2",
        ],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    x: float = pdt.Field(
        ...,
        description="Location x-coordinate (typically easing).",
        examples=[419665.0],
    )
    y: float = pdt.Field(
        ...,
        description="Location y-coordinate (typically northing).",
        examples=[6195240.0],
    )


class MeasurementStationMetadata(JsonPointerRef):
    """Measurement metadata according to the IEA Task 43 WRA data model."""

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(
            **{
                "$ref": (
                    "https://raw.githubusercontent.com/IEA-Task-43/"
                    "digital_wra_data_standard/master/schema/"
                    "iea43_wra_data_model.schema.json"
                ),
                "description": (
                    "A measurement metadata JSON document according to "
                    "the IEA Task 43 WRA Data Model."
                ),
                "examples": ["https://foo.com/bar/example_iea43.json"],
            }
        )
        if "type" in field_schema.keys():
            del field_schema["type"]


class MeasurementStationBasis(pdt.BaseModel):
    """Measurement station basis in a wind resource assessment."""

    # TODO - placeholder to be implemented
    pass


class ReferenceWindFarm(pdt.BaseModel):
    """Reference wind farm metadata."""

    # TODO - placeholder to be implemented
    pass


class ReferenceWindFarmBasis(pdt.BaseModel):
    """Reference wind farm basis in a wind resource assessment."""

    # TODO - placeholder to be implemented
    pass


class TurbineModelPerfSpecRef(JsonPointerRef):
    """Turbine model performance specification reference (PLACEHOLDER)."""

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(
            **{
                "$ref": "https://foo.bar.com/baz/wtg_model.schema.json",
                "title": "Turbine Model Performance Specification Reference",
                "description": (
                    "Reference to a json document with turbine model "
                    "performance specification (PLACEHOLDER)."
                ),
                "examples": ["https://foo.com/bar/example_wtg_model.json"],
            }
        )
        if "type" in field_schema.keys():
            del field_schema["type"]


# TODO consider only using external schema
class TurbineModel(BaseModelWithRefs):
    """Specification of a wind turbine model."""

    turbine_model_id: str = pdt.Field(
        ...,
        description="Unique identifier of the turbine model.",
        examples=["dbb25743-60f4-4eab-866f-31d5f8af69d6", "XYZ199-8.5MW v004"],
    )
    label: str = pdt.Field(
        ...,
        description="Label of the turbine model.",
        examples=["V172-7.2 MW", "N175/6.X", "SG 6.6-170", "E-175 EP5"],
    )
    perf_spec_ref: TurbineModelPerfSpecRef | None = pdt.Field(
        None,
        title="Turbine Model Performance Specification Reference",
        description=(
            "Reference to a json document with turbine model "
            "performance specification (PLACEHOLDER)."
        ),
        examples=["https://foo.com/bar/example_wtg_model.json"],
    )


# TODO expand definition of operational restriction
class OperationalRestriction(pdt.BaseModel):
    """Specifications of an operational restriction."""

    label: str = pdt.Field(
        ...,
        description="Label of the operational restriction.",
        examples=["WSM curtailment", "MEC curtailment"],
    )
    description: str | None = description_field
    comments: str | None = comments_field


class TurbineSpecification(pdt.BaseModel):
    """Specification of all details for a turbine configuration."""

    turbine_id: str | None = pdt.Field(
        None,
        description="Unique identifier of the turbine specification.",
        examples=["b55caeac-f152-4b13-8217-3fddeab792cf", "T1-scen1"],
    )
    label: str = pdt.Field(
        ...,
        description="Label of the turbine.",
        examples=[
            "T1",
            "WTG02",
            "WEA_003",
        ],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    location: Location = pdt.Field(
        ..., description="Horizontal location of the turbine."
    )
    hub_height: float = pdt.Field(..., description="Turbine hub height.")
    turbine_model_id: str = pdt.Field(
        ..., description="Unique identifier of the turbine model."
    )
    restrictions: list[OperationalRestriction] | None = pdt.Field(
        None, description="List of operational restrictions at the turbine level."
    )


class WindFarm(pdt.BaseModel):
    """A collection of wind turbines considered as one unit (plant)."""

    name: str = pdt.Field(
        ...,
        description="Name of the wind farm.",
        examples=["Barefoot Wind Farm", "Project Summit Phase III"],
    )
    label: str | None = pdt.Field(
        None,
        description="Abbreviated label of the wind farm.",
        examples=["BWF", "Summit PhIII"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    turbines: list[TurbineSpecification] = pdt.Field(
        ..., description="List of specifications for constituent turbines."
    )
    relevance: WindFarmRelevance = pdt.Field(
        ..., description="The relevance of the wind farm for the assessment."
    )
    operational_lifetime_start_date: dt.date | None = pdt.Field(
        None,
        description="Operational lifetime start date (format YYYY-MM-DD).",
        examples=["2026-01-01", "2017-04-01"],
    )
    operational_lifetime_end_date: dt.date | None = pdt.Field(
        None,
        description="Operational lifetime end date (format YYYY-MM-DD).",
        examples=["2051-03-31", "2025-12-31"],
    )
    wind_farm_restrictions: list[OperationalRestriction] | None = pdt.Field(
        None, description="List of operational restrictions at the wind farm level."
    )


# TODO add input data sources specification
class CalculationModelSpecification(pdt.BaseModel):
    """Specification of a model used in an energy assessment."""

    name: str = pdt.Field(
        ...,
        description="Name of the model.",
        examples=["WAsP", "VORTEX BLOCKS", "DNV CFD", "VENTOS/M"],
    )
    description: str | None = description_field
    comments: str | None = comments_field


# TODO - this needs to be completed with more fields for relevant details
#      - it may need to be separated for the measurement wind resource
#        assessment and the turbine wind resource assessment
class UncertaintyComponent(pdt.BaseModel):
    """Wind resource uncertainty assessment component."""

    label: str = pdt.Field(
        ...,
        description="Label of the wind uncertainty component.",
        examples=["Long-term consistency"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    results: Results = pdt.Field(
        ..., description="Wind resource uncertainty assessment component results."
    )


class UncertaintyCategory(pdt.BaseModel):
    """Wind resource uncertainty assessment category."""

    components: list[UncertaintyComponent] = pdt.Field(
        ..., description="Wind resource uncertainty assessment components."
    )
    category_results: list[Results] = pdt.Field(
        ..., description="Category level assessment results."
    )


class UncertaintyAssessment(pdt.BaseModel):
    """Wind resource uncertainty assessment including all components."""

    categories: dict[UncertaintyCategoryLabel, UncertaintyCategory] = pdt.Field(
        ..., description="Wind resource uncertainty assessment categories."
    )


# TODO - to be extended
class WindResourceAssessment(pdt.BaseModel):
    """Wind resource assessment at the measurement locations."""

    # measurement_station_basis: MeasurementStationBasis
    # reference_wind_farm_basis: ReferenceWindFarmBasis
    # data_filtering
    # sensor_data_availability_results
    # sensor_results
    # gap_filling
    # primary_data_availability_results
    # primary_measurement_period_results
    # long_term_correction
    # long_term_results
    # vertical_extrapolation
    # hub_height_results
    results: list[Results] = pdt.Field(
        ..., description="Assessment results at the measurement location(s)."
    )
    uncertainty_assessment: UncertaintyAssessment = pdt.Field(
        ..., description="Measurement wind resource uncertainty assessment."
    )


class WindResourceAssessmentBasis(pdt.BaseModel):
    """Measurement wind resource assessment basis in a scenario."""

    # TODO - placeholder to be implemented
    pass


# TODO this needs to be completed with more fields for relevant details
class TurbineWindResourceAssessment(pdt.BaseModel):
    """Wind resource assessment at the turbine locations."""

    turbine_wind_resource_results: list[Results] = pdt.Field(
        ..., description="Assessment results at the turbine location(s)."
    )
    wind_spatial_models: list[CalculationModelSpecification] = pdt.Field(
        ..., description="Wind spatial models used in the assessment."
    )
    # TODO should not be optional
    uncertainty_assessment: UncertaintyAssessment | None = pdt.Field(
        None, description="Turbine wind resource uncertainty assessment."
    )


# TODO this needs to be completed with more fields for relevant details
class GrossEnergyAssessment(pdt.BaseModel):
    """Gross energy yield assessment."""

    results: list[Results] = pdt.Field(..., description="Gross energy yield results.")


class PlantPerformanceComponent(pdt.BaseModel):
    """Plant performance assessment component."""

    basis: ComponentAssessmentBasis = pdt.Field(
        ..., description="Basis of plant performance element assessment."
    )
    variability: ComponentVariabilityType = pdt.Field(
        ..., description="Considered variability in plant performance element."
    )
    calculation_models: list[CalculationModelSpecification] | None = pdt.Field(
        None, description="Calculation models used in the assessment."
    )
    results: Results = pdt.Field(
        ..., description="Plant performance assessment component results."
    )


class PlantPerformanceCategory(pdt.BaseModel):
    """Plant performance assessment category."""

    components: list[PlantPerformanceComponent] = pdt.Field(
        ..., description="Plant performance assessment category components."
    )
    category_results: list[Results] = pdt.Field(
        ..., description="Category level assessment results."
    )


class PlantPerformanceAssessment(pdt.BaseModel):
    """Plant performance assessment details and results."""

    categories: dict[
        PlantPerformanceCategoryLabel, PlantPerformanceCategory
    ] = pdt.Field(..., description="Plant performance assessment categories.")
    # TODO remove optional
    net_energy_uncertainty_assessment: UncertaintyAssessment | None = pdt.Field(
        None, description="Net energy uncertainty assessment."
    )
    net_energy_results: list[Results] = pdt.Field(
        ..., description="Net energy yield results at different confidence limits."
    )


class Scenario(pdt.BaseModel):
    """Single unique energy yield assessment scenario."""

    scenario_id: str | None = pdt.Field(
        None,
        description="Unique identifier of the scenario.",
        examples=["3613a846-1e74-4535-ad40-7368f7ad452d"],
    )
    label: str = pdt.Field(
        ..., description="Label of the scenario.", examples=["Sc1", "A", "B01"]
    )
    description: str | None = description_field
    comments: str | None = comments_field
    is_main_scenario: bool | None = pdt.Field(
        None, description="Whether or not this is the main scenario in the report."
    )
    operational_lifetime_length_years: float = pdt.Field(
        ...,
        description="Number of years of project operational lifetime.",
        gt=1.0,
        lt=100.0,
        examples=[10.0, 20.0, 30.0],
    )
    wind_farms: list[WindFarm] = pdt.Field(
        [], description="List of all wind farms included in the scenario."
    )
    wind_resource_assessment_basis: WindResourceAssessmentBasis | None = pdt.Field(
        None, description="Measurement wind resource assessment basis for the scenario."
    )
    turbine_wind_resource_assessment: TurbineWindResourceAssessment | None = pdt.Field(
        None, description="Wind resource assessment at the turbine locations."
    )
    gross_energy_assessment: GrossEnergyAssessment = pdt.Field(
        ..., description="Gross energy yield assessment."
    )
    plant_performance_assessment: PlantPerformanceAssessment = pdt.Field(
        ..., description="Plant performance assessment including net energy results."
    )


class Organisation(pdt.BaseModel):
    """Issuing or receiving organisation of an energy yield assessment."""

    name: str = pdt.Field(
        ...,
        description="Entity name of the organisation.",
        examples=["The Torre Egger Consultants Limited", "Miranda Investments Limited"],
    )
    abbreviation: str | None = pdt.Field(
        None,
        description="Abbreviated name of the organisation.",
        examples=["Torre Egger", "Miranda"],
    )
    address: str | None = pdt.Field(
        None,
        description="Address of the organisation.",
        examples=["5 Munro Road, Summit Centre, Sgurrsville, G12 0YE, UK"],
    )
    contact_name: str | None = pdt.Field(
        None,
        description="Name(s) of contact person(s) in the organisation.",
        examples=["Luis Bunuel", "Miles Davis, John Coltrane"],
    )


class ReportContributor(pdt.BaseModel):
    """Contributor to an energy yield assessment."""

    name: str = pdt.Field(
        ...,
        description="Name of the contributor.",
        examples=["Joan Miro", "Andrei Tarkovsky"],
    )
    email_address: pdt.EmailStr | None = pdt.Field(
        None,
        description="Email address of the contributor.",
        examples=["j.miro@art.cat", "andrei.tarkovsky@cinema.com"],
    )
    contributor_type: Literal["author", "verifier", "approver", "other"] = pdt.Field(
        ..., description="Type of contributor."
    )
    contribution_comments: str | None = pdt.Field(
        None,
        description="Comments to clarify contribution.",
        examples=["Second author"],
    )
    completion_date: dt.date | None = pdt.Field(
        None,
        description="Contribution completion date (format YYYY-MM-DD).",
        examples=["2022-10-04"],
    )


class EnergyYieldAssessment(BaseModelWithRefs):
    """IEC 61400-15-2 EYA DEF energy yield assessment data model."""

    class Config:
        """``EnergyYieldAssessment`` data model configurations."""

        @staticmethod
        def schema_extra(
            schema: dict[str, Any], model: Type[EnergyYieldAssessment]
        ) -> None:
            """Additional items for the model schema."""
            add_null_type_to_schema_optional_fields(schema=schema, model=model)
            schema.update(
                {
                    "$schema": get_json_schema_reference_uri(),
                    "$id": get_json_schema_uri(),
                    "$version": get_json_schema_version(),
                    "title": "IEC 61400-15-2 EYA DEF Data Model",
                    "additionalProperties": False,
                }
            )

    json_uri: str | None = pdt.Field(
        None,
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
    def cast_measurement_stations(cls, v):
        """Cast ``measurement_stations`` as ``MeasurementStationMetadata``.

        :param v: each value passed in the ``measurement_stations`` list
            to the ``EnergyYieldAssessment`` constructor
        :return: the value of ``v`` cast as ``MeasurementStationMetadata``
        """
        return MeasurementStationMetadata(v)

    @classmethod
    def final_json_schema(cls) -> dict:
        """Get a json schema representation of the top-level data model.

        NOTE: there is a known issue with the JSON Schema export
        functionality in pydantic where variables that can be set to
        ``None`` are not correctly set to nullable in the json schema.
        This will likely be resolved in the near term. In the meanwhile,
        json documents should not include ``null`` values, but properties
        with a ``null`` value should rather be excluded.
        """
        schema_dict = cls.schema(by_alias=True)
        properties_exclude = ["$id", "json_uri"]
        for property_exclude in properties_exclude:
            if property_exclude in schema_dict["properties"].keys():
                del schema_dict["properties"][property_exclude]
        schema_dict = reduce_json_schema_all_of(schema_dict)
        defined_fields = ["description", "comments"]
        for field_label in defined_fields:
            schema_dict = move_field_to_definitions(
                json_dict=schema_dict, field_label=field_label
            )
        return schema_dict
