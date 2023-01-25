"""Top level pydantic data model for the IEC 61400-15-2 EYA DEF.

"""

from __future__ import annotations

import datetime as dt
from typing import Any, Literal, Type

import pydantic as pdt

from eya_def_tools.data_models.base_models import BaseModelWithRefs, EyaDefBaseModel
from eya_def_tools.data_models.enums import (
    AssessmentBasis,
    PlantPerformanceCategoryLabel,
    UncertaintyCategoryLabel,
    VariabilityType,
)
from eya_def_tools.data_models.fields import comments_field, description_field
from eya_def_tools.data_models.measurement_station import MeasurementStationMetadata
from eya_def_tools.data_models.result import Result
from eya_def_tools.data_models.spatial import CoordinateReferenceSystem
from eya_def_tools.data_models.turbine_model import TurbineModel
from eya_def_tools.data_models.wind_farm import WindFarmConfiguration
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


class ReferenceWindFarm(EyaDefBaseModel):
    """Reference wind farm metadata."""

    # TODO - placeholder to be implemented
    pass


class ReferenceWindFarmBasis(EyaDefBaseModel):
    """Reference wind farm basis in a wind resource assessment."""

    # TODO - placeholder to be implemented
    pass


# TODO add input data sources specification
class CalculationModelSpecification(EyaDefBaseModel):
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
class UncertaintyComponent(EyaDefBaseModel):
    """Wind resource uncertainty assessment component."""

    label: str = pdt.Field(
        ...,
        description="Label of the wind uncertainty component.",
        examples=["Long-term consistency"],
    )
    description: str | None = description_field
    comments: str | None = comments_field
    results: list[Result] = pdt.Field(
        ..., description="Wind resource uncertainty assessment component results."
    )


class UncertaintyCategory(EyaDefBaseModel):
    """Wind resource uncertainty assessment category."""

    components: list[UncertaintyComponent] = pdt.Field(
        ..., description="Wind resource uncertainty assessment components."
    )
    category_results: list[Result] = pdt.Field(
        ..., description="Category level assessment results."
    )


class UncertaintyAssessment(EyaDefBaseModel):
    """Wind resource uncertainty assessment including all components."""

    categories: dict[UncertaintyCategoryLabel, UncertaintyCategory] = pdt.Field(
        ..., description="Wind resource uncertainty assessment categories."
    )


# TODO - to be extended
class WindResourceAssessment(EyaDefBaseModel):
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
    results: list[Result] = pdt.Field(
        ..., description="Assessment results at the measurement location(s)."
    )
    uncertainty_assessment: UncertaintyAssessment = pdt.Field(
        ..., description="Measurement wind resource uncertainty assessment."
    )


class WindResourceAssessmentBasis(EyaDefBaseModel):
    """Measurement wind resource assessment basis in a scenario."""

    # TODO - placeholder to be implemented
    pass


# TODO this needs to be completed with more fields for relevant details
class TurbineWindResourceAssessment(EyaDefBaseModel):
    """Wind resource assessment at the turbine locations."""

    turbine_wind_resource_results: list[Result] = pdt.Field(
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
class GrossEnergyAssessment(EyaDefBaseModel):
    """Gross energy yield assessment."""

    results: list[Result] = pdt.Field(..., description="Gross energy yield results.")


class PlantPerformanceComponent(EyaDefBaseModel):
    """Plant performance assessment component."""

    basis: AssessmentBasis = pdt.Field(
        ..., description="Basis of plant performance element assessment."
    )
    variability: VariabilityType = pdt.Field(
        ..., description="Considered variability in plant performance element."
    )
    calculation_models: list[CalculationModelSpecification] | None = pdt.Field(
        None, description="Calculation models used in the assessment."
    )
    results: Result = pdt.Field(
        ..., description="Plant performance assessment component results."
    )


class PlantPerformanceCategory(EyaDefBaseModel):
    """Plant performance assessment category."""

    components: list[PlantPerformanceComponent] = pdt.Field(
        ..., description="Plant performance assessment category components."
    )
    category_results: list[Result] = pdt.Field(
        ..., description="Category level assessment results."
    )


class PlantPerformanceAssessment(EyaDefBaseModel):
    """Plant performance assessment details and results."""

    categories: dict[
        PlantPerformanceCategoryLabel, PlantPerformanceCategory
    ] = pdt.Field(..., description="Plant performance assessment categories.")
    # TODO remove optional
    net_energy_uncertainty_assessment: UncertaintyAssessment | None = pdt.Field(
        None, description="Net energy uncertainty assessment."
    )
    net_energy_results: list[Result] = pdt.Field(
        ..., description="Net energy yield results at different confidence limits."
    )


class Scenario(EyaDefBaseModel):
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
    wind_farms: list[WindFarmConfiguration] = pdt.Field(
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


class Organisation(EyaDefBaseModel):
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


class ReportContributor(EyaDefBaseModel):
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
            BaseModelWithRefs.Config.schema_extra(schema=schema, model=model)
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
            to the ``EnergyYieldAssessment`` constructor
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
