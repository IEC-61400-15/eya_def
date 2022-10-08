# -*- coding: utf-8 -*-
"""Data model for the IEC 61400-15-2 Reporting Digital Exchange Format.

This module defines a comprehensive data model for describing an energy
yield assessment (EYA) according to the IEC 61400-15-2 Reporting Digital
Exchange Format (DEF), which is referred to the "EYA DEF data model" in
short. The python implementation makes use of the `pydantic` package to
define the model and supports export as a json schema.

"""

from pathlib import Path
from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, EmailStr
import json


def get_json_schema_version() -> str:
    """Get the version string of the json schema.

    :return: the semantic version string of the schema, following the
        format <major>.<minor>.<patch> (e.g. '1.2.3')
    """
    return "0.0.1"  # TODO this is a placeholder to be updated


class ReportContributor(BaseModel):
    """Contributor to a report ."""
    name: str = Field(
        ...,
        description="Name of the author.",
        examples=["Joan Miro", "Andrei Tarkovsky"])
    email_address: EmailStr | None = Field(
        None,
        description="Email address of the author.",
        examples=["j.miro@art.cat", "andrei.tarkovsky@cinema.com"])
    contributor_type: Literal[
        'author', 'verifier', 'approver', 'other'] = Field(
            ...,
            description="Type of contributor.")
    contribution_notes: str | None = Field(
        None,
        description="Notes to clarify contribution.")
    completion_date: date | None = Field(
        None,
        description="Contribution completion date (format YYYY-MM-DD).",
        examples=["2022-10-04"])


class CoordinateSystem(BaseModel):
    """Specification of a coordinate reference system for GIS data."""
    system_label: str = Field(
        ...,
        description="Label of the coordinate system.",
        examples=["OSGB36 / British National Grid", "SWEREF99 TM"])
    epsg_number: int | None = Field(
        None,
        description="EPSG integer code to identify the coordinate system.",
        examples=[27700, 3006])


class TurbineModel(BaseModel):
    """Specification of a wind turbine model."""
    turbine_model_label: str = Field(
        ...,
        description="Label of the turbine model.",
        examples=["V172-7.2 MW", "N175/6.X", "SG 6.6-170", "E-175 EP5"])


class Turbine(BaseModel):
    """Turbine representation with location and performance data."""
    turbine_label: str = Field(
        ...,
        description="Label of the turbine.",
        examples=['T1', 'WTG02', 'WEA_003'])
    x: float = Field(
        ...,
        description="Wind turbine x-coordinate.")
    y: float = Field(
        ...,
        description="Wind turbine y-coordinate.")
    hub_height: float = Field(
        ...,
        description="Hub height of the turbine.",
        examples=[80.0, 145.0, 169.5])
    turbine_model: TurbineModel = Field(
        ...,
        description="Specification of the turbine model.")


class WindFarm(BaseModel):
    """A collection of wind turbines considered as one unit (plant).

    :ivar label: wind farm label
    :ivar turbines: list of the `Turbine` instances belonging to the
        wind farm
    :ivar relevance: whether the wind farm is relevant as is internal,
        external or future
    """
    wind_farm_name: str = Field(
        ...,
        description="Name of the wind farm.",
        examples=["Barefoot Wind Farm", "Project Summit Phase III"])
    wind_farm_label: str | None = Field(
        None,
        description="Abbreviated label of the wind farm.",
        examples=["BWF", "Summit PhIII"])
    wind_farm_description: str | None = Field(
        None,
        description="Description of the wind farm.",
        examples=["The third phase of the Summit project"])
    wind_farm_comments: str | None = Field(
        None,
        description="Comments regarding the wind farm.")
    relevance: Literal['internal', 'external', 'future'] = Field(
        ...,
        description="The relevance of the wind farm for the assessment.")
    operational_lifetime_start_date: date | None = Field(
        None,
        description="Operational lifetime start date (format YYYY-MM-DD).",
        examples=["2026-01-01", "2017-04-01"])
    operational_lifetime_end_date: date | None = Field(
        None,
        description="Operational lifetime end date (format YYYY-MM-DD).",
        examples=["2051-03-31", "2025-12-31"])
    turbines: list[Turbine] = Field(
        ...,
        description="List of turbines that form part of the wind farm.")
    coordinate_system: CoordinateSystem = Field(
        ...,
        description="Specification of the coordinate reference system used.")


class SiteWindFarmsConfiguration(BaseModel):
    """Configuration of all relevant wind farms for the site."""
    wind_farms_configuration_label: str = Field(
        ...,
        description="The wind farms configuration label.")
    wind_farms_configuration_description: str | None = Field(
        None,
        description="The wind farms configuration description.")
    wind_farms_configuration_comments: str | None = Field(
        None,
        description="Comments regarding the wind farms configuration.")
    wind_farms: list[WindFarm] = Field(
        ...,
        description="List of wind farms belonging to the configuration.")


class WindSpatialModel(BaseModel):
    """Wind spatial model used in the assessment."""
    model_name: str = Field(
        ...,
        description="Name of the wind spatial model.",
        examples=["WAsP", "VORTEX BLOCKS", "DNV CFD", "VENTOS/M"])
    model_description: str | None = Field(
        None,
        description="Description of the wind spatial model.",)
    model_comments: str | None = Field(
        None,
        description="Comments on the wind spatial model.")


class MastWindResourceResults(BaseModel):
    """Wind resource assessment results at the measurement(s)."""
    pass  # TODO temporary placeholder


class TurbineWindResourceResults(BaseModel):
    """Wind resource assessment results at turbines."""
    pass  # TODO temporary placeholder


class GrossEnergyResults(BaseModel):
    """Gross energy yield results."""
    pass  # TODO temporary placeholder


class PlantPerformanceResults(BaseModel):
    """Plant performance results including all losses."""
    pass  # TODO temporary placeholder


class NetEnergyResults(BaseModel):
    """Net energy yield results."""
    pass  # TODO temporary placeholder


class UncertaintyResults(BaseModel):
    """Results of uncertainty analysis."""
    pass  # TODO temporary placeholder


class ConfidenceLimitResults(BaseModel):
    """Energy yield results at different confidence limits."""
    pass  # TODO temporary placeholder


class EnergyAssessmentResults(BaseModel):
    """A single set of energy assessment results for a scenario"""
    results_type: Literal[
        'lifetime', 'any_one_year', 'one_operational_year', 'other'] = Field(
        ...,
        description="Type of energy assessment results.")
    results_label: str = Field(
        ...,
        description="Label of the results.",
        examples=["10-year"])
    results_description: str = Field(
        ...,
        description="Description of the results.",
        examples=["First 10 years of operation"])
    results_comments: str | None = Field(
        None,
        description="Comments on the results.")
    mast_wind_resource_results: MastWindResourceResults | None = Field(
        None,  # Optional as the basis can also be operational data
        description="Wind resource assessment results at the measurement(s).")
    turbine_wind_resource_results: TurbineWindResourceResults | None = Field(
        None,  # Optional as it may not be used with operational data
        description="Wind resource assessment results at turbines.")
    gross_energy_results: GrossEnergyResults = Field(
        ...,
        description="Gross energy yield results.")
    plant_performance_results: PlantPerformanceResults = Field(
        ...,
        description="Plant performance results including all losses.")
    net_energy_results: NetEnergyResults = Field(
        ...,
        description="Net energy yield results.")
    uncertainty_results: UncertaintyResults = Field(
        ...,
        description="Results of uncertainty analysis.")
    confidence_limit_results: ConfidenceLimitResults = Field(
        ...,
        description="Energy yield results at different confidence limits.")


class Scenario(BaseModel):
    """Single unique scenario of energy assessment."""
    scenario_label: str = Field(
        ...,
        description="Label of the scenario.",
        examples=["Sc1", "A", "B01"])
    scenario_description: str | None = Field(
        None,
        description="Description of the scenario.",
        examples=["Main scenario", "XZY220-7.2MW turbine model scenario"])
    scenario_comments: str | None = Field(
        None,
        description="Comments on the scenario.")
    is_main_scenario: bool = Field(
        ...,
        description="Whether or not this is the main scenario in the report.")
    operational_lifetime_length_years: float = Field(
        ...,
        description="Number of years of project operational lifetime.",
        gt=1.0,
        lt=100.0,
        examples=[10.0, 20.0, 30.0])
    wind_farms_configuration: SiteWindFarmsConfiguration = Field(
        ...,
        description="Configuration of all relevant wind farms for the site.")
    wind_spatial_models: list[WindSpatialModel] = Field(
        ...,
        description="Wind spatial models used in the assessment.")
    energy_assessment_results: list[EnergyAssessmentResults] = Field(
        ...,
        description="Energy assessment results for the scenario")


class EnergyAssessmentReport(BaseModel):
    """IEC 61400-15-2 Reporting DEF energy assessment report data model."""

    class Config:
        """EnergyAssessmentReport data model configurations."""
        schema_extra = {
            '$schema': "https://json-schema.org/draft/2020-12/schema",
            '$id': ("https://raw.githubusercontent.com/IEC-61400-15/"
                    "energy_yield_reporting_DEF/blob/main/"
                    "iec_61400-15-2_reporting_def.schema.json"),
            '$version': get_json_schema_version(),
            'title': "IEC 61400-15-2 Reporting DEF data model",
            'additionalProperties': True}

    project_name: str = Field(
        ...,
        description="Name of the project under assessment.",
        examples=["Barefoot Wind Farm"])
    report_title: str = Field(
        ...,
        description="Title of the energy assessment report.",
        examples=["Energy yield assessment of the Barefoot Wind Farm"])
    report_description: str | None = Field(
        None,
        description="Description of the energy assessment report.")
    report_comments: str | None = Field(
        None,
        description="Comments on the energy assessment report.")
    document_id: str | None = Field(
        None,
        description="Report document ID.",
        examples=["C385945/A/UK/R/002/E"])
    document_version: str = Field(
        None,
        description="Report version (avoid duplicating from `document_id`).",
        examples=["1.2.3", "A", "Rev. A"])
    issue_date: date = Field(
        ...,
        description="Report issue date (format YYYY-MM-DD).",
        examples=["2022-10-05"])
    issuing_organisation_name: str = Field(
        ...,
        description="Entity name of the organisation issuing the report.",
        examples=["The Natural Power Consultants Limited"])
    issuing_organisation_abbreviation: str = Field(
        ...,
        description="Abbreviated name of issuing organisation.",
        examples=["Natural Power", "DNV", "Brightwind", "NREL"])
    issuing_organisation_address: str | None = Field(
        None,
        description="Address of organisation issuing the report.")
    receiving_organisation_name: str | None = Field(
        None,
        description="Entity name of the organisation receiving the report.",
        examples=["Cubico Sustainable Investments Limited"])
    receiving_organisation_abbreviation: str | None = Field(
        None,
        description="Abbreviated name of receiving organisation.",
        examples=["Cubico", "Apex", "COP"])
    receiving_organisation_contact_name: str | None = Field(
        None,
        description="Name(s) of contact person(s) in receiving organisation.",
        examples=["Luis Bunuel", "Miles Davis, John Coltrane"])
    receiving_organisation_address: str | None = Field(
        None,
        description="Address of organisation receiving the report.")
    contributors: list[ReportContributor] = Field(
        ...,
        description="List of report contributors (e.g. author and verifier)")
    report_confidentiality_classification: str | None = Field(
        None,
        description="Confidentiality classification of the report.",
        examples=["Confidential", "Commercial in confidence"])
    scenarios: list[Scenario] = Field(
        ...,
        description="List of scenarios included in the report")


def export_json_schema(filepath: Path) -> None:
    """Export the top-level data model to a json schema.

    NOTE: there is a known issue with the json schema export
    functionality in pydantic where variables that can be set to `None`
    are not correctly set to nullable in the json schema. This will
    likely be resolved in the near term. In the meanwhile, json
    documents should not include `null` values, but properties with a
    `null` value should rather be excluded.

    :param filepath: the path of the file to export to
    """
    schema_dict = EnergyAssessmentReport.schema()
    schema_key_order = [
        '$schema', '$id', '$version', 'title', 'description', 'type',
        'properties', 'required', 'additionalProperties', 'definitions']
    sorted_schema_dict = {}
    for key in schema_key_order:
        if key in schema_dict:
            sorted_schema_dict[key] = schema_dict.pop(key)
    for key, val in schema_dict.items():
        sorted_schema_dict[key] = val
        print(key, val)
    with open(filepath, 'w') as f:
        f.write(json.dumps(sorted_schema_dict, indent=2))


# export_json_schema(Path("../iec_61400-15-2_reporting_def.schema.json"))
