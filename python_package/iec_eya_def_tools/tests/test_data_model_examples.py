# -*- coding: utf-8 -*-
"""Test the `iec_eya_def_tools.data_model` module on example datasets.

"""


import pytest

import iec_eya_def_tools.data_model as data_model


@pytest.fixture
def energy_assessment_report_a() -> data_model.EnergyAssessmentReport:
    """Make test case instance 'a' of `EnergyAssessmentReport`."""
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

    wind_spatial_model = data_model.WindSpatialModel(
        model_name="VENTOS/M",
        model_description="VENTOS/M is a coupled CFD-mesoscale model",
        model_comments=(
            "The simulations were run using 60 representative days."))

    neighbouring_turbine_model = data_model.TurbineModel(
        turbine_model_label="XYZ-3.2/140")
    neighbouring_turbines = [
        data_model.Turbine(
            turbine_label="Mu_T1",
            x=419665.0,
            y=6195240.0,
            coordinate_system=coordinate_system,
            hub_height=125.0,
            turbine_model=neighbouring_turbine_model),
        data_model.Turbine(
            turbine_label="Mu_T2",
            x=420665.0,
            y=6195240.0,
            coordinate_system=coordinate_system,
            hub_height=125.0,
            turbine_model=neighbouring_turbine_model)]
    neighbouring_wind_farm = data_model.WindFarm(
        wind_farm_name="Munro Wind Farm",
        wind_farm_label="MWF",
        wind_farm_description="",
        wind_farm_comments="",
        operational_lifetime_start_date="2018-07-01",  # type: ignore
        operational_lifetime_end_date="2038-06-30",  # type: ignore
        relevance='external',
        turbines=neighbouring_turbines)

    turbine_model_a = data_model.TurbineModel(
        turbine_model_label="ABC165-5.5MW")
    turbines_a = [
        data_model.Turbine(
            turbine_label="WTG01",
            x=419665.0,
            y=6194240.0,
            coordinate_system=coordinate_system,
            hub_height=150.0,
            turbine_model=turbine_model_a),
        data_model.Turbine(
            turbine_label="WTG02",
            x=420665.0,
            y=6194240.0,
            coordinate_system=coordinate_system,
            hub_height=160.0,
            turbine_model=turbine_model_a)]
    project_wind_farm_a = data_model.WindFarm(
        wind_farm_name="Barefoot Wind Farm",
        operational_lifetime_start_date="2024-01-01",  # type: ignore
        relevance='internal',
        turbines=turbines_a)
    wind_farms_a = [project_wind_farm_a, neighbouring_wind_farm]
    wind_farms_configuration_a = data_model.SiteWindFarmsConfiguration(
        wind_farms_configuration_label="A",
        wind_farms_configuration_description=(
            "Wind farms configuration for turbine model scenario A"),
        wind_farms=wind_farms_a)
    energy_assessment_results_a_lifetime = data_model.EnergyAssessmentResults(
        results_type='lifetime',
        results_label="30-year",
        results_description=(
            "Results for the full operational lifetime of 30 years"),
        mast_wind_resource_results=data_model.MastWindResourceResults(),
        turbine_wind_resource_results=data_model.TurbineWindResourceResults(),
        gross_energy_results=data_model.GrossEnergyResults(),
        plant_performance_results=data_model.PlantPerformanceResults(),
        net_energy_results=data_model.NetEnergyResults(),
        uncertainty_results=data_model.UncertaintyResults(),
        confidence_limit_results=data_model.ConfidenceLimitResults())
    energy_assessment_results_a_1year = data_model.EnergyAssessmentResults(
        results_type='any_one_year',
        results_label="1-year",
        results_description=(
            "Results for any one operational year"),
        results_comments=(
            "Results consider mean of losses that vary over the "
            "operational lifetime."),
        mast_wind_resource_results=data_model.MastWindResourceResults(),
        turbine_wind_resource_results=data_model.TurbineWindResourceResults(),
        gross_energy_results=data_model.GrossEnergyResults(),
        plant_performance_results=data_model.PlantPerformanceResults(),
        net_energy_results=data_model.NetEnergyResults(),
        uncertainty_results=data_model.UncertaintyResults(),
        confidence_limit_results=data_model.ConfidenceLimitResults())
    energy_assessment_results_a = [
        energy_assessment_results_a_lifetime,
        energy_assessment_results_a_1year]
    scenario_a = data_model.Scenario(
        scenario_label="A",
        scenario_description="ABC165-5.5MW turbine model scenario",
        is_main_scenario=True,
        operational_lifetime_length_years=30,
        wind_farms_configuration=wind_farms_configuration_a,
        wind_spatial_models=[wind_spatial_model],
        energy_assessment_results=energy_assessment_results_a)

    turbine_model_b = data_model.TurbineModel(
        turbine_model_label="PQR169-5.8MW")
    turbines_b = [
        data_model.Turbine(
            turbine_label="WTG01",
            x=419665.0,
            y=6194240.0,
            coordinate_system=coordinate_system,
            hub_height=148.0,
            turbine_model=turbine_model_b),
        data_model.Turbine(
            turbine_label="WTG02",
            x=420665.0,
            y=6194240.0,
            coordinate_system=coordinate_system,
            hub_height=158.0,
            turbine_model=turbine_model_b)]
    project_wind_farm_b = data_model.WindFarm(
        wind_farm_name="Barefoot Wind Farm",
        relevance='internal',
        turbines=turbines_b)
    wind_farms_b = [project_wind_farm_b, neighbouring_wind_farm]
    wind_farms_configuration_b = data_model.SiteWindFarmsConfiguration(
        wind_farms_configuration_label="B",
        wind_farms_configuration_description=(
            "Wind farms configuration for turbine model scenario B"),
        wind_farms_configuration_comments=(
            "The wind farms configuration is identical to that for "
            "scenario A, except for the different turbine model "
            "configuration"),
        wind_farms=wind_farms_b)
    energy_assessment_results_b_lifetime = data_model.EnergyAssessmentResults(
        results_type='lifetime',
        results_label="30-year",
        results_description=(
            "Results for the full operational lifetime of 30 years"),
        mast_wind_resource_results=data_model.MastWindResourceResults(),
        turbine_wind_resource_results=data_model.TurbineWindResourceResults(),
        gross_energy_results=data_model.GrossEnergyResults(),
        plant_performance_results=data_model.PlantPerformanceResults(),
        net_energy_results=data_model.NetEnergyResults(),
        uncertainty_results=data_model.UncertaintyResults(),
        confidence_limit_results=data_model.ConfidenceLimitResults())
    energy_assessment_results_b_1year = data_model.EnergyAssessmentResults(
        results_type='any_one_year',
        results_label="1-year",
        results_description=(
            "Results for any one operational year"),
        results_comments=(
            "Results consider mean of losses that vary over the "
            "operational lifetime."),
        mast_wind_resource_results=data_model.MastWindResourceResults(),
        turbine_wind_resource_results=data_model.TurbineWindResourceResults(),
        gross_energy_results=data_model.GrossEnergyResults(),
        plant_performance_results=data_model.PlantPerformanceResults(),
        net_energy_results=data_model.NetEnergyResults(),
        uncertainty_results=data_model.UncertaintyResults(),
        confidence_limit_results=data_model.ConfidenceLimitResults())
    energy_assessment_results_b = [
        energy_assessment_results_b_lifetime,
        energy_assessment_results_b_1year]
    scenario_b = data_model.Scenario(
        scenario_label="B",
        scenario_description="PQR169-5.8MW turbine model scenario",
        scenario_comments=(
            "The site suitability of turbine model has not yet investigated."),
        is_main_scenario=False,
        operational_lifetime_length_years=30,
        wind_farms_configuration=wind_farms_configuration_b,
        wind_spatial_models=[wind_spatial_model],
        energy_assessment_results=energy_assessment_results_b)

    scenarios = [scenario_a, scenario_b]

    energy_assessment_report = data_model.EnergyAssessmentReport(
        project_name="Barefoot Wind Farm",
        report_title="Energy yield assessment of the Barefoot Wind Farm",
        report_description=(
            "Wind resource and energy yield assessment of the Barefoot "
            "Wind Farm based on two on-site meteorological masts and "
            "considering two different turbine scenarios"),
        report_comments=(
            "Update to consider further on-site measurement data"),
        document_id="12345678",
        document_version="B",
        issue_date="2022-10-07",  # type: ignore
        issuing_organisation="Natural Power Consultants Limited ",
        issuing_organisation_address=(
            "The Greenhouse, Dalry, Castle Douglas, DG7 3XS, UK"),
        receiving_organisation="Cubico Sustainable Investments Limited",
        receiving_organisation_contact_name="Charlie Plumley",
        receiving_organisation_address=(
            "70 St Mary Axe, London, EC3A 8BE, UK"),
        contributors=contributors,
        report_confidentiality_classification="Confidential",
        scenarios=scenarios)
    return energy_assessment_report


def test_initiate_energy_assessment_report_a(energy_assessment_report_a):
    assert isinstance(
        energy_assessment_report_a, data_model.EnergyAssessmentReport)
    with open("test.json", 'w') as f:
        f.write(energy_assessment_report_a.json(indent=2))
