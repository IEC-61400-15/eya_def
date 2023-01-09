"""Pydantic data model for the IEC 61400-15-2 EYA DEF.

This module defines a comprehensive data model for describing an energy
yield assessment (EYA) according to the IEC 61400-15-2 Reporting Digital
Exchange Format (DEF), which is referred to the "EYA DEF data model".
The python implementation makes use of the ``pydantic`` package to
define the model and supports export as a json schema.

Note that a few somewhat ugly temporary fixes have been implemented for
the translation between this data model and json representations of the
schema and model instances. Pydantic version 2 is due to be released
soon, which will likely allow solving some of these issues in a more
robust and elegant way. There will be no effort to improve these fixes
until this package moves to rely on pydantic v2.

"""

from __future__ import annotations

import datetime as dt
from typing import Any, Literal, Mapping, Type

import pydantic as pdt

from eya_def_tools.enums import (
    ComponentAssessmentBasis,
    ComponentVariabilityType,
    PlantPerformanceCategoryLabel,
    ResultsApplicabilityType,
    UncertaintyCategoryLabel,
)
from eya_def_tools.typing import NestedAnnotatedFloatDict
from eya_def_tools.utils.json_schema_utils import (
    add_null_type_to_schema_optional_fields,
    reduce_json_schema_all_of,
)


class JsonPointerRef(str):
    """JSON Pointer reference."""

    def dict(self) -> dict[str, str]:
        """Get a ``dict`` representation of the reference.

        :return: a dict of the form ``{"$ref": "<reference_uri>"}``
        """
        return {"$ref": self.format()}

    def json(self) -> str:
        """Get a json ``str`` representation of the reference.

        :return: a string of the form ``{"$ref": "<reference_uri>"}``
        """
        return '{"$ref": "' + self.format() + '"}'


class BaseModelWithRefs(pdt.BaseModel):
    """Base model variant that includes JSON Pointer references."""

    @classmethod
    def get_ref_field_labels(cls) -> list[str]:
        """Get a list of the field labels that are references."""
        if len(cls.__fields__) == 0:
            return []
        ref_field_labels = []
        for field_key, field_val in cls.__fields__.items():
            if issubclass(field_val.type_, JsonPointerRef):
                ref_field_labels.append(field_key)
        return ref_field_labels

    @pdt.root_validator(pre=True)
    def convert_json_pointer_to_str(cls, values: Mapping[Any, Any]) -> dict[Any, Any]:
        """Convert all JSON Pointer references to ´str´.

        :param values: the pre-validation values (arguments) passed to
            the constructor
        :return: a ``dict`` copy of ``values`` where each JSON Pointer
            reference value of the form ``{"$ref": "<reference>"}`` is
            replaced by the ``str`` value of ``<reference>``
        """
        validated_values = {}
        for key, value in values.items():
            if (
                key in cls.get_ref_field_labels()
                and isinstance(value, dict)
                and len(value) == 1
                and isinstance(list(value.keys())[0], str)
                and list(value.keys())[0] == "$ref"
                and isinstance(list(value.values())[0], str)
            ):
                validated_values[key] = list(value.values())[0]
            elif key in cls.get_ref_field_labels() and isinstance(value, list):
                for item in value:
                    if (
                        isinstance(item, dict)
                        and len(item) == 1
                        and isinstance(list(item.keys())[0], str)
                        and list(item.keys())[0] == "$ref"
                        and isinstance(list(item.values())[0], str)
                    ):
                        if key not in validated_values:
                            validated_values[key] = [list(item.values())[0]]
                        else:
                            validated_values[key].append(list(item.values())[0])
                    else:
                        if key not in validated_values:
                            validated_values[key] = [item]
                        else:
                            validated_values[key].append(item)
            else:
                validated_values[key] = value
        return validated_values

    def dict(self, *args, **kwargs) -> dict:
        """A ``dict`` representation of the model instance.

        :param args: any positional arguments for
            ``pydantic.BaseModel.json``
        :param kwargs: any key-worded arguments for
            ``pydantic.BaseModel.json``
        :return: a ``dict`` representing the model instance
        """
        dict_repr = super().dict(*args, **kwargs)
        for ref_field_label in self.get_ref_field_labels():
            if (
                ref_field_label in dict_repr.keys()
                and dict_repr[ref_field_label] is not None
            ):
                field = getattr(self, ref_field_label)
                if isinstance(field, list):
                    dict_repr[ref_field_label] = []
                    for item in field:
                        dict_repr[ref_field_label].append(item.dict())
                else:
                    dict_repr[ref_field_label] = field.dict()
        return dict_repr

    def json(self, *args, **kwargs) -> str:
        """A json ``str`` representation of the model instance.

        :param args: any positional arguments for
            ``pydantic.BaseModel.json``
        :param kwargs: any key-worded arguments for
            ``pydantic.BaseModel.json``
        :return: a json ``str`` representing the model instance
        """
        json_repr = super().json(*args, **kwargs)
        for ref_field_label in self.get_ref_field_labels():
            field = getattr(self, ref_field_label)
            if isinstance(field, list):
                for item in set(field):
                    raw_ref_str = '"' + item.format() + '"'
                    ref_str = item.json()
                    json_repr = json_repr.replace(raw_ref_str, ref_str)
            else:
                raw_ref_str = '"' + getattr(self, ref_field_label).format() + '"'
                ref_str = getattr(self, ref_field_label).json()
                json_repr = json_repr.replace(raw_ref_str, ref_str)
        return json_repr


def get_json_schema_reference_uri() -> str:
    """Get the reference JSON Schema URI of the EYA DEF JSON Schema.

    :return: the public URI of the JSON Schema reference used
    """
    return "https://json-schema.org/draft/2020-12/schema"


def get_json_schema_uri() -> str:
    """Get the URI of the EYA DEF JSON Schema.

    :return: the public URI of the latest released version of the JSON
        Schema
    """
    # TODO this is a placeholder to be updated (and consider including
    #      version in URI)
    return (
        "https://raw.githubusercontent.com/IEC-61400-15/eya_def/blob/main/"
        "iec_61400-15-2_eya_def.schema.json"
    )


def get_json_schema_version() -> str:
    """Get the current version string of the EYA DEF JSON Schema.

    :return: the semantic version string of the JSON Schema, following
        the format <major>.<minor>.<patch> (e.g. '1.2.3')
    """
    # TODO this is a placeholder to be updated (consider linking to git
    #      repo tags and consider how to distinguish JSON Schema and
    #      python package versions)
    return "0.0.1"


def get_json_schema_title() -> str:
    """Get the EYA DEF JSON Schema title."""
    return "IEC 61400-15-2 EYA DEF Data Model"


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
    description: str | None = pdt.Field(
        None,
        description="Description of the location.",
        examples=[
            "Preliminary location of T1",
        ],
    )
    comments: str | None = pdt.Field(
        None,
        description="Comments regarding the location.",
        examples=["Pending ground investigations"],
    )
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
        if type in field_schema.keys():
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
    description: str = pdt.Field(
        ...,
        description="Description of the operational restriction.",
        examples=[
            (
                "Wind sector management (WSM) curtailment as specified by "
                "the turbine manufacturer"
            )
        ],
    )
    comments: str | None = pdt.Field(
        None, description="Comments regarding the operational restriction."
    )


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
    description: str | None = pdt.Field(
        None,
        description="Description of the turbine configuration.",
        examples=[
            "Turbine specification for T1 in Scenario B",
        ],
    )
    comments: str | None = pdt.Field(
        None,
        description="Comments regarding the turbine configuration.",
        examples=[
            (
                "Preliminary alternative configuration with Unconfirmed "
                "turbine suitability"
            )
        ],
    )
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
    description: str | None = pdt.Field(
        None,
        description="Description of the wind farm.",
        examples=["The third phase of the Summit project"],
    )
    comments: str | None = pdt.Field(
        None, description="Comments regarding the wind farm."
    )
    turbines: list[TurbineSpecification] = pdt.Field(
        ..., description="List of specifications for constituent turbines."
    )
    relevance: Literal["internal", "external", "future"] = pdt.Field(  # TODO use Enum
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
    description: str | None = pdt.Field(
        None,
        description="Description of the model.",
    )
    comments: str | None = pdt.Field(None, description="Comments on the model.")


class ResultsComponent(pdt.BaseModel):
    """Component of a set of results."""

    component_type: str = pdt.Field(  # TODO use Enum
        ...,
        description="Type of results component.",
        examples=["mean", "median", "std", "P90"],
    )
    description: str | None = pdt.Field(
        None, description="Description of the results component."
    )
    comments: str | None = pdt.Field(
        None, description="Comments on the results component."
    )
    values: float | NestedAnnotatedFloatDict = pdt.Field(
        ...,
        description="Result value(s) as simple float or labeled map.",
        examples=[123.4, {"WTG01": 123.4, "WTG02": 143.2}],
    )


class Results(pdt.BaseModel):
    """Single set of results for an element of an energy assessment."""

    label: str = pdt.Field(
        ..., description="Label of the results.", examples=["10-year P50"]
    )
    description: str | None = pdt.Field(
        None,
        description="Description of the results.",
        examples=["10-year wind farm net P50 energy yield."],
    )
    comments: str | None = pdt.Field(
        None,
        description="Comments on the results.",
        examples=["Corresponds to first 10 years of operation."],
    )
    unit: str = pdt.Field(
        ..., description="Unit of result values (TO REPLACE BY LITERAL)."
    )
    applicability_type: ResultsApplicabilityType = pdt.Field(
        ..., description="Applicability type of energy assessment results."
    )
    results_dimensions: list[
        Literal["none", "location", "hub_height", "year", "month", "month_of_year"]
    ] = pdt.Field(..., description="Type of energy assessment results.")
    result_components: list[ResultsComponent] = pdt.Field(
        ..., description="List of result components."
    )


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
    description: str | None = pdt.Field(
        None,
        description="Description of the wind uncertainty component.",
        examples=[
            (
                "Uncertainty associated with the consistency of the "
                "long-term reference data"
            )
        ],
    )
    comments: str | None = pdt.Field(
        None, description="Comments on the wind uncertainty component."
    )
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


# TODO this needs to be completed with more fields for relevant details
class NetEnergyAssessment(pdt.BaseModel):
    """Net energy yield results."""

    results: list[Results] = pdt.Field(
        ..., description="Energy yield results at different confidence limits."
    )
    # TODO remove optional
    uncertainty_assessment: UncertaintyAssessment | None = pdt.Field(
        None, description="Net energy uncertainty assessment."
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
    description: str | None = pdt.Field(
        None,
        description="Description of the scenario.",
        examples=["Main scenario", "XZY220-7.2MW turbine model scenario"],
    )
    comments: str | None = pdt.Field(None, description="Comments on the scenario.")
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
        ..., description="Plant performance assessment including all losses."
    )
    net_energy_assessment: NetEnergyAssessment = pdt.Field(
        ..., description="Net energy yield assessment."
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
                    "title": get_json_schema_title(),
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
    description: str | None = pdt.Field(
        None,
        description="Description of the energy assessment report.",
        examples=[
            (
                "Wind resource and energy yield assessment of the Barefoot "
                "Wind Farm based on one on-site meteorological mast and "
                "considering two different turbine scenarios."
            )
        ],
    )
    comments: str | None = pdt.Field(
        None,
        description="Comments on the energy assessment report.",
        examples=["Update to consider further on-site measurement data."],
    )
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
        if schema_dict is None:
            raise ValueError("the 'schema' method on the class returned 'None'")
        properties_exclude = ["$id", "json_uri"]
        for property_exclude in properties_exclude:
            if property_exclude in schema_dict["properties"].keys():
                del schema_dict["properties"][property_exclude]
        schema_dict = reduce_json_schema_all_of(schema_dict)
        return schema_dict
