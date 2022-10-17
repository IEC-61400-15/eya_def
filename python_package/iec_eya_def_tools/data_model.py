# -*- coding: utf-8 -*-
"""Data model for the IEC 61400-15-2 Reporting Digital Exchange Format.

This module defines a comprehensive data model for describing an energy
yield assessment (EYA) according to the IEC 61400-15-2 Reporting Digital
Exchange Format (DEF), which is referred to the "EYA DEF data model" in
short. The python implementation makes use of the `pydantic` package to
define the model and supports export as a json schema.

Note that some temporary fixes have been implemented for the translation
between this data model and json representations of the schema and model
instances. Pydantic version 2 is due to be released soon, which will
likely solve most of these issues in a more robust way.

"""

from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, EmailStr


ResultsApplicabilityType = Literal[  # TODO consider using Enum
    'lifetime', 'any_one_year', 'one_operational_year', 'other']
"""Period of/in time that a set of results are applicable."""


WindUncertaintyCategoryLabel = Literal[  # TODO consider using Enum
    'measurement', 'historical', 'vertical', 'horizontal']
"""Category labels in the wind resource uncertainty assessment."""


PlantPerformanceCategoryLabel = Literal[  # TODO consider using Enum
    'turbine_interaction', 'availability', 'electrical', 'turbine_performance',
    'environmental', 'curtailment', 'other']
"""Category labels in the plant performance assessment."""


PlantPerformanceComponentBasis = Literal[
        'timeseries_calculation', 'distribution_calculation',
        'other_calculation', 'project_specific_estimate',
        'regional_assumption', 'generic_assumption',
        'not_considered', 'other']
"""Basis of component in the plant performance assessment."""


PlantPerformanceComponentVariabilityClass = Literal[
        'static_process', 'annual_variable', 'other']
"""Variability class of component in the plant performance assessment."""


NestedAnnotFloatDict = (
    dict[str, float]
    | dict[str, dict[str, float]]
    | dict[str, dict[str, dict[str, float]]]
    | dict[str, dict[str, dict[str, dict[str, float]]]])
"""Custom type of annotated floats of up to four dimensions."""


def reduce_json_all_of(json_dict: dict) -> dict:
    """Get a copy of a json dict without superfluous ollOf definitions.

    This is a temporary fix and should be resolved when moving to
    pydantic version 2.

    :param json_dict: the original json `dict`
    :return: a `dict` where superfluous ollOf definitions are removed
    """
    reduced_json_dict = {}
    for key, val in json_dict.items():
        if isinstance(val, dict):
            reduced_json_dict[key] = reduce_json_all_of(val)
        elif key == 'allOf' and isinstance(val, list) and len(val) == 1:
            reduced_json_dict.update(val[0].items())
        else:
            reduced_json_dict[key] = val
    return reduced_json_dict


def get_json_schema_reference_uri() -> str:
    """Get the reference schema URI of the json schema.

    :return: the public URI of the schema reference used
    """
    return "https://json-schema.org/draft/2020-12/schema"


def get_json_schema_uri() -> str:
    """Get the URI of the json schema.

    :return: the public URI of the latest released version of the json
        schema
    """
    # TODO this is a placeholder to be updated
    return (
        "https://raw.githubusercontent.com/IEC-61400-15/"
        "energy_yield_reporting_DEF/blob/main/"
        "iec_61400-15-2_reporting_def.schema.json")


def get_json_schema_version() -> str:
    """Get the current version string of the json schema.

    :return: the semantic version string of the schema, following the
        format <major>.<minor>.<patch> (e.g. '1.2.3')
    """
    # TODO this is a placeholder to be updated
    #      (consider using versioneer)
    return "0.0.1"


def get_json_schema_title() -> str:
    """Get the IEC 61400-15-2 Reporting DEF json schema title.

    :return: the title of the json schema.
    """
    return "IEC 61400-15-2 Reporting DEF data model"


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
        description="Notes to clarify contribution.",
        examples=["Second author"])
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


class Location(BaseModel):
    """Specification of a horizontal location in space (x and y)."""
    location_id: str | None = Field(
        None,
        description="Unique identifier of the location.",
        examples=["ee15ff84-6733-4858-9656-ba995d9b1022"])
    location_type: Literal['turbine', 'measurement', 'other'] | None = Field(
        None,
        description="The type of location.")
    label: str = Field(
        ...,
        description="Label of the location.",
        examples=['M1', 'T1', 'WTG02', 'WEA_003', ])
    description: str | None = Field(
        None,
        description="Description of the location.",
        examples=["Verified location of Mast M1", ])
    comments: str | None = Field(
        None,
        description="Comments regarding the location.",
        examples=[(
            "Documented in installation report and independently confirmed")])
    x: float = Field(
        ...,
        description="Location x-coordinate (typically easing).",
        examples=[419665.0])
    y: float = Field(
        ...,
        description="Location y-coordinate (typically northing).",
        examples=[6195240.0])
    coordinate_system: CoordinateSystem = Field(
        ...,
        description="Specification of the coordinate reference system used.")


class JsonPointerRef(str):
    """Json pointer reference."""

    def json(self) -> str:
        """Get a json `str` representation of the reference.

        :return: a string of the form `{"$ref": "<reference_uri>"}`
        """
        return '{"$ref": "' + self.format() + '"}'


class MetadataIEA43ModelRef(JsonPointerRef):
    """IEA Task 43 WRA Data Model reference."""

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(**{
            '$ref': (
                "https://raw.githubusercontent.com/IEA-Task-43/"
                "digital_wra_data_standard/master/schema/"
                "iea43_wra_data_model.schema.json"),
            'title': "Metadata Reference (IEA Task 43 WRA Data Model)",
            'description': (
                "Reference to a json document with measurement metadata "
                "according to the IEA Task 43 WRA data model."),
            'examples': ["https://foo.com/bar/example_iea43.json"]})
        if type in field_schema.keys():
            del field_schema['type']


class WindMeasurementCampaign(BaseModel):
    """Details of a wind measurement campaign."""
    measurement_id: str = Field(
        ...,
        description="Measurement unique ID.",
        examples=["BF_M1_1.0.0"])
    name: str = Field(
        ...,
        description=(
            "Measurement name for use as label; when including a "
            "'metadata_ref_iea43_model', it is recommended this value "
            "matches the 'name' field of the 'measurement_location'."),
        examples=["Mast M1"])
    label: str | None = Field(
        None,
        description="Measurement label (if not provided name is used).",
        examples=["M1"])
    description: str | None = Field(
        None,
        description="Measurement description.",
        examples=["Barefoot Wind Farm on-site meteorological mast"])
    comments: str | None = Field(
        None,
        description="Measurement comments.",
        examples=["Measurements were still ongoing at time of assessment"])
    location: Location = Field(
        ...,
        description="Horizontal location of the measurement equipment.")
    metadata_ref_iea43_model: MetadataIEA43ModelRef | None = Field(
        None,
        title="Metadata Reference (IEA Task 43 WRA Data Model)",
        description=(
            "Reference to a json document with measurement metadata "
            "according to the IEA Task 43 WRA data model."),
        examples=["https://foo.com/bar/example_iea43.json"])

    def dict(self, *args, **kwargs) -> dict:
        """A `dict` representation of the model instance.

        :param args: any positional arguments for `BaseModel.json`
        :param kwargs: any key-worded arguments for `BaseModel.json`
        :return: a `dict` representing the model instance
        """
        dict_repr = super(WindMeasurementCampaign, self).dict(*args, **kwargs)
        if self.metadata_ref_iea43_model:
            dict_repr['metadata_ref_iea43_model'] = (
                self.metadata_ref_iea43_model.json())
        return dict_repr

    def json(self, *args, **kwargs) -> str:
        """A json `str` representation of the model instance.

        :param args: any positional arguments for `BaseModel.json`
        :param kwargs: any key-worded arguments for `BaseModel.json`
        :return: a json `str` representing the model instance
        """
        json_repr = super(WindMeasurementCampaign, self).json(*args, **kwargs)
        if self.metadata_ref_iea43_model:
            raw_metadata_ref_iea43_model_str = (
                '"' + self.metadata_ref_iea43_model.format() + '"')
            metadata_ref_iea43_model_str = self.metadata_ref_iea43_model.json()
            json_repr = json_repr.replace(
                raw_metadata_ref_iea43_model_str, metadata_ref_iea43_model_str)
        return json_repr


class TurbineModelPerfSpecRef(JsonPointerRef):
    """Turbine model performance specification reference (PLACEHOLDER)."""

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(**{
            '$ref': (
                "https://foo.bar.com/baz/wtg_model.schema.json"),
            'title': "Turbine Model Performance Specification Reference",
            'description': (
                "Reference to a json document with turbine model "
                "performance specification (PLACEHOLDER)."),
            'examples': ["https://foo.com/bar/example_wtg_model.json"]})
        if type in field_schema.keys():
            del field_schema['type']


class TurbineModel(BaseModel):
    """Specification of a wind turbine model."""
    label: str = Field(
        ...,
        description="Label of the turbine model.",
        examples=["V172-7.2 MW", "N175/6.X", "SG 6.6-170", "E-175 EP5"])
    perf_spec_ref: TurbineModelPerfSpecRef | None = Field(
        None,
        title="Turbine Model Performance Specification Reference",
        description=(
            "Reference to a json document with turbine model "
            "performance specification (PLACEHOLDER)."),
        examples=["https://foo.com/bar/example_wtg_model.json"])

    def dict(self, *args, **kwargs) -> dict:
        """A `dict` representation of the model instance.

        :param args: any positional arguments for `BaseModel.json`
        :param kwargs: any key-worded arguments for `BaseModel.json`
        :return: a `dict` representing the model instance
        """
        dict_repr = super(TurbineModel, self).dict(*args, **kwargs)
        if self.perf_spec_ref:
            dict_repr['perf_spec_ref'] = self.perf_spec_ref.json()
        return dict_repr

    def json(self, *args, **kwargs) -> str:
        """A json `str` representation of the model instance.

        :param args: any positional arguments for `BaseModel.json`
        :param kwargs: any key-worded arguments for `BaseModel.json`
        :return: a json `str` representing the model instance
        """
        json_repr = super(TurbineModel, self).json(*args, **kwargs)
        if self.perf_spec_ref:
            raw_perf_spec_ref_str = '"' + self.perf_spec_ref.format() + '"'
            perf_spec_ref_str = self.perf_spec_ref.json()
            json_repr = (
                json_repr.replace(raw_perf_spec_ref_str, perf_spec_ref_str))
        return json_repr


class OperationalRestriction(BaseModel):
    """Specifications of an operational restriction for a wind farm."""
    label: str = Field(
        ...,
        description="Label of the operational restriction.",
        examples=["WSM curtailment", "MEC curtailment"])
    description: str = Field(
        ...,
        description="Description of the operational restriction.",
        examples=[(
            "Wind sector management (WSM) curtailment as specified by "
            "the turbine manufacturer")])
    comments: str | None = Field(
        None,
        description="Comments regarding the operational restriction.")


class WindFarm(BaseModel):
    """A collection of wind turbines considered as one unit (plant)."""
    name: str = Field(
        ...,
        description="Name of the wind farm.",
        examples=["Barefoot Wind Farm", "Project Summit Phase III"])
    label: str | None = Field(
        None,
        description="Abbreviated label of the wind farm.",
        examples=["BWF", "Summit PhIII"])
    description: str | None = Field(
        None,
        description="Description of the wind farm.",
        examples=["The third phase of the Summit project"])
    comments: str | None = Field(
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
    turbine_ids: list[str] = Field(
        ...,
        description="List of turbine IDs that form part of the wind farm.",
        examples=[['WTG01-V1.0', 'WTG02-V1.0']])
    turbine_location_maps: list[dict[str, Location]] = Field(
        ...,
        description=(
            "Maps to associate each turbine IDs with a location."
            "TO REPLACE OBJECT BY REFERENCE."))
    turbine_model_maps: list[dict[str, TurbineModel]] = Field(
        ...,
        description=(
            "Maps to associate each turbine IDs with a model. "
            "TO REPLACE OBJECT BY REFERENCE."))
    turbine_hub_height_maps: list[dict[str, float]] = Field(
        ...,
        description=(
            "Maps to associate each turbine IDs with a hub height."
            "TO REPLACE OBJECT BY REFERENCE."))
    operational_restrictions: list[OperationalRestriction] | None = Field(
        None,
        description="List of operational restrictions for the wind farm.")


class SiteWindFarmsConfiguration(BaseModel):
    """Configuration of all relevant wind farms for the site."""
    label: str = Field(
        ...,
        description="The wind farms configuration label.",
        examples=["B"])
    description: str | None = Field(
        None,
        description="The wind farms configuration description.",
        examples=["Wind farms configuration for turbine model scenario B."])
    comments: str | None = Field(
        None,
        description="Comments regarding the wind farms configuration.",
        examples=[(
            "This wind farms configuration is identical to that for "
            "Scenario A, except for the different turbine model "
            "configuration.")])
    wind_farms: list[WindFarm] = Field(
        ...,
        description="List of wind farms belonging to the configuration.")


class CalculationModelSpecification(BaseModel):
    """Specification of a model used in an energy assessment."""
    name: str = Field(
        ...,
        description="Name of the model.",
        examples=["WAsP", "VORTEX BLOCKS", "DNV CFD", "VENTOS/M"])
    description: str | None = Field(
        None,
        description="Description of the model.",)
    comments: str | None = Field(
        None,
        description="Comments on the model.")
    # TODO add input data sources specification


class ResultsComponent(BaseModel):
    """Component of a set of results."""
    component_type: str = Field(
        ...,
        description="Type of results component (TO REPLACE BY LITERAL).",
        examples=["mean", "median", "std", 'P90'])
    description: str | None = Field(
        None,
        description="Description of the results component.")
    comments: str | None = Field(
        None,
        description="Comments on the results component.")
    values: float | NestedAnnotFloatDict = Field(
        ...,
        description="Result value(s) as simple float or labeled map.",
        examples=[123.4, {'WTG01': 123.4, 'WTG02': 143.2}])


class Results(BaseModel):
    """Single set of results for an element of an energy assessment."""
    label: str = Field(
        ...,
        description="Label of the results.",
        examples=["10-year P50"])
    description: str | None = Field(
        None,
        description="Description of the results.",
        examples=["10-year wind farm net P50 energy yield."])
    comments: str | None = Field(
        None,
        description="Comments on the results.",
        examples=["Corresponds to first 10 years of operation."])
    unit: str = Field(
        ...,
        description="Unit of result values (TO REPLACE BY LITERAL).")
    applicability_type: ResultsApplicabilityType = Field(
            ...,
            description="Applicability type of energy assessment results.")
    results_dimensions: list[Literal[
        'none', 'location', 'hub_height',
        'year', 'month', 'month_of_year']] = Field(
            ...,
            description="Type of energy assessment results.")
    result_components: list[ResultsComponent] = Field(
        ...,
        description="List of result components.")


class WindUncertaintyComponent(BaseModel):
    """Wind resource uncertainty assessment component."""
    results: Results = Field(
        ...,
        description="Wind resource uncertainty assessment component results.")
    # TODO this needs to be completed with more fields for relevant details


class WindUncertaintyCategory(BaseModel):
    """Wind resource uncertainty assessment category."""
    components: list[WindUncertaintyComponent] = Field(
            ...,
            description="Wind resource uncertainty assessment components.")
    category_results: list[Results] = Field(
            ...,
            description="Category level assessment results.")


class WindUncertaintyAssessment(BaseModel):
    """Wind resource uncertainty assessment including all components."""
    categories: dict[
        WindUncertaintyCategoryLabel, WindUncertaintyCategory] = Field(
            ...,
            description="Wind resource uncertainty assessment categories.")


class WindResourceAssessment(BaseModel):
    """Wind resource assessment details and results."""
    measurement_wind_resource_results: list[Results] = Field(
        ...,
        description="Assessment results at the measurement location(s).")
    turbine_wind_resource_results: list[Results] = Field(
        ...,
        description="Assessment results at the turbine location(s).")
    wind_spatial_models: list[CalculationModelSpecification] = Field(
        ...,
        description="Wind spatial models used in the assessment.")
    uncertainty_assessment: WindUncertaintyAssessment = Field(
        ...,
        description="Wind resource uncertainty assessment.")
    # TODO this needs to be completed with more fields for relevant details


class ReferenceTurbineAssessment(BaseModel):
    """Reference operational turbine assessment (PLACEHOLDER)."""
    pass  # TODO temporary placeholder


class GrossEnergyAssessment(BaseModel):
    """Gross energy yield assessment."""
    results: list[Results] = Field(
        ...,
        description="Gross energy yield results.")


class PlantPerformanceComponent(BaseModel):
    """Plant performance assessment component."""
    basis: PlantPerformanceComponentBasis = Field(
            ...,
            description="Basis of plant performance element assessment.")
    variability: PlantPerformanceComponentVariabilityClass = Field(
            ...,
            description="Considered variability in plant performance element.")
    calculation_models: list[CalculationModelSpecification] | None = Field(
        None,
        description="Calculation models used in the assessment.")
    results: Results = Field(
        ...,
        description="Plant performance assessment component results.")


class PlantPerformanceCategory(BaseModel):
    """Plant performance assessment category."""
    components: list[PlantPerformanceComponent] = Field(
            ...,
            description="Plant performance assessment category components.")
    category_results: list[Results] = Field(
            ...,
            description="Category level assessment results.")


class PlantPerformanceAssessment(BaseModel):
    """Plant performance assessment details and results."""
    categories: dict[
        PlantPerformanceCategoryLabel, PlantPerformanceCategory] = Field(
            ...,
            description="Plant performance assessment categories.")


class NetEnergyAssessment(BaseModel):
    """Net energy yield results."""
    results: list[Results] = Field(
        ...,
        description="Energy yield results at different confidence limits.")
    # TODO this needs to be completed with more fields for relevant details


class EnergyAssessment(BaseModel):
    """Energy assessment details and results for a scenario."""
    label: str = Field(
        ...,
        description="Label of the assessment.",
        examples=["Scenario A EYA"])
    description: str = Field(
        ...,
        description="Description of the assessment.",
        examples=["Energy yield assessment details for Scenario A."])
    comments: str | None = Field(
        None,
        description="Comments on the assessment.",
        examples=[(
            "The Scenario B assessment should be considered indicative "
            "only due to potentially inaccurate assumptions.")])
    wind_resource_assessment: WindResourceAssessment | None = Field(
        None,  # Optional as the basis can also be operational data
        description="Wind resource assessment based on wind measurements.")
    reference_turbine_assessment: ReferenceTurbineAssessment | None = Field(
        None,  # Optional as the basis can also be measurement data
        description="Reference operational turbine assessment.")
    gross_energy_assessment: GrossEnergyAssessment = Field(
        ...,
        description="Gross energy yield assessment.")
    plant_performance_assessment: PlantPerformanceAssessment = Field(
        ...,
        description="Plant performance assessment including all losses.")
    net_energy_assessment: NetEnergyAssessment = Field(
        ...,
        description="Net energy yield assessment.")


class Scenario(BaseModel):
    """Single unique scenario of energy assessment."""
    label: str = Field(
        ...,
        description="Label of the scenario.",
        examples=["Sc1", "A", "B01"])
    description: str | None = Field(
        None,
        description="Description of the scenario.",
        examples=["Main scenario", "XZY220-7.2MW turbine model scenario"])
    comments: str | None = Field(
        None,
        description="Comments on the scenario.")
    is_main_scenario: bool | None = Field(
        None,
        description="Whether or not this is the main scenario in the report.")
    operational_lifetime_length_years: float = Field(
        ...,
        description="Number of years of project operational lifetime.",
        gt=1.0,
        lt=100.0,
        examples=[10.0, 20.0, 30.0])
    wind_measurement_campaigns: list[WindMeasurementCampaign] = Field(
        ...,
        description="Details of the wind measurement campaign.")
    wind_farms_configuration: SiteWindFarmsConfiguration = Field(
        ...,
        description="Configuration of all relevant wind farms for the site.")
    energy_assessment: EnergyAssessment = Field(
        ...,
        description="Energy assessment for the scenario.")


class EnergyAssessmentReport(BaseModel):
    """IEC 61400-15-2 Reporting DEF energy assessment report data model."""

    class Config:
        """EnergyAssessmentReport data model configurations."""

        schema_extra = {
            '$schema': get_json_schema_reference_uri(),
            '$id': get_json_schema_uri(),
            '$version': get_json_schema_version(),
            'title': get_json_schema_title()}

    json_doc_id: str | None = Field(
        None,
        description="Unique ID of json document.",
        examples=[(
            "https://foo.bar.com/api/eya_report?"
            "id=8f46a815-8b6d-4870-8e92-c031b20320c6.json")],
        alias='$id')
    title: str = Field(
        ...,
        description="Title of the energy assessment report.",
        examples=["Energy yield assessment of the Barefoot Wind Farm"])
    description: str | None = Field(
        None,
        description="Description of the energy assessment report.",
        examples=[(
            "Wind resource and energy yield assessment of the Barefoot "
            "Wind Farm based on one on-site meteorological mast and "
            "considering two different turbine scenarios.")])
    comments: str | None = Field(
        None,
        description="Comments on the energy assessment report.",
        examples=["Update to consider further on-site measurement data."])
    project_name: str = Field(
        ...,
        description="Name of the project under assessment.",
        examples=["Barefoot Wind Farm"])
    document_id: str | None = Field(
        None,
        title="Document ID",
        description=(
            "The ID of the report document; when including a "
            "document_version, do not duplicate the version here"),
        examples=["C385945/A/UK/R/002", "0345.923454.0001"])
    document_version: str | None = Field(
        None,
        description="Version of the report document.",
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
    confidentiality_classification: str | None = Field(
        None,
        description="Confidentiality classification of the report.",
        examples=["Confidential", "Commercial in confidence"])
    scenarios: list[Scenario] = Field(
        ...,
        description="List of scenarios included in the report")

    @classmethod
    def final_json_schema(cls) -> dict:
        """Get a json schema representation of the top-level data model.

        NOTE: there is a known issue with the json schema export
        functionality in pydantic where variables that can be set to `None`
        are not correctly set to nullable in the json schema. This will
        likely be resolved in the near term. In the meanwhile, json
        documents should not include `null` values, but properties with a
        `null` value should rather be excluded.
        """
        schema_dict = cls.schema(by_alias=True)
        assert bool(schema_dict)
        assert isinstance(schema_dict, dict)
        schema_key_order = [
            '$schema', '$id', '$version', 'title', 'description', 'type',
            'properties', 'required', 'additionalProperties', 'definitions']
        updated_schema_dict = {}
        for key in schema_key_order:
            if key in schema_dict:
                updated_schema_dict[key] = schema_dict.pop(key)
        properties_exclude = ['$id', 'json_doc_id']
        for property_exclude in properties_exclude:
            if property_exclude in updated_schema_dict['properties'].keys():
                del updated_schema_dict['properties'][property_exclude]
        updated_schema_dict = reduce_json_all_of(updated_schema_dict)
        return updated_schema_dict
