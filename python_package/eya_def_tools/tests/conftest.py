# -*- coding: utf-8 -*-
"""Setup and fixtures for the entire `eya_def_tools` test module.

"""

import pytest
import json
from pathlib import Path

import eya_def_tools.data_model as data_model


TEST_INPUT_DATA_DIRNAME = "test_input_data"
"""Directory name of test input data."""


def build_energy_assessment_report_a() -> data_model.EnergyAssessmentReport:
    """Build example instance 'a' of `EnergyAssessmentReport`.

    :return: the complete example test instance 'a' of the top-level
        `EnergyAssessmentReport` data model, for use as the primary
        test case
    """
    main_author = data_model.ReportContributor(
        name="Ben Simmonds",
        email_address="bens@naturalpower.com",  # type: ignore
        contributor_type='author',
        completion_date="2022-10-05",  # type: ignore
        contribution_notes="Main author")
    second_author = data_model.ReportContributor(
        name="Andreas Athanasopoulos",
        email_address="andreasa@naturalpower.com",  # type: ignore
        contributor_type='author',
        completion_date="2022-10-05",  # type: ignore
        contribution_notes="Second author")
    verifier = data_model.ReportContributor(
        name="Graeme Watson",
        email_address="graemew@naturalpower.com",  # type: ignore
        contributor_type='verifier',
        completion_date="2022-10-06")  # type: ignore
    approver = data_model.ReportContributor(
        name="Christian Jonsson",
        email_address="christianj@naturalpower.com",  # type: ignore
        contributor_type='approver',
        completion_date="2022-10-07")  # type: ignore
    contributors = [main_author, second_author, verifier, approver]

    coordinate_system = data_model.CoordinateSystem(
        system_label="WGS 84 / UTM zone 30N",
        epsg_number=32630)

    wind_measurement_campaign = data_model.WindMeasurementCampaign(
        measurement_id="BF_M1_1.0.0",
        name="Mast M1",
        label="M1",
        description=(
            "Barefoot Wind Farm on-site meteorological mast"),
        comments="Measurements were still ongoing at time of assessment.",
        location=data_model.Location(
            location_id="ee15ff84-6733-4858-9656-ba995d9b1022",
            location_type='measurement',
            label='M1',
            description="Verified location of Mast M1",
            comments=(
                "Documented in installation report and independently "
                "confirmed"),
            x=420165.0,
            y=6194740.0,
            coordinate_system=coordinate_system),
        metadata_ref_iea43_model=data_model.MetadataIEA43ModelRef(
            "/foo/bar/metadata_ref_iea43_model.json"))

    turbine_ids = ['WTG01', 'WTG02']
    turbine_location_map = {
        'WTG01': data_model.Location(
            location_id="c697566d-cf38-4626-9cda-bc7a77230d48",
            location_type='turbine',
            label='WTG01',
            x=419665.0,
            y=6194240.0,
            coordinate_system=coordinate_system),
        'WTG02': data_model.Location(
            location_id="c73f2e46-ba0b-4775-a2f3-b76e3c3b5012",
            location_type='turbine',
            label='WTG02',
            x=420665.0,
            y=6194240.0,
            coordinate_system=coordinate_system)}

    measurement_wind_resource_results = [
        data_model.Results(
            label="Measurement-height long-term wind",
            unit="m/s",
            applicability_type='lifetime',
            results_dimensions=['location'],
            result_components=[data_model.ResultsComponent(
                component_type='mean',
                values={
                    'BF_M1_1.0.0': 6.83})])]
    wind_spatial_model = data_model.CalculationModelSpecification(
        name="VENTOS/M",
        description="VENTOS/M is a coupled CFD-mesoscale model.",
        comments=(
            "The simulations were run using 60 representative days."))

    neighbouring_turbine_model = data_model.TurbineModel(
        label="XYZ-3.2/140")
    neighbouring_turbine_location_map = {
        'Mu_T1': data_model.Location(
            location_id="79166b5c-7e55-485b-b7e7-24f835c5e40a",
            location_type='turbine',
            label='Mu_T1',
            x=419665.0,
            y=6195240.0,
            coordinate_system=coordinate_system),
        'Mu_T2': data_model.Location(
            location_id="dc4dba73-8f1c-494f-868e-e548f2a3923f",
            location_type='turbine',
            label='Mu_T2',
            x=419665.0,
            y=6195240.0,
            coordinate_system=coordinate_system)}
    neighbouring_turbine_model_map = {
        'Mu_T1': neighbouring_turbine_model,
        'Mu_T2': neighbouring_turbine_model}
    neighbouring_turbine_hub_height_map = {
        'Mu_T1': 125.0,
        'Mu_T2': 125.0}
    neighbouring_wind_farm = data_model.WindFarm(
        name="Munro Wind Farm",
        label="MWF",
        description="The operational Munro Wind Farm",
        comments=(
            "Specifications taken from publicly available information."),
        relevance='external',
        operational_lifetime_start_date="2018-07-01",  # type: ignore
        operational_lifetime_end_date="2038-06-30",  # type: ignore
        turbine_ids=['Mu_T1', 'Mu_T2'],
        turbine_location_maps=[neighbouring_turbine_location_map],
        turbine_model_maps=[neighbouring_turbine_model_map],
        turbine_hub_height_maps=[neighbouring_turbine_hub_height_map])

    turbine_model_a = data_model.TurbineModel(
        label="ABC165-5.5MW")
    turbine_model_map_a = {
        'WTG01': turbine_model_a,
        'WTG02': turbine_model_a}
    turbine_hub_height_map_a = {
        'WTG01': 150.0,
        'WTG02': 160.0}
    project_wind_farm_a = data_model.WindFarm(
        name="Barefoot Wind Farm",
        operational_lifetime_start_date="2024-01-01",  # type: ignore
        relevance='internal',
        turbine_ids=turbine_ids,
        turbine_location_maps=[turbine_location_map],
        turbine_model_maps=[turbine_model_map_a],
        turbine_hub_height_maps=[turbine_hub_height_map_a],
        operational_restrictions=[data_model.OperationalRestriction(
            label="WSM curtailment",
            description=(
                "Wind sector management (WSM) curtailment as specified"
                "by the turbine manufacturer"))])
    wind_farms_a = [project_wind_farm_a, neighbouring_wind_farm]
    wind_farms_configuration_a = data_model.SiteWindFarmsConfiguration(
        label="A",
        description=(
            "Wind farms configuration for turbine model scenario A."),
        wind_farms=wind_farms_a)
    turbine_wind_resource_results_a = [
        data_model.Results(
            label="Turbine-location hub-height long-term wind",
            unit="m/s",
            applicability_type='lifetime',
            results_dimensions=['location'],
            result_components=[data_model.ResultsComponent(
                component_type='mean',
                values={
                    'WTG01': 6.91,
                    'WTG02': 6.95})])]
    wind_uncertainty_assessment_a = data_model.WindUncertaintyAssessment(
        categories={
            'historical': data_model.WindUncertaintyCategory(
                components=[
                    data_model.WindUncertaintyComponent(
                        results=data_model.Results(
                                label="Regression model uncertainty",
                                unit="dimensionless",
                                applicability_type='lifetime',
                                results_dimensions=['location'],
                                result_components=[data_model.ResultsComponent(
                                    component_type='std',
                                    values={
                                        'BF_M1_1.0.0': 0.025})])),
                    data_model.WindUncertaintyComponent(
                        results=data_model.Results(
                            label="Long-term consistency uncertainty",
                            unit="dimensionless",
                            applicability_type='lifetime',
                            results_dimensions=['location'],
                            result_components=[data_model.ResultsComponent(
                                component_type='std',
                                values={
                                    'BF_M1_1.0.0': 0.02})]))],
                category_results=[
                    data_model.Results(
                        label="Historical wind resource uncertainty",
                        unit="dimensionless",
                        applicability_type='lifetime',
                        results_dimensions=['location'],
                        result_components=[data_model.ResultsComponent(
                            component_type='std',
                            values={
                                'BF_M1_1.0.0': 0.03201})])])})
    wind_resource_assessment_a = data_model.WindResourceAssessment(
        measurement_wind_resource_results=measurement_wind_resource_results,
        turbine_wind_resource_results=turbine_wind_resource_results_a,
        wind_spatial_models=[wind_spatial_model],
        uncertainty_assessment=wind_uncertainty_assessment_a)
    gross_energy_assessment_a = data_model.GrossEnergyAssessment(
        results=[
            data_model.Results(
                label="Gross yield",
                unit="MWh/annum",
                applicability_type='lifetime',
                results_dimensions=['location'],
                result_components=[data_model.ResultsComponent(
                    component_type='mean',
                    values={
                        'WTG01': 15500.,
                        'WTG02': 16700.})]),
            data_model.Results(
                label="Gross yield",
                unit="MWh/annum",
                applicability_type='lifetime',
                results_dimensions=['none'],
                result_components=[data_model.ResultsComponent(
                    component_type='mean',
                    values=32200.)])])
    plant_performance_assessment_a = data_model.PlantPerformanceAssessment(
        categories={
            'curtailment': data_model.PlantPerformanceCategory(
                components=[data_model.PlantPerformanceComponent(
                    basis='timeseries_calculation',
                    variability='static_process',
                    calculation_models=[
                        data_model.CalculationModelSpecification(
                            name="Timeseries tool",
                            comments="Internal toolset")],
                    results=data_model.Results(
                        label="Loads curtailment",
                        description=(
                            "Curtailment due to a wind sector management "
                            "strategy to reduce turbine loads."),
                        comments=(
                            "Considering curtailment strategy as specified by "
                            "the turbine manufacturer."),
                        unit='dimensionless',
                        applicability_type='lifetime',
                        results_dimensions=['location'],
                        result_components=[
                            data_model.ResultsComponent(
                                component_type='mean',
                                values={
                                    'WTG01': 0.975,
                                    'WTG02': 0.983}),
                            data_model.ResultsComponent(
                                component_type='std',
                                values={
                                    'WTG01': 0.005,
                                    'WTG02': 0.005})]))],
                category_results=[data_model.Results(
                    label="Curtailment",
                    description="Curtailment losses.",
                    unit='dimensionless',
                    applicability_type='lifetime',
                    results_dimensions=['location'],
                    result_components=[
                        data_model.ResultsComponent(
                            component_type='mean',
                            values={
                                'WTG01': 0.975,
                                'WTG02': 0.983}),
                        data_model.ResultsComponent(
                            component_type='std',
                            values={
                                'WTG01': 0.005,
                                'WTG02': 0.005})])])})
    net_energy_assessment_a = data_model.NetEnergyAssessment(
        results=[
            data_model.Results(
                    label="Net yield",
                    unit="MWh/annum",
                    applicability_type='lifetime',
                    results_dimensions=['none'],
                    result_components=[
                        data_model.ResultsComponent(
                            component_type='median',
                            values=31528.6),
                        data_model.ResultsComponent(
                            component_type='std',
                            values=3468.1),
                        data_model.ResultsComponent(
                            component_type='P90',
                            values=27089.4)]),
            data_model.Results(
                label="Net yield",
                unit="MWh/annum",
                applicability_type='any_one_year',
                results_dimensions=['none'],
                result_components=[
                    data_model.ResultsComponent(
                        component_type='median',
                        values=31528.6),
                    data_model.ResultsComponent(
                        component_type='std',
                        values=4729.3),
                    data_model.ResultsComponent(
                        component_type='P90',
                        values=25475.1)])])
    energy_assessment_a = data_model.EnergyAssessment(
        label="Scenario A EYA",
        description="Energy yield assessment details for Scenario A.",
        wind_resource_assessment=wind_resource_assessment_a,
        gross_energy_assessment=gross_energy_assessment_a,
        plant_performance_assessment=plant_performance_assessment_a,
        net_energy_assessment=net_energy_assessment_a)
    scenario_a = data_model.Scenario(
        label="A",
        description="ABC165-5.5MW turbine model scenario",
        is_main_scenario=True,
        operational_lifetime_length_years=30,
        wind_measurement_campaigns=[wind_measurement_campaign],
        wind_farms_configuration=wind_farms_configuration_a,
        energy_assessment=energy_assessment_a)

    turbine_model_b = data_model.TurbineModel(
        label="PQR169-5.8MW")
    turbine_model_map_b = {
        'WTG01': turbine_model_b,
        'WTG02': turbine_model_b}
    turbine_hub_height_map_b = {
        'WTG01': 148.0,
        'WTG02': 158.0}
    project_wind_farm_b = data_model.WindFarm(
        name="Barefoot Wind Farm",
        relevance='internal',
        turbine_ids=turbine_ids,
        turbine_location_maps=[turbine_location_map],
        turbine_model_maps=[turbine_model_map_b],
        turbine_hub_height_maps=[turbine_hub_height_map_b])
    wind_farms_b = [project_wind_farm_b, neighbouring_wind_farm]
    wind_farms_configuration_b = data_model.SiteWindFarmsConfiguration(
        label="B",
        description=(
            "Wind farms configuration for turbine model scenario B."),
        comments=(
            "This wind farms configuration is identical to that for "
            "Scenario A, except for the different turbine model "
            "configuration."),
        wind_farms=wind_farms_b)
    turbine_wind_resource_results_b = [
        data_model.Results(
            label="Turbine-location hub-height long-term wind",
            unit="m/s",
            applicability_type='lifetime',
            results_dimensions=['location'],
            result_components=[data_model.ResultsComponent(
                component_type='mean',
                values={
                    'WTG01': 6.91,
                    'WTG02': 6.95})])]
    wind_uncertainty_assessment_b = data_model.WindUncertaintyAssessment(
        categories={
            'historical': data_model.WindUncertaintyCategory(
                components=[
                    data_model.WindUncertaintyComponent(
                        results=data_model.Results(
                                label="Regression model uncertainty",
                                unit="dimensionless",
                                applicability_type='lifetime',
                                results_dimensions=['location'],
                                result_components=[data_model.ResultsComponent(
                                    component_type='std',
                                    values={
                                        'BF_M1_1.0.0': 0.025})])),
                    data_model.WindUncertaintyComponent(
                        results=data_model.Results(
                            label="Long-term consistency uncertainty",
                            unit="dimensionless",
                            applicability_type='lifetime',
                            results_dimensions=['location'],
                            result_components=[data_model.ResultsComponent(
                                component_type='std',
                                values={
                                    'BF_M1_1.0.0': 0.02})]))],
                category_results=[
                    data_model.Results(
                        label="Historical wind resource uncertainty",
                        unit="dimensionless",
                        applicability_type='lifetime',
                        results_dimensions=['location'],
                        result_components=[data_model.ResultsComponent(
                            component_type='std',
                            values={
                                'BF_M1_1.0.0': 0.03201})])])})
    wind_resource_assessment_b = data_model.WindResourceAssessment(
        measurement_wind_resource_results=measurement_wind_resource_results,
        turbine_wind_resource_results=turbine_wind_resource_results_b,
        wind_spatial_models=[wind_spatial_model],
        uncertainty_assessment=wind_uncertainty_assessment_b)
    gross_energy_assessment_b = data_model.GrossEnergyAssessment(
        results=[
            data_model.Results(
                label="Gross yield",
                unit="MWh/annum",
                applicability_type='lifetime',
                results_dimensions=['location'],
                result_components=[data_model.ResultsComponent(
                    component_type='mean',
                    values={
                        'WTG01': 18100.,
                        'WTG02': 18900.})]),
            data_model.Results(
                label="Gross yield",
                unit="MWh/annum",
                applicability_type='lifetime',
                results_dimensions=['none'],
                result_components=[data_model.ResultsComponent(
                    component_type='mean',
                    values=37000.)])])
    plant_performance_assessment_b = data_model.PlantPerformanceAssessment(
        categories={
            'curtailment': data_model.PlantPerformanceCategory(
                components=[data_model.PlantPerformanceComponent(
                    basis='project_specific_estimate',
                    variability='static_process',
                    results=data_model.Results(
                        label="Loads curtailment",
                        description=(
                            "Expected curtailment due to a wind sector "
                            "management to reduce turbine loads."),
                        comments=(
                            "A broad estimate of curtailment losses in "
                            "the absence of details from the turbine "
                            "manufacturer."),
                        unit='dimensionless',
                        applicability_type='lifetime',
                        results_dimensions=['location'],
                        result_components=[
                            data_model.ResultsComponent(
                                component_type='mean',
                                values={
                                    'WTG01': 0.95,
                                    'WTG02': 0.95}),
                            data_model.ResultsComponent(
                                component_type='std',
                                values={
                                    'WTG01': 0.05,
                                    'WTG02': 0.05})]))],
                category_results=[data_model.Results(
                    label="Curtailment",
                    description="Curtailment losses.",
                    unit='dimensionless',
                    applicability_type='lifetime',
                    results_dimensions=['location'],
                    result_components=[
                        data_model.ResultsComponent(
                            component_type='mean',
                            values={
                                'WTG01': 0.95,
                                'WTG02': 0.95}),
                        data_model.ResultsComponent(
                            component_type='std',
                            values={
                                'WTG01': 0.05,
                                'WTG02': 0.05})])])})
    net_energy_assessment_b = data_model.NetEnergyAssessment(
        results=[
            data_model.Results(
                    label="Net yield",
                    unit="MWh/annum",
                    applicability_type='lifetime',
                    results_dimensions=['none'],
                    result_components=[
                        data_model.ResultsComponent(
                            component_type='median',
                            values=35150.0),
                        data_model.ResultsComponent(
                            component_type='std',
                            values=4569.5),
                        data_model.ResultsComponent(
                            component_type='P90',
                            values=29301.0)]),
            data_model.Results(
                label="Net yield",
                unit="MWh/annum",
                applicability_type='any_one_year',
                results_dimensions=['none'],
                result_components=[
                    data_model.ResultsComponent(
                        component_type='median',
                        values=35150.0),
                    data_model.ResultsComponent(
                        component_type='std',
                        values=5799.8),
                    data_model.ResultsComponent(
                        component_type='P90',
                        values=27726.3)])])
    energy_assessment_b = data_model.EnergyAssessment(
        label="Scenario B EYA",
        description="Energy yield assessment details for Scenario B.",
        comments=(
            "The Scenario B assessment should be considered indicative "
            "only due to potentially inaccurate assumptions."),
        wind_resource_assessment=wind_resource_assessment_b,
        gross_energy_assessment=gross_energy_assessment_b,
        plant_performance_assessment=plant_performance_assessment_b,
        net_energy_assessment=net_energy_assessment_b)
    scenario_b = data_model.Scenario(
        label="B",
        description="PQR169-5.8MW turbine model scenario",
        comments=(
            "The site suitability of turbine model has not yet investigated."),
        is_main_scenario=False,
        operational_lifetime_length_years=30,
        wind_measurement_campaigns=[wind_measurement_campaign],
        wind_farms_configuration=wind_farms_configuration_b,
        energy_assessment=energy_assessment_b)

    scenarios = [scenario_a, scenario_b]

    energy_assessment_report = data_model.EnergyAssessmentReport(
        **{'$id': (
            "https://example.naturalpower.com/api/v2/eya/report/"
            "id=b1396029-e9af-49f7-9599-534db175e53c")},
        title="Energy yield assessment of the Barefoot Wind Farm",
        description=(
            "Wind resource and energy yield assessment of the Barefoot "
            "Wind Farm based on one on-site meteorological mast and "
            "considering two different turbine scenarios."),
        comments=(
            "Update to consider further on-site measurement data."),
        project_name="Barefoot Wind Farm",
        document_id="12345678",
        document_version="B",
        issue_date="2022-10-07",  # type: ignore
        issuing_organisation_name="The Natural Power Consultants Limited",
        issuing_organisation_abbreviation="Natural Power",
        issuing_organisation_address=(
            "The Greenhouse, Dalry, Castle Douglas, DG7 3XS, UK"),
        receiving_organisation_name="Cubico Sustainable Investments Limited",
        receiving_organisation_abbreviation="Cubico",
        receiving_organisation_contact_name="Charlie Plumley",
        receiving_organisation_address=(
            "70 St Mary Axe, London, EC3A 8BE, UK"),
        contributors=contributors,
        confidentiality_classification="Confidential",
        scenarios=scenarios)
    return energy_assessment_report


@pytest.fixture(scope='session')
def energy_assessment_report_a() -> data_model.EnergyAssessmentReport:
    """Get test case instance 'a' of `EnergyAssessmentReport`.

    :return: the complete example test instance 'a' of the top-level
        `EnergyAssessmentReport` data model, for use as the primary
        test case
    """
    return build_energy_assessment_report_a()


@pytest.fixture(scope='session')
def energy_assessment_report_a_tmp_filepath(
        energy_assessment_report_a, json_examples_tmp_dirpath) -> Path:
    """Get the temporary path of the test case instance 'a' json file.

    :return: the directory path of the temporary json file
        representation of the example test case instance 'a'
    """
    filepath = (
            json_examples_tmp_dirpath
            / "iec_61400-15-2_reporting_def_example_a.json")
    with open(filepath, 'w') as f:
        f.write(energy_assessment_report_a.json(
            indent=2, exclude_none=True, by_alias=True))
    return filepath


@pytest.fixture(scope='session')
def test_input_data_dirpath():
    """Get the path of the directory where test input data is located.

    :return: the directory path of test input data
    """
    dirpath = Path(__file__).parent
    return dirpath / TEST_INPUT_DATA_DIRNAME


@pytest.fixture(scope='session')
def top_level_dirpath() -> Path:
    """Get the path of the top-level project directory.

    The top-level is the git repository, one level above the python
    package.

    :return: path to the project top-level directory
    """
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture(scope='session')
def master_json_schema_dirpath(top_level_dirpath) -> Path:
    """Get the path of the json schema directory.

    :param top_level_dirpath: path to the project top-level directory
    :return: directory path where the master json schema is located
    :raises ValueError: if the directory does not exist at the expected
        location
    """
    master_json_schema_dirpath = top_level_dirpath / "json_schema"
    if not master_json_schema_dirpath.is_dir():
        raise ValueError(
            f"the expected json schema directory "
            f"'{master_json_schema_dirpath}' does not exist")
    return master_json_schema_dirpath


@pytest.fixture(scope='session')
def master_json_schema_filepath(master_json_schema_dirpath) -> Path:
    """Get the path of the IEC 61400-15-2 Reporting DEF json schema.

    :param master_json_schema_dirpath: directory path where the master
        json schema is located
    :return: file path of the master json schema
    :raises ValueError: if the file does not exist at the expected
        location
    """
    filepath = (
        master_json_schema_dirpath
        / "iec_61400-15-2_reporting_def.schema.json")
    if not filepath.is_file():
        raise ValueError(
            f"the expected json schema file '{filepath}' does not exist")
    return filepath


@pytest.fixture(scope='session')
def master_json_schema(master_json_schema_filepath) -> dict:
    """Get `dict` representation of the master json schema.

    Note that this function returns a representation of the master
    IEC 61400-15-2 Reporting DEF json schema and not a json schema
    representation of the pydantic model.

    :param master_json_schema_filepath: file path of the master json
        schema
    :return: a `dict` representation of the master IEC 61400-15-2
        Reporting DEF json schema
    """
    with open(master_json_schema_filepath) as f:
        json_schema = json.load(f)
    return json_schema


@pytest.fixture(scope='session')
def pydantic_json_schema(energy_assessment_report_a) -> dict:
    """Get a `dict` representation of the pydantic json schema.

    :param energy_assessment_report_a: the complete example test
        instance 'a' of the top-level `EnergyAssessmentReport` data
        model used as the primary test case
    :return: a `dict` representation of the pydantic data model json
        schema exported from the `data_model.EnergyAssessmentReport`
        class
    """
    return energy_assessment_report_a.final_json_schema()


@pytest.fixture(scope='session')
def pydantic_json_schema_tmp_path(
        pydantic_json_schema, tmp_path_factory) -> Path:
    """Get the path to the temporary pydantic json schema file.

    :param pydantic_json_schema: a `dict` representation of the pydantic
        json schema exported from `data_model.EnergyAssessmentReport`
    :param tmp_path_factory: the `pytest` `tmp_path_factory`
    :return: the path to the temporary json schema file representation
        of the pydantic data model
    """
    tmp_dirpath = tmp_path_factory.mktemp("schema")
    filepath = tmp_dirpath / "iec_61400-15-2_reporting_def.schema.json"
    with open(filepath, 'w') as f:
        f.write(json.dumps(pydantic_json_schema, indent=2))
    return filepath


@pytest.fixture(scope='session')
def pydantic_json_schema_from_file(pydantic_json_schema_tmp_path) -> dict:
    """Get `dict` representation of the pydantic json schema from file.

    :param pydantic_json_schema_tmp_path: the path to the temporary json
        schema file representation of the pydantic data model
    :return: a `dict` representation of the pydantic data model json
        schema read back from the temporary file
    """
    with open(pydantic_json_schema_tmp_path) as f:
        json_schema = json.load(f)
    return json_schema


@pytest.fixture(scope='session')
def json_examples_dirpath(top_level_dirpath) -> Path:
    """Get the path of the json examples permanent directory.

    :param top_level_dirpath: path to the project top-level directory
    :return: directory path where the json examples are located
    :raises ValueError: if the directory does not exist at the expected
        location
    """
    json_examples_dirpath = top_level_dirpath / "json_schema" / "examples"
    if not json_examples_dirpath.is_dir():
        raise ValueError(
            f"the expected json examples directory "
            f"'{json_examples_dirpath}' does not exist")
    return json_examples_dirpath


@pytest.fixture(scope='session')
def json_example_filepaths(json_examples_dirpath) -> list[Path]:
    """Get the paths of the IEC 61400-15-2 Reporting DEF json examples.

    :param json_examples_dirpath: directory path where the json examples
        are located
    :return: file paths of the json examples
    :raises ValueError: if no example json files exist at the expected
        location
    """
    filename_pattern = "iec_61400-15-2_reporting_def_example*.json"
    json_example_filepaths = list(json_examples_dirpath.glob(filename_pattern))
    if len(json_example_filepaths) < 1:
        raise ValueError(
            f"no example json files with the expected filename pattern "
            f"exist in the directory '{json_examples_dirpath}'")
    return json_example_filepaths


@pytest.fixture(scope='session')
def json_example_dict(json_example_filepaths) -> dict[str, dict]:
    """Get `dict` of the IEC 61400-15-2 Reporting DEF json examples.

    :param json_example_filepaths: list of paths to the json example
        files
    :return: a `dict` of the form {<filename>: <example_dict>}
    """
    json_example_dict = {}
    for json_example_filepath in json_example_filepaths:
        with open(json_example_filepath) as f:
            json_example_dict[f.name] = json.load(f)
    return json_example_dict


@pytest.fixture(scope='session')
def json_examples_tmp_dirpath(tmp_path_factory) -> Path:
    """Get a temporary directory path for json schema example files.

    This directory path is used for json schema example files that are
    generated during the test session (not for the permanent example
    files that are located in `json_examples_dirpath`).

    :param tmp_path_factory: the `pytest` `tmp_path_factory`
    :return: a `Path` representation of the temporary json schema
        examples directory
    """
    return tmp_path_factory.mktemp("examples")


# TEMPORARY CODE
# def export_json_schema(filepath: Path):
#     """Export the top-level json schema from the pydantic model.
#
#     :param filepath: the path to export the json schema file to
#     """
#     from eya_def_tools import data_model
#     import json
#     json_schema = data_model.EnergyAssessmentReport.final_json_schema()
#     with open(filepath, 'w') as f:
#         f.write(json.dumps(json_schema, indent=2))
#
#
# def export_energy_assessment_report_example_as_json_file(
#         filepath: Path,
#         exclude_none: bool = True,
#         by_alias: bool = True) -> None:
#     """Export example instance 'a' of `EnergyAssessmentReport` to json.
#
#     :param filepath: the path to export the json file to
#     :param exclude_none: whether to exclude variables set to `None` from
#         the json document
#     :param by_alias: whether to use model variable aliases as property
#         names
#     """
#     with open(filepath, 'w') as f:
#         f.write(build_energy_assessment_report_a().json(
#             indent=2, exclude_none=exclude_none, by_alias=by_alias))
#
#
# export_json_schema(Path("iec_61400-15-2_reporting_def.schema.json"))
#
# export_energy_assessment_report_example_as_json_file(
#     Path("iec_61400-15-2_reporting_def_example_a.json"))
