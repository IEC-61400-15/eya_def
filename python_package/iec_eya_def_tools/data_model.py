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
from typing import List, Literal
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
    email_address: EmailStr = Field(
        None,
        description="Email address of the author.",
        examples=["j.miro@art.cat", "andrei.tarkovsky@cinema.com"])
    contributor_type: Literal[
        'author', 'verifier', 'approver', 'other'] = Field(
            ...,
            description="Type of contributor.")
    contribution_notes: str = Field(
        None,
        description="Notes to clarify contribution.")
    completion_date: date = Field(
        None,
        description="Contribution completion date in the format YYYY-MM-DD.",
        examples=["2022-10-04"])


class CoordinateSystem(BaseModel):
    """Specification of a coordinate reference system for GIS data."""
    system_label: str = Field(
        ...,
        description="Label of the coordinate system.",
        examples=["OSGB36 / British National Grid", "SWEREF99 TM"])
    epsg_number: int = Field(
        None,
        description="EPSG integer code to identify the coordinate system.",
        examples=[27700, 3006])


class TurbineModel(BaseModel):
    """Specification of a wind turbine model."""
    pass


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
    coordinate_reference_system: CoordinateSystem = Field(
        ...,
        description="Specification of the coordinate reference system used.")
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
    wind_farm_label: str = Field(
        ...,
        description="Label of the wind farm.",
        examples=["Barefoot Wind Farm", "Project Summit Phase III"])
    turbines: List[Turbine] = Field(
        ...,
        description="List of turbines that form part of the wind farm.")
    relevance: Literal['internal', 'external', 'future'] = Field(
        ...,
        description="The relevance of the wind farm for the assessment.")


class WindFarmsConfiguration(BaseModel):
    """Configuration of all relevant wind farms for the site."""
    wind_farms_configuration_label: str = Field(
        ...,
        description="The wind farms configuration label.")
    wind_farms_configuration_comments: str = Field(
        ...,
        description="Comments regarding the wind farms configuration.")
    wind_farms: List[WindFarm] = Field(
        ...,
        description="List of wind farms belonging to the configuration.")


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
        description="Label of the results",
        examples=["10-year"])
    results_description: str = Field(
        ...,
        description="Description of the results",
        examples=["First 10 years of operation"])
    results_comments: str = Field(
        None,
        description="Comments on the results")
    mast_wind_resource_results: MastWindResourceResults = Field(
        None,  # Optional as the basis can also be operational data
        description="Wind resource assessment results at the measurement(s).")
    turbine_wind_resource_results: TurbineWindResourceResults = Field(
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
    project_lifetime_length_years: float = Field(
        ...,
        description="Number of years of project lifetime considered.",
        gt=1.0,
        lt=100.0,
        examples=[10.0, 20.0, 30.0])
    project_lifetime_start_date: date = Field(
        None,
        description="Project lifetime start date in the format YYYY-MM-DD.",
        examples=["2023-01-01", "2017-04-01"])
    wind_farms_configuration: WindFarmsConfiguration = Field(
        ...,
        description="Configuration of all relevant wind farms for the site.")
    energy_assessment_results: List[EnergyAssessmentResults] = Field(
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
    report_description: str = Field(
        None,
        description="Description of the energy assessment report.")
    report_comments: str = Field(
        None,
        description="Comments on the energy assessment report.")
    document_id: str = Field(
        None,
        description="Report document ID.",
        examples=["C385945/A/UK/R/002/E"])
    document_version: str = Field(
        None,
        description="Report version (avoid duplicating from `document_id`).",
        examples=["1.2.3", "A", "Rev. A"])
    issue_date: date = Field(
        ...,
        description="Report issue date in the format YYYY-MM-DD.",
        examples=["2022-10-05"])
    issuing_organisation: str = Field(
        ...,
        description="Organisation issuing the report.",
        examples=["DNV", "Natural Power", "Brightwind", "NREL"])
    issuing_organisation_address: str = Field(
        None,
        description="Address of organisation issuing the report.")
    receiving_organisation: str = Field(
        None,
        description="Organisation receiving the report.",
        examples=["Cubico", "Apex", "COP"])
    receiving_organisation_contact_name: str = Field(
        None,
        description="Name(s) of contact person(s) in receiving organisation.",
        examples=["Luis Bunuel", "Miles Davis, John Coltrane"])
    receiving_organisation_address: str = Field(
        None,
        description="Address of organisation receiving the report.")
    contributors: List[ReportContributor] = Field(
        ...,
        description="List of report contributors (e.g. author and verifier)")
    report_confidentiality_classification: str = Field(
        None,
        description="Confidentiality classification of the report.",
        examples=["Confidential", "Commercial in confidence"])
    scenarios: List[Scenario] = Field(
        ...,
        description="List of scenarios included in the report")


def export_json_schema(filepath: Path) -> None:
    """Export the top-level data model to a json schema.

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


export_json_schema(Path("../iec_61400-15-2_reporting_def.schema.json"))
