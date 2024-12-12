"""Setup and fixtures for the ``eya_def_tools`` test module.

The data model component fixtures all have the scope of the entire test
session to avoid having to build them for every individual test. The
tests should therefore not alter any of the data model component
instances, which may cause interference with other tests. Tests that
involve modifications should create their own instances or make copies.

"""

import datetime as dt
import json
import urllib.request as urllib_request
import uuid as uuid_
from pathlib import Path
from typing import Any

import pytest

from eya_def_tools.data_models import (
    dataset,
    energy_assessment,
    eya_def,
    eya_def_header,
    general,
    iea43_wra_data_model,
    plant_performance,
    reference_wind_farm,
    scenario,
    spatial,
    turbine_model,
    wind_farm,
    wind_resource,
    wind_uncertainty,
)


@pytest.fixture(scope="session")
def top_level_dirpath() -> Path:
    """The path of the top-level project repository directory.

    The top-level is the Git repository, one level above the Python
    package.

    :return: path to the project top-level directory
    """
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture(scope="session")
def master_json_schema_dirpath(top_level_dirpath: Path) -> Path:
    """The path of the JSON Schema directory.

    :param top_level_dirpath: path to the project top-level directory
    :return: directory path where the master json schema is located
    :raises ValueError: if the directory does not exist at the expected
        location
    """
    master_json_schema_dirpath = top_level_dirpath / "json_schema"
    if not master_json_schema_dirpath.is_dir():
        raise ValueError(
            f"the expected json schema directory "
            f"'{master_json_schema_dirpath}' does not exist"
        )
    return master_json_schema_dirpath


@pytest.fixture(scope="session")
def master_json_schema_filepath(master_json_schema_dirpath: Path) -> Path:
    """The path of the IEC 61400-15-2 EYA DEF JSON Schema.

    :param master_json_schema_dirpath: directory path where the master
        json schema is located
    :return: file path of the master json schema
    :raises ValueError: if the file does not exist at the expected
        location
    """
    filepath = master_json_schema_dirpath / "iec_61400-15-2_eya_def.schema.json"
    if not filepath.is_file():
        raise ValueError(f"the expected json schema file '{filepath}' does not exist")
    return filepath


@pytest.fixture(scope="session")
def master_json_schema(master_json_schema_filepath: Path) -> dict[str, Any]:
    """A ``dict`` representation of the master json schema.

    Note that this function returns a representation of the master
    IEC 61400-15-2 EYA DEF JSON Schema and not a JSON Schema
    representation of the pydantic model.

    :param master_json_schema_filepath: file path of the master json
        schema
    :return: a ``dict`` representation of the master IEC 61400-15-2
        EYA DEF JSON Schema
    """
    with open(master_json_schema_filepath) as f:
        json_schema = json.load(f)

    return json_schema


@pytest.fixture(scope="session")
def pydantic_json_schema() -> dict[str, Any]:
    """A ``dict`` representation of the pydantic JSON Schema.

    :return: a ``dict`` representation of the pydantic data model JSON
        Schema exported from the ``EyaDefDocument`` class
    """
    return eya_def.EyaDefDocument.model_json_schema(by_alias=True)


@pytest.fixture(scope="session")
def pydantic_json_schema_tmp_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The path to the temporary pydantic JSON Schema file.

    :param tmp_path_factory: the ``pytest`` ``tmp_path_factory``
    :return: the path to the temporary JSON Schema file representation
        of the pydantic data model
    """
    tmp_dirpath = tmp_path_factory.mktemp("schema")
    filepath = tmp_dirpath / "iec_61400-15-2_eya_def.schema.json"
    with open(filepath, "w") as f:
        f.write(eya_def.EyaDefDocument.model_json_schema_str(by_alias=True))

    return filepath


@pytest.fixture(scope="session")
def pydantic_json_schema_from_file(
    pydantic_json_schema_tmp_path: Path,
) -> dict[str, Any]:
    """A `dict` representation of the pydantic JSON Schema from file.

    :param pydantic_json_schema_tmp_path: the path to the temporary JSON
        Schema file representation of the pydantic data model
    :return: a ``dict`` representation of the pydantic data model JSON
        Schema read back from the temporary file
    """
    with open(pydantic_json_schema_tmp_path) as f:
        json_schema = json.load(f)

    return json_schema


@pytest.fixture(scope="session")
def json_examples_dirpath(top_level_dirpath: Path) -> Path:
    """The path of the JSON examples permanent directory.

    :param top_level_dirpath: path to the project top-level directory
    :return: directory path where the JSON examples are located
    :raises ValueError: if the directory does not exist at the expected
        location
    """
    json_examples_dirpath = top_level_dirpath / "json_schema" / "examples"
    if not json_examples_dirpath.is_dir():
        raise ValueError(
            f"the expected json examples directory "
            f"'{json_examples_dirpath}' does not exist"
        )
    return json_examples_dirpath


@pytest.fixture(scope="session")
def json_example_filepaths(json_examples_dirpath: Path) -> list[Path]:
    """The paths of the IEC 61400-15-2 EYA DEF JSON example files.

    :param json_examples_dirpath: directory path where the JSON example
        files are located
    :return: file paths of the JSON examples
    :raises ValueError: if no example JSON files exist at the expected
        location
    """
    filename_pattern = "iec_61400-15-2_eya_def_example_?.json"
    json_example_filepaths = list(json_examples_dirpath.glob(filename_pattern))
    if len(json_example_filepaths) < 1:
        raise ValueError(
            f"no example json files with the expected filename pattern "
            f"exist in the directory '{json_examples_dirpath}'"
        )
    return json_example_filepaths


@pytest.fixture(scope="session")
def json_example_dict(json_example_filepaths: list[Path]) -> dict[str, Any]:
    """A ``dict`` of the IEC 61400-15-2 EYA DEF JSON examples.

    :param json_example_filepaths: list of paths to the JSON example
        files
    :return: a ``dict`` of the form ``{<filename>: <example_dict>}``
    """
    json_example_dict = {}
    for json_example_filepath in json_example_filepaths:
        with open(json_example_filepath) as f:
            json_example_dict[f.name] = json.load(f)

    return json_example_dict


@pytest.fixture(scope="session")
def json_examples_tmp_dirpath(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A temporary directory path for JSON Schema example files.

    This directory path is used for JSON Schema example files that are
    generated during the test session (not for the permanent example
    files that are located in ``json_examples_dirpath``).

    :param tmp_path_factory: the ``pytest`` ``tmp_path_factory``
    :return: a ``Path`` representation of the temporary JSON Schema
        examples directory
    """
    return tmp_path_factory.mktemp("examples")


@pytest.fixture(scope="session")
def iea43_wra_data_model_json_schema() -> dict[str, Any]:
    """The IEA Task 43 WRA Data Model JSON Schema."""
    with urllib_request.urlopen(
        iea43_wra_data_model.IEA43_WRA_DATA_MODEL_SCHEMA_URI
    ) as url:
        json_schema = json.load(url)
    return json_schema


@pytest.fixture(scope="session")
def turbine_location_wtg01_a() -> spatial.Location:
    """Turbine test case instance 'WTG01_a' of ``Location``."""
    return spatial.Location(
        x=419665.0,
        y=6194240.0,
    )


@pytest.fixture(scope="session")
def turbine_location_wtg01_b() -> spatial.Location:
    """Turbine test case instance 'WTG01_b' of ``Location``."""
    return spatial.Location(
        x=419675.0,
        y=6194260.0,
    )


@pytest.fixture(scope="session")
def turbine_location_wtg02_a() -> spatial.Location:
    """Turbine test case instance 'WTG02_a' of ``Location``."""
    return spatial.Location(
        x=420665.0,
        y=6194240.0,
    )


@pytest.fixture(scope="session")
def turbine_location_wtg02_b() -> spatial.Location:
    """Turbine test case instance 'WTG02_b' of ``Location``."""
    return spatial.Location(
        x=420655.0,
        y=6194220.0,
    )


@pytest.fixture(scope="session")
def turbine_location_mu_t1_a() -> spatial.Location:
    """Turbine test case instance 'Mu_T1_a' of ``Location``."""
    return spatial.Location(
        x=419665.0,
        y=6195240.0,
    )


@pytest.fixture(scope="session")
def turbine_location_mu_t2_a() -> spatial.Location:
    """Turbine test case instance 'Mu_T2_a' of ``Location``."""
    return spatial.Location(
        x=419665.0,
        y=6195240.0,
    )


# TODO update once draft of IEC-61400-16 data model is ready
@pytest.fixture(scope="session")
def turbine_model_a() -> turbine_model.TurbineModelSpecifications:
    """Test case instance 'a' of ``TurbineModel``."""
    return turbine_model.TurbineModelSpecifications(
        {
            "id": "6ca5bc01-04b1-421a-a033-133304d6cc7f",
            "label": "ABC165-5.5MW",
        }
    )


# TODO update once draft of IEC-61400-16 data model is ready
@pytest.fixture(scope="session")
def turbine_model_b() -> turbine_model.TurbineModelSpecifications:
    """Test case instance 'b' of ``TurbineModel``."""
    return turbine_model.TurbineModelSpecifications(
        {
            "id": "e2914c83-f355-4cf2-9051-8e0f34aa3c03",
            "label": "PQR169-5.8MW",
        }
    )


# TODO update once draft of IEC-61400-16 data model is ready
@pytest.fixture(scope="session")
def turbine_model_c() -> turbine_model.TurbineModelSpecifications:
    """Test case instance 'c' of ``TurbineModel``."""
    return turbine_model.TurbineModelSpecifications(
        {
            "turbine_model_id": "e3288cbd-fa3b-4241-8a4c-3856fc10c55e",
            "label": "XYZ-3.2/140",
        }
    )


@pytest.fixture(scope="session")
def all_turbine_models(
    turbine_model_a: turbine_model.TurbineModelSpecifications,
    turbine_model_b: turbine_model.TurbineModelSpecifications,
    turbine_model_c: turbine_model.TurbineModelSpecifications,
) -> list[turbine_model.TurbineModelSpecifications]:
    """A list of all turbine model test case instances."""
    return [turbine_model_a, turbine_model_b, turbine_model_c]


@pytest.fixture(scope="session")
def turbine_operational_restriction_a() -> wind_farm.OperationalRestriction:
    """Test case instance 'a' of ``OperationalRestriction``."""
    return wind_farm.OperationalRestriction(
        label="WSM curtailment",
        description=(
            "Wind sector management (WSM) curtailment as specified"
            "by the turbine manufacturer. The power output is limited "
            "to 4.5 MW at wind speeds above 18.0 m/s when the wind "
            "direction is from between 120.0 and 210.0 degrees."
        ),
        comments=(
            "The strategy is designed to mitigate against the impact "
            "of high ambient turbulence intensity."
        ),
    )


@pytest.fixture(scope="session")
def turbine_specification_wtg01_a(
    turbine_location_wtg01_a: spatial.Location,
    turbine_operational_restriction_a: wind_farm.OperationalRestriction,
) -> wind_farm.TurbineConfiguration:
    """Test case instance 'WTG01_a' of ``TurbineSpecification``."""
    return wind_farm.TurbineConfiguration(
        id="2bbe1cb3-e9f3-42ad-be61-3657ea2ac174",
        label="WTG01_A",
        description="Configuration of WTG01 in Scenario A",
        location=turbine_location_wtg01_a,
        ground_level_altitude=44.9,
        hub_height=150.0,
        turbine_model_id="6ca5bc01-04b1-421a-a033-133304d6cc7f",
        restrictions=[turbine_operational_restriction_a],
    )


@pytest.fixture(scope="session")
def turbine_specification_wtg01_b(
    turbine_location_wtg01_b: spatial.Location,
) -> wind_farm.TurbineConfiguration:
    """Test case instance 'WTG01_b' of ``TurbineSpecification``."""
    return wind_farm.TurbineConfiguration(
        id="f5cfd507-5550-4fbb-bdca-3dc6b1c6323c",
        label="WTG01_B",
        description="Configuration of WTG01 in Scenario B",
        location=turbine_location_wtg01_b,
        ground_level_altitude=45.1,
        hub_height=148.0,
        turbine_model_id="e2914c83-f355-4cf2-9051-8e0f34aa3c03",
    )


@pytest.fixture(scope="session")
def turbine_specification_wtg02_a(
    turbine_location_wtg02_a: spatial.Location,
    turbine_operational_restriction_a: wind_farm.OperationalRestriction,
) -> wind_farm.TurbineConfiguration:
    """Test case instance 'WTG02_a' of ``TurbineSpecification``."""
    return wind_farm.TurbineConfiguration(
        id="39f9dd43-6322-4738-81af-6a65766b26e3",
        label="WTG02_A",
        description="Configuration of WTG02 in Scenario A",
        location=turbine_location_wtg02_a,
        ground_level_altitude=46.3,
        hub_height=160.0,
        turbine_model_id="6ca5bc01-04b1-421a-a033-133304d6cc7f",
        restrictions=[turbine_operational_restriction_a],
    )


@pytest.fixture(scope="session")
def turbine_specification_wtg02_b(
    turbine_location_wtg02_b: spatial.Location,
) -> wind_farm.TurbineConfiguration:
    """Test case instance 'WTG02_b' of ``TurbineSpecification``."""
    return wind_farm.TurbineConfiguration(
        id="a5ee87e3-5254-45fb-a057-4548b8c0424c",
        label="WTG02_B",
        description="Configuration of WTG02 in Scenario B",
        location=turbine_location_wtg02_b,
        ground_level_altitude=44.6,
        hub_height=158.0,
        turbine_model_id="e2914c83-f355-4cf2-9051-8e0f34aa3c03",
    )


@pytest.fixture(scope="session")
def turbine_specification_mu_t1_a(
    turbine_location_mu_t1_a: spatial.Location,
) -> wind_farm.TurbineConfiguration:
    """Test case instance 'Mu_T1_a' of ``TurbineSpecification``."""
    return wind_farm.TurbineConfiguration(
        id="f08b05bd-f90b-4833-91a5-4284b64c80db",
        label="Mu_T1_a",
        description="Configuration of the neighbouring Mu_T1_a turbine",
        location=turbine_location_mu_t1_a,
        ground_level_altitude=40.2,
        hub_height=125.0,
        turbine_model_id="e3288cbd-fa3b-4241-8a4c-3856fc10c55e",
    )


@pytest.fixture(scope="session")
def turbine_specification_mu_t2_a(
    turbine_location_mu_t2_a: spatial.Location,
) -> wind_farm.TurbineConfiguration:
    """Test case instance 'Mu_T2_a' of ``TurbineSpecification``."""
    return wind_farm.TurbineConfiguration(
        id="b87f21bc-e1d8-4150-a2f4-d7f019bf96fc",
        label="Mu_T2_a",
        description="Configuration of the neighbouring Mu_T2_a turbine",
        location=turbine_location_mu_t2_a,
        ground_level_altitude=41.0,
        hub_height=125.0,
        turbine_model_id="e3288cbd-fa3b-4241-8a4c-3856fc10c55e",
    )


@pytest.fixture(scope="session")
def wind_farm_operational_restriction_a() -> wind_farm.OperationalRestriction:
    """Wind farm test case instance 'a' of ``OperationalRestriction``."""
    return wind_farm.OperationalRestriction(
        label="Temporary grid curtailment",
        description=(
            "The wind farm is required to initially curtail its grid "
            "export to a maximum of 10.0 MW due to grid upgrade works."
        ),
        start_datetime=dt.datetime(2024, 1, 1, 0, 0, 0),
        end_datetime=dt.datetime(2026, 1, 1, 0, 0, 0),
    )


@pytest.fixture(scope="session")
def wind_farm_a(
    turbine_specification_wtg01_a: wind_farm.TurbineConfiguration,
    turbine_specification_wtg02_a: wind_farm.TurbineConfiguration,
    wind_farm_operational_restriction_a: wind_farm.OperationalRestriction,
) -> wind_farm.WindFarmConfiguration:
    """Test case instance 'a' of ``WindFarm``."""
    return wind_farm.WindFarmConfiguration(
        id="bf_a",
        label="Barefoot Wind Farm",
        abbreviation="Barefoot",
        description="Barefoot Wind Farm configuration for Scenario A",
        turbines=[turbine_specification_wtg01_a, turbine_specification_wtg02_a],
        relevance=wind_farm.WindFarmRelevance.INTERNAL,
        assessment_period_start_date=dt.date(2024, 1, 1),
        assessment_period_end_date=dt.date(2054, 12, 31),
        installed_capacity=11.0,
        restrictions=[wind_farm_operational_restriction_a],
    )


@pytest.fixture(scope="session")
def wind_farm_b(
    turbine_specification_wtg01_b: wind_farm.TurbineConfiguration,
    turbine_specification_wtg02_b: wind_farm.TurbineConfiguration,
) -> wind_farm.WindFarmConfiguration:
    """Test case instance 'b' of ``WindFarm``."""
    return wind_farm.WindFarmConfiguration(
        id="bf_b",
        label="Barefoot Wind Farm",
        abbreviation="Barefoot",
        description="Barefoot Wind Farm configuration for Scenario B",
        comments="Secondary wind farm scenario",
        turbines=[turbine_specification_wtg01_b, turbine_specification_wtg02_b],
        relevance=wind_farm.WindFarmRelevance.INTERNAL,
        assessment_period_start_date=dt.date(2024, 1, 1),
        assessment_period_end_date=dt.date(2058, 12, 31),
        installed_capacity=11.6,
        export_capacity=11.5,
    )


@pytest.fixture(scope="session")
def neighbouring_wind_farm_a(
    turbine_specification_mu_t1_a: wind_farm.TurbineConfiguration,
    turbine_specification_mu_t2_a: wind_farm.TurbineConfiguration,
) -> wind_farm.WindFarmConfiguration:
    """Neighboring project test case instance 'a' of ``WindFarm``."""
    return wind_farm.WindFarmConfiguration(
        id="mu",
        label="Munro Wind Farm",
        abbreviation="MWF",
        description="The operational Munro Wind Farm",
        comments=(
            "Details taken from publicly available information; location "
            "data based on publicly available data and confirmed with "
            "satellite imagery."
        ),
        turbines=[turbine_specification_mu_t1_a, turbine_specification_mu_t2_a],
        relevance=wind_farm.WindFarmRelevance.EXTERNAL,
        assessment_period_start_date=dt.date(2018, 7, 1),
        assessment_period_end_date=dt.date(2038, 6, 30),
        installed_capacity=6.4,
    )


@pytest.fixture(scope="session")
def all_wind_farms(
    wind_farm_a: wind_farm.WindFarmConfiguration,
    wind_farm_b: wind_farm.WindFarmConfiguration,
    neighbouring_wind_farm_a: wind_farm.WindFarmConfiguration,
) -> list[wind_farm.WindFarmConfiguration]:
    """A list of all test case wind farm configurations."""
    return [wind_farm_a, wind_farm_b, neighbouring_wind_farm_a]


@pytest.fixture(scope="session")
def measurement_station_a_filepath(json_examples_dirpath: Path) -> Path:
    """Path to test case 'a' of measurement station metadata."""
    return (
        json_examples_dirpath / "iec_61400-15-2_eya_def_example_a_iea43_wra_mast.json"
    )


@pytest.fixture(scope="session")
def measurement_station_a(
    measurement_station_a_filepath: Path,
) -> iea43_wra_data_model.WraDataModelDocument:
    """Test case instance 'a' of measurement station metadata.."""
    with open(measurement_station_a_filepath, "r") as f:
        json_data_dict = json.load(f)

    return iea43_wra_data_model.WraDataModelDocument(json_data_dict)


@pytest.fixture(scope="session")
def reference_wind_farm_dataset_a() -> reference_wind_farm.OperationalDatasetMetadata:
    """Test case instance 'a' of ``ReferenceWindFarmDataset``."""
    return reference_wind_farm.OperationalDatasetMetadata(
        id="munro_wind_farm_reference_wtg_scada",
        label="WTG SCADA",
        classification=reference_wind_farm.SingleSourceDatasetClassification(
            data_type=reference_wind_farm.OperationalDataType.SCADA,
            data_source_type=reference_wind_farm.OperationalDataSourceType.SECONDARY,
        ),
        supplying_organisation=general.Organisation(
            name="Munro Wind Limited",
            abbreviation="Munro Wind",
            address="High Munro Walk, Glasgow, G12 0YE, UK",
        ),
        integrity_verification=(
            "The data were downloaded through direct connection to the "
            "site SCADA database. No further integrity verification "
            "was possible."
        ),
        time_resolution=general.TimeResolution(
            value=10, unit=general.TimeMeasurementUnit.MINUTE
        ),
        start_date=dt.date(2020, 1, 1),
        end_date=dt.date(2022, 12, 31),
        data_variables=[
            reference_wind_farm.OperationalDataVariable(
                variable_type=(
                    reference_wind_farm.OperationalDataVariableType.WIND_SPEED
                ),
                data_level=reference_wind_farm.OperationalDataLevel.TURBINE_LEVEL,
                statistic_types=[dataset.StatisticType.MEAN],
            ),
            reference_wind_farm.OperationalDataVariable(
                variable_type=(
                    reference_wind_farm.OperationalDataVariableType.YAW_ANGLE
                ),
                data_level=reference_wind_farm.OperationalDataLevel.TURBINE_LEVEL,
                statistic_types=[dataset.StatisticType.MEAN],
            ),
            reference_wind_farm.OperationalDataVariable(
                variable_type=(
                    reference_wind_farm.OperationalDataVariableType.ACTIVE_POWER
                ),
                data_level=reference_wind_farm.OperationalDataLevel.TURBINE_LEVEL,
                statistic_types=[dataset.StatisticType.MEAN],
            ),
            reference_wind_farm.OperationalDataVariable(
                variable_type=(
                    reference_wind_farm.OperationalDataVariableType.ROTOR_SPEED
                ),
                data_level=reference_wind_farm.OperationalDataLevel.TURBINE_LEVEL,
                statistic_types=[dataset.StatisticType.MEAN],
            ),
            reference_wind_farm.OperationalDataVariable(
                variable_type=(
                    reference_wind_farm.OperationalDataVariableType.AIR_TEMPERATURE
                ),
                comments="The sensor is mounted outside, below the nacelle.",
                data_level=reference_wind_farm.OperationalDataLevel.TURBINE_LEVEL,
                statistic_types=[dataset.StatisticType.MEAN],
            ),
        ],
    )


@pytest.fixture(scope="session")
def reference_wind_farm_a(
    reference_wind_farm_dataset_a: reference_wind_farm.OperationalDatasetMetadata,
) -> reference_wind_farm.ReferenceWindFarm:
    """Test case instance 'a' of ``ReferenceWindFarm``."""
    return reference_wind_farm.ReferenceWindFarm(
        wind_farm_id="mu",
        operational_datasets=[reference_wind_farm_dataset_a],
    )


@pytest.fixture(scope="session")
def reference_meteorological_dataset_a_filepath(json_examples_dirpath: Path) -> Path:
    """Path to test case 'a' of reference met dataset metadata."""
    return (
        json_examples_dirpath / "iec_61400-15-2_eya_def_example_a_iea43_wra_era5.json"
    )


@pytest.fixture(scope="session")
def reference_meteorological_dataset_a(
    reference_meteorological_dataset_a_filepath: Path,
) -> iea43_wra_data_model.WraDataModelDocument:
    """Test case instance 'a' of reference met dataset metadata."""
    with open(reference_meteorological_dataset_a_filepath, "r") as f:
        json_data_dict = json.load(f)

    return iea43_wra_data_model.WraDataModelDocument(json_data_dict)


@pytest.fixture(scope="session")
def wind_resource_assessment_a() -> wind_resource.WindResourceAssessment:
    """Test case instance 'a' of ``WindResourceAssessment``."""
    return wind_resource.WindResourceAssessment(
        id="BfWF_WRA_1",
        dataset_statistics=wind_resource.WindResourceDatasetStatistics(
            data_availability=[
                dataset.Dataset(
                    dimensions=[
                        dataset.DatasetDimension.WIND_DATASET_ID,
                        dataset.DatasetDimension.POINT_ID,
                        dataset.DatasetDimension.YEAR,
                        dataset.DatasetDimension.MONTH,
                    ],
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=[
                                (["BF_M1", "Spd_80.1_315", 2021, 1], 0.877),
                                (["BF_M1", "Spd_80.1_315", 2021, 2], 0.992),
                                (["BF_M1", "Spd_80mSE", 2021, 1], 0.886),
                                (["BF_M1", "Spd_80mSE", 2021, 2], 0.994),
                            ],
                        )
                    ],
                ),
                dataset.Dataset(
                    dimensions=[
                        dataset.DatasetDimension.WIND_FARM_ID,
                        dataset.DatasetDimension.OPERATIONAL_DATASET_ID,
                        dataset.DatasetDimension.VARIABLE_ID,
                        dataset.DatasetDimension.TURBINE_ID,
                        dataset.DatasetDimension.YEAR,
                        dataset.DatasetDimension.MONTH,
                    ],
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=[
                                (
                                    [
                                        "mu",
                                        "munro_wind_farm_reference_wtg_scada",
                                        "active_power",
                                        "f08b05bd-f90b-4833-91a5-4284b64c80db",
                                        2019,
                                        1,
                                    ],
                                    0.989,
                                ),
                                (
                                    [
                                        "mu",
                                        "munro_wind_farm_reference_wtg_scada",
                                        "active_power",
                                        "b87f21bc-e1d8-4150-a2f4-d7f019bf96fc",
                                        2019,
                                        1,
                                    ],
                                    0.991,
                                ),
                            ],
                        )
                    ],
                ),
            ],
        ),
        results=wind_resource.WindResourceResults(
            wind_speed=[
                dataset.Dataset(
                    dimensions=[
                        dataset.DatasetDimension.WIND_DATASET_ID,
                        dataset.DatasetDimension.HEIGHT,
                    ],
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=[
                                (
                                    ["BF_M1", 120.0],
                                    6.83,
                                ),
                                (
                                    ["BF_M1", 125.0],
                                    6.85,
                                ),
                                (
                                    ["BF_M1", 148.0],
                                    6.93,
                                ),
                                (
                                    ["BF_M1", 150.0],
                                    6.94,
                                ),
                                (
                                    ["BF_M1", 158.0],
                                    6.96,
                                ),
                                (
                                    ["BF_M1", 160.0],
                                    6.97,
                                ),
                            ],
                        ),
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.STANDARD_DEVIATION,
                            ),
                            values=[
                                (
                                    ["BF_M1", 120.0],
                                    0.27,
                                ),
                                (
                                    ["BF_M1", 125.0],
                                    0.27,
                                ),
                                (
                                    ["BF_M1", 148.0],
                                    0.29,
                                ),
                                (
                                    ["BF_M1", 150.0],
                                    0.29,
                                ),
                                (
                                    ["BF_M1", 158.0],
                                    0.31,
                                ),
                                (
                                    ["BF_M1", 160.0],
                                    0.31,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
            probability=[
                dataset.Dataset(
                    dimensions=[
                        dataset.DatasetDimension.WIND_DATASET_ID,
                        dataset.DatasetDimension.HEIGHT,
                        dataset.DatasetDimension.WIND_FROM_DIRECTION,
                        dataset.DatasetDimension.WIND_SPEED,
                    ],
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=[
                                (
                                    ["BF_M1", 120.0, 0.0, 2.5],
                                    0.1,
                                ),
                                (
                                    ["BF_M1", 120.0, 120.0, 2.5],
                                    0.2,
                                ),
                                (
                                    ["BF_M1", 120.0, 240.0, 2.5],
                                    0.3,
                                ),
                                (
                                    ["BF_M1", 120.0, 0.0, 10.0],
                                    0.1,
                                ),
                                (
                                    ["BF_M1", 120.0, 120.0, 10.0],
                                    0.2,
                                ),
                                (
                                    ["BF_M1", 120.0, 240.0, 10.0],
                                    0.1,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
            wind_shear_exponent=[
                dataset.Dataset(
                    dimensions=[dataset.DatasetDimension.WIND_DATASET_ID],
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=[
                                (
                                    ["BF_M1"],
                                    0.18,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
            temperature=[
                dataset.Dataset(
                    dimensions=[
                        dataset.DatasetDimension.WIND_DATASET_ID,
                        dataset.DatasetDimension.HEIGHT,
                    ],
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=[
                                (
                                    ["BF_M1", 120.0],
                                    1.234,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
            air_density=[
                dataset.Dataset(
                    dimensions=[
                        dataset.DatasetDimension.WIND_DATASET_ID,
                        dataset.DatasetDimension.HEIGHT,
                    ],
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=[
                                (
                                    ["BF_M1", 120.0],
                                    1.234,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


@pytest.fixture(scope="session")
def turbine_wind_resource_assessment_a() -> wind_resource.TurbineWindResourceAssessment:
    """Test case instance 'a' of ``TurbineWindResourceAssessment``."""
    return wind_resource.TurbineWindResourceAssessment(
        wind_resource_assessment_id_reference="BfWF_WRA_1",
        results=wind_resource.TurbineWindResourceResults(
            wind_speed=[
                dataset.Dataset(
                    dimensions=[dataset.DatasetDimension.TURBINE_ID],
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=[
                                (
                                    ["WTG01"],
                                    6.91,
                                ),
                                (
                                    ["WTG02"],
                                    6.95,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        weighting=wind_resource.TurbineWindResourceWeighting(
            source_wind_data=[
                dataset.Dataset(
                    dimensions=[
                        dataset.DatasetDimension.TURBINE_ID,
                        dataset.DatasetDimension.WIND_DATASET_ID,
                    ],
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=[
                                (
                                    ["WTG01", "BF_M1"],
                                    1.0,
                                ),
                                (
                                    ["WTG02", "BF_M1"],
                                    1.0,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


@pytest.fixture(scope="session")
def turbine_wind_resource_assessment_b() -> wind_resource.TurbineWindResourceAssessment:
    """Test case instance 'b' of ``TurbineWindResourceAssessment``."""
    return wind_resource.TurbineWindResourceAssessment(
        wind_resource_assessment_id_reference="BfWF_WRA_1",
        results=wind_resource.TurbineWindResourceResults(
            wind_speed=[
                dataset.Dataset(
                    dimensions=[dataset.DatasetDimension.TURBINE_ID],
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=[
                                (
                                    ["WTG01"],
                                    6.90,
                                ),
                                (
                                    ["WTG02"],
                                    6.94,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


@pytest.fixture(scope="session")
def long_term_adj_uncertainty_subcat_a() -> wind_uncertainty.WindUncertaintySubcategory:
    """Test case 'a' of long-term adjustment ``WindUncertaintySubcategory``."""
    return wind_uncertainty.WindUncertaintySubcategory(
        label=wind_uncertainty.WindUncertaintySubcategoryLabel.LONG_TERM_ADJUSTMENT,
        results=wind_uncertainty.WindUncertaintyResults(
            relative_wind_speed_uncertainty=[
                dataset.Dataset(
                    dimensions=None,
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.STANDARD_DEVIATION,
                            ),
                            values=0.025,
                        )
                    ],
                ),
                dataset.Dataset(
                    dimensions=[dataset.DatasetDimension.WIND_DATASET_ID],
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.STANDARD_DEVIATION,
                            ),
                            values=[
                                (
                                    ["BF_M1"],
                                    0.025,
                                )
                            ],
                        )
                    ],
                ),
            ],
        ),
    )


@pytest.fixture(scope="session")
def lt_consistency_uncertainty_subcat_a() -> (
    wind_uncertainty.WindUncertaintySubcategory
):
    """Test case 'a' of reference consistency ``WindUncertaintySubcategory``."""
    return wind_uncertainty.WindUncertaintySubcategory(
        label=(
            wind_uncertainty.WindUncertaintySubcategoryLabel.REFERENCE_DATA_CONSISTENCY
        ),
        results=wind_uncertainty.WindUncertaintyResults(
            relative_wind_speed_uncertainty=[
                dataset.Dataset(
                    dimensions=None,
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.STANDARD_DEVIATION,
                            ),
                            values=0.02,
                        )
                    ],
                ),
                dataset.Dataset(
                    dimensions=[dataset.DatasetDimension.WIND_DATASET_ID],
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.STANDARD_DEVIATION,
                            ),
                            values=[
                                (
                                    ["BF_M1"],
                                    0.02,
                                )
                            ],
                        )
                    ],
                ),
            ],
        ),
    )


@pytest.fixture(scope="session")
def historical_wind_uncertainty_category_a(
    long_term_adj_uncertainty_subcat_a: wind_uncertainty.WindUncertaintySubcategory,
    lt_consistency_uncertainty_subcat_a: wind_uncertainty.WindUncertaintySubcategory,
) -> wind_uncertainty.WindUncertaintyCategory:
    """Test case 'a' of historical ``WindUncertaintyCategory``."""
    return wind_uncertainty.WindUncertaintyCategory(
        label=wind_uncertainty.WindUncertaintyCategoryLabel.HISTORICAL_WIND_RESOURCE,
        subcategories=[
            long_term_adj_uncertainty_subcat_a,
            lt_consistency_uncertainty_subcat_a,
        ],
        results=wind_uncertainty.WindUncertaintyResults(
            relative_wind_speed_uncertainty=[
                dataset.Dataset(
                    dimensions=None,
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.STANDARD_DEVIATION,
                            ),
                            values=0.03201,
                        ),
                    ],
                ),
                dataset.Dataset(
                    dimensions=[dataset.DatasetDimension.WIND_DATASET_ID],
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.STANDARD_DEVIATION,
                            ),
                            values=[
                                (
                                    ["BF_M1"],
                                    0.03201,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


@pytest.fixture(scope="session")
def wind_uncertainty_assessment_a(
    historical_wind_uncertainty_category_a: wind_uncertainty.WindUncertaintyCategory,
) -> wind_uncertainty.WindUncertaintyAssessment:
    return wind_uncertainty.WindUncertaintyAssessment(
        categories=[historical_wind_uncertainty_category_a],
        results=wind_uncertainty.WindUncertaintyResults(
            relative_wind_speed_uncertainty=[
                dataset.Dataset(
                    dimensions=None,
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=0.48,
                        )
                    ],
                )
            ],
            relative_energy_uncertainty=[
                dataset.Dataset(
                    dimensions=None,
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=0.95,
                        )
                    ],
                )
            ],
        ),
        wind_speed_to_energy_sensitivity_factor=1.65,
    )


@pytest.fixture(scope="session")
def wind_uncertainty_assessment_b(
    historical_wind_uncertainty_category_a: wind_uncertainty.WindUncertaintyCategory,
) -> wind_uncertainty.WindUncertaintyAssessment:
    return wind_uncertainty.WindUncertaintyAssessment(
        categories=[historical_wind_uncertainty_category_a],
        results=wind_uncertainty.WindUncertaintyResults(
            relative_wind_speed_uncertainty=[
                dataset.Dataset(
                    dimensions=None,
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=0.47,
                        )
                    ],
                )
            ],
            relative_energy_uncertainty=[
                dataset.Dataset(
                    dimensions=None,
                    statistics=[
                        dataset.DatasetStatistic(
                            statistic=dataset.BasicStatistic(
                                statistic_type=dataset.StatisticType.MEAN,
                            ),
                            values=0.92,
                        )
                    ],
                )
            ],
        ),
        wind_speed_to_energy_sensitivity_factor=1.66,
    )


@pytest.fixture(scope="session")
def plant_performance_curtailment_category_a() -> (
    plant_performance.PlantPerformanceCategory
):
    """Curtailment test case instance 'a' of ``PlantPerformanceCategory``."""
    turbine_wise_result_components = [
        dataset.DatasetStatistic(
            statistic=dataset.BasicStatistic(
                statistic_type=dataset.StatisticType.MEAN,
            ),
            values=[
                (
                    ["WTG01"],
                    0.975,
                ),
                (
                    ["WTG02"],
                    0.983,
                ),
            ],
        ),
        dataset.DatasetStatistic(
            statistic=dataset.BasicStatistic(
                statistic_type=dataset.StatisticType.STANDARD_DEVIATION,
            ),
            values=[
                (
                    ["WTG01"],
                    0.006,
                ),
                (
                    ["WTG02"],
                    0.004,
                ),
            ],
        ),
        dataset.DatasetStatistic(
            statistic=dataset.InterAnnualVariabilityStatistic(
                statistic_type=dataset.StatisticType.INTER_ANNUAL_VARIABILITY,
            ),
            values=[
                (
                    ["WTG01"],
                    0.002,
                ),
                (
                    ["WTG02"],
                    0.001,
                ),
            ],
        ),
    ]
    return plant_performance.PlantPerformanceCategory(
        label=plant_performance.PlantPerformanceCategoryLabel.CURTAILMENT,
        subcategories=[
            plant_performance.PlantPerformanceSubcategory(
                label=(
                    plant_performance.PlantPerformanceSubcategoryLabel.LOAD_CURTAILMENT
                ),
                description=(
                    "Curtailment due to a wind sector management "
                    "strategy to reduce turbine loads."
                ),
                comments=(
                    "Considering curtailment strategy as specified by "
                    "the turbine manufacturer."
                ),
                basis="time_series_calculation",
                variability=general.TimeVariabilityType.STATIC,
                results=plant_performance.PlantPerformanceResults(
                    efficiency=[
                        dataset.Dataset(
                            dimensions=[dataset.DatasetDimension.TURBINE_ID],
                            statistics=turbine_wise_result_components,
                        )
                    ],
                ),
            )
        ],
        results=plant_performance.PlantPerformanceResults(
            efficiency=[
                dataset.Dataset(
                    description="Curtailment losses.",
                    dimensions=[dataset.DatasetDimension.TURBINE_ID],
                    statistics=turbine_wise_result_components,
                )
            ],
        ),
    )


@pytest.fixture(scope="session")
def plant_performance_curtailment_category_b() -> (
    plant_performance.PlantPerformanceCategory
):
    """Curtailment test case instance 'b' of ``PlantPerformanceCategory``."""
    turbine_wise_result_components = [
        dataset.DatasetStatistic(
            statistic=dataset.BasicStatistic(
                statistic_type=dataset.StatisticType.MEAN,
            ),
            values=[
                (
                    ["WTG01"],
                    0.95,
                ),
                (
                    ["WTG02"],
                    0.95,
                ),
            ],
        ),
        dataset.DatasetStatistic(
            statistic=dataset.BasicStatistic(
                statistic_type=dataset.StatisticType.STANDARD_DEVIATION,
            ),
            values=[
                (
                    ["WTG01"],
                    0.05,
                ),
                (
                    ["WTG02"],
                    0.05,
                ),
            ],
        ),
    ]
    return plant_performance.PlantPerformanceCategory(
        label=plant_performance.PlantPerformanceCategoryLabel.CURTAILMENT,
        subcategories=[
            plant_performance.PlantPerformanceSubcategory(
                label=(
                    plant_performance.PlantPerformanceSubcategoryLabel.LOAD_CURTAILMENT
                ),
                description=(
                    "A broad estimate of curtailment losses due to a "
                    "wind sector management strategy to reduce turbine "
                    "loads, in the absence of details from the turbine "
                    "manufacturer, provided by the client and not "
                    "independently verified."
                ),
                basis="project_specific_assumption",
                provenance=general.AssessmentComponentProvenance(
                    assessor_type="first_party",
                ),
                variability=general.TimeVariabilityType.STATIC,
                results=plant_performance.PlantPerformanceResults(
                    efficiency=[
                        dataset.Dataset(
                            dimensions=[dataset.DatasetDimension.TURBINE_ID],
                            statistics=turbine_wise_result_components,
                        )
                    ],
                ),
            )
        ],
        results=plant_performance.PlantPerformanceResults(
            efficiency=[
                dataset.Dataset(
                    description="Curtailment losses.",
                    dimensions=[dataset.DatasetDimension.TURBINE_ID],
                    statistics=turbine_wise_result_components,
                )
            ],
        ),
    )


@pytest.fixture(scope="session")
def energy_assessment_a(
    wind_uncertainty_assessment_a: wind_uncertainty.WindUncertaintyAssessment,
    plant_performance_curtailment_category_a: (
        plant_performance.PlantPerformanceCategory
    ),
) -> energy_assessment.EnergyAssessment:
    """Test case instance 'a' of ``EnergyAssessment``."""
    return energy_assessment.EnergyAssessment(
        gross_energy_assessment=energy_assessment.GrossEnergyAssessment(
            comments=(
                "Using an in-house calculation tool with a wind speed and "
                "direction frequency distribution association method."
            ),
            results=energy_assessment.GrossEnergyAssessmentResults(
                annual_energy_production=[
                    dataset.Dataset(
                        dimensions=[dataset.DatasetDimension.TURBINE_ID],
                        statistics=[
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=dataset.StatisticType.MEAN,
                                ),
                                values=[
                                    (
                                        ["WTG01"],
                                        15.5,
                                    ),
                                    (
                                        ["WTG02"],
                                        16.7,
                                    ),
                                ],
                            )
                        ],
                    ),
                    dataset.Dataset(
                        dimensions=None,
                        statistics=[
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=dataset.StatisticType.MEAN,
                                ),
                                values=32.2,
                            )
                        ],
                    ),
                ],
            ),
        ),
        wind_uncertainty_assessment=wind_uncertainty_assessment_a,
        plant_performance_assessment=plant_performance.PlantPerformanceAssessment(
            categories=[plant_performance_curtailment_category_a],
            results=plant_performance.PlantPerformanceResults(
                efficiency=[
                    dataset.Dataset(
                        dimensions=None,
                        statistics=[
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=dataset.StatisticType.MEAN,
                                ),
                                values=0.879,
                            ),
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=(
                                        dataset.StatisticType.STANDARD_DEVIATION
                                    ),
                                ),
                                values=0.071,
                            ),
                            dataset.DatasetStatistic(
                                statistic=dataset.InterAnnualVariabilityStatistic(
                                    statistic_type=(
                                        dataset.StatisticType.INTER_ANNUAL_VARIABILITY
                                    ),
                                ),
                                values=0.121,
                            ),
                        ],
                    )
                ]
            ),
        ),
        net_energy_assessment=energy_assessment.NetEnergyAssessment(
            comments=(
                "In-house calculation tool, using a frequency distribution "
                "approach and treating all wind uncertainty components and "
                "all plant performance loss components as independent."
            ),
            results=energy_assessment.NetEnergyAssessmentResults(
                annual_energy_production=[
                    dataset.Dataset(
                        dimensions=None,
                        statistics=[
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=dataset.StatisticType.MEDIAN,
                                ),
                                values=31.5286,
                            ),
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=(
                                        dataset.StatisticType.STANDARD_DEVIATION
                                    ),
                                    return_period=10.0,
                                ),
                                values=3.4681,
                            ),
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=(
                                        dataset.StatisticType.STANDARD_DEVIATION
                                    ),
                                    return_period=1.0,
                                ),
                                values=4.7293,
                            ),
                            dataset.DatasetStatistic(
                                statistic=dataset.ExceedanceLevelStatistic(
                                    statistic_type=(
                                        dataset.StatisticType.EXCEEDANCE_LEVEL
                                    ),
                                    probability=0.9,
                                    return_period=10.0,
                                ),
                                values=27.0894,
                            ),
                            dataset.DatasetStatistic(
                                statistic=dataset.ExceedanceLevelStatistic(
                                    statistic_type=(
                                        dataset.StatisticType.EXCEEDANCE_LEVEL
                                    ),
                                    probability=0.9,
                                    return_period=1.0,
                                ),
                                values=25.4751,
                            ),
                        ],
                    ),
                ],
                energy_production=[
                    dataset.Dataset(
                        dimensions=[
                            dataset.DatasetDimension.YEAR,
                            dataset.DatasetDimension.MONTH,
                        ],
                        statistics=[
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=dataset.StatisticType.MEAN,
                                ),
                                values=[([2030, 1], 12.1)],
                            ),
                        ],
                    )
                ],
            ),
        ),
    )


@pytest.fixture(scope="session")
def energy_assessment_b(
    wind_uncertainty_assessment_b: wind_uncertainty.WindUncertaintyAssessment,
    plant_performance_curtailment_category_b: (
        plant_performance.PlantPerformanceCategory
    ),
) -> energy_assessment.EnergyAssessment:
    """Test case instance 'b' of ``EnergyAssessment``."""
    return energy_assessment.EnergyAssessment(
        gross_energy_assessment=energy_assessment.GrossEnergyAssessment(
            results=energy_assessment.GrossEnergyAssessmentResults(
                annual_energy_production=[
                    dataset.Dataset(
                        dimensions=[dataset.DatasetDimension.TURBINE_ID],
                        statistics=[
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=dataset.StatisticType.MEAN,
                                ),
                                values=[
                                    (
                                        ["WTG01"],
                                        18.1,
                                    ),
                                    (
                                        ["WTG02"],
                                        18.9,
                                    ),
                                ],
                            )
                        ],
                    ),
                    dataset.Dataset(
                        dimensions=None,
                        statistics=[
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=dataset.StatisticType.MEAN,
                                ),
                                values=37.0,
                            )
                        ],
                    ),
                ],
            ),
        ),
        wind_uncertainty_assessment=wind_uncertainty_assessment_b,
        plant_performance_assessment=plant_performance.PlantPerformanceAssessment(
            categories=[plant_performance_curtailment_category_b],
            results=plant_performance.PlantPerformanceResults(
                efficiency=[
                    dataset.Dataset(
                        dimensions=None,
                        statistics=[
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=dataset.StatisticType.MEAN,
                                ),
                                values=0.897,
                            ),
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=(
                                        dataset.StatisticType.STANDARD_DEVIATION
                                    ),
                                ),
                                values=0.07,
                            ),
                            dataset.DatasetStatistic(
                                statistic=dataset.InterAnnualVariabilityStatistic(
                                    statistic_type=(
                                        dataset.StatisticType.INTER_ANNUAL_VARIABILITY
                                    ),
                                ),
                                values=0.12,
                            ),
                        ],
                    )
                ]
            ),
        ),
        net_energy_assessment=energy_assessment.NetEnergyAssessment(
            results=energy_assessment.NetEnergyAssessmentResults(
                annual_energy_production=[
                    dataset.Dataset(
                        dimensions=None,
                        statistics=[
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=dataset.StatisticType.MEDIAN,
                                ),
                                values=35.15,
                            ),
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=(
                                        dataset.StatisticType.STANDARD_DEVIATION
                                    ),
                                    return_period=10.0,
                                ),
                                values=4.5695,
                            ),
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=(
                                        dataset.StatisticType.STANDARD_DEVIATION
                                    ),
                                    return_period=1.0,
                                ),
                                values=5.7998,
                            ),
                            dataset.DatasetStatistic(
                                statistic=dataset.ExceedanceLevelStatistic(
                                    statistic_type=(
                                        dataset.StatisticType.EXCEEDANCE_LEVEL
                                    ),
                                    probability=0.9,
                                    return_period=10.0,
                                ),
                                values=29.301,
                            ),
                            dataset.DatasetStatistic(
                                statistic=dataset.ExceedanceLevelStatistic(
                                    statistic_type=(
                                        dataset.StatisticType.EXCEEDANCE_LEVEL
                                    ),
                                    probability=0.9,
                                    return_period=1.0,
                                ),
                                values=27.7263,
                            ),
                        ],
                    ),
                ],
                energy_production=[
                    dataset.Dataset(
                        dimensions=[
                            dataset.DatasetDimension.YEAR,
                            dataset.DatasetDimension.MONTH,
                        ],
                        statistics=[
                            dataset.DatasetStatistic(
                                statistic=dataset.BasicStatistic(
                                    statistic_type=dataset.StatisticType.MEAN,
                                ),
                                values=[([2030, 1], 12.0)],
                            ),
                        ],
                    )
                ],
            ),
        ),
    )


@pytest.fixture(scope="session")
def scenario_a(
    turbine_wind_resource_assessment_a: wind_resource.TurbineWindResourceAssessment,
    energy_assessment_a: energy_assessment.EnergyAssessment,
) -> scenario.Scenario:
    """Test case instance 'a' of ``Scenario``."""
    return scenario.Scenario(
        id="b6953ecb-f88b-4660-9f69-bedbbe4c240b",
        label="A",
        description="ABC165-5.5MW turbine model scenario",
        is_main_scenario=True,
        wind_farm_ids=["bf_a", "mu"],
        turbine_wind_resource_assessment=turbine_wind_resource_assessment_a,
        energy_assessment=energy_assessment_a,
    )


@pytest.fixture(scope="session")
def scenario_b(
    turbine_wind_resource_assessment_b: wind_resource.TurbineWindResourceAssessment,
    energy_assessment_b: energy_assessment.EnergyAssessment,
) -> scenario.Scenario:
    """Test case instance 'b' of ``Scenario``."""
    return scenario.Scenario(
        id="e27fefdf-cdd7-441f-a7a7-c4347514b4f7",
        label="B",
        description="PQR169-5.8MW turbine model scenario",
        comments="Site suitability of turbine model has not yet investigated.",
        is_main_scenario=False,
        wind_farm_ids=["bf_b", "mu"],
        turbine_wind_resource_assessment=turbine_wind_resource_assessment_b,
        energy_assessment=energy_assessment_b,
    )


@pytest.fixture(scope="session")
def all_scenarios(
    scenario_a: scenario.Scenario,
    scenario_b: scenario.Scenario,
) -> list[scenario.Scenario]:
    """A list of all test case scenarios."""
    return [scenario_a, scenario_b]


@pytest.fixture(scope="session")
def issuing_organisation_a() -> general.Organisation:
    """Issuing organisation test case instance 'a' of ``Organisation``."""
    return general.Organisation(
        name="The Torre Egger Consultants Limited",
        abbreviation="Torre Egger",
        address="5 Munro Road, Sgurrsville, G12 0YE, UK",
    )


@pytest.fixture(scope="session")
def receiving_organisations_a() -> general.Organisation:
    """receiving organisation test case instance 'a' of ``Organisation``."""
    return general.Organisation(
        name="Miranda Investments Limited",
        abbreviation="Miranda",
        address="9 Acosta St., Ivanslake, Republic of Miranda",
        contact_name="Luis Bunuel",
    )


@pytest.fixture(scope="session")
def main_author_a() -> eya_def_header.ReportContributor:
    """Main author test case instance 'a' of ``ReportContributor``."""
    return eya_def_header.ReportContributor(
        name="Joan Miro",
        email_address="j.miro@art.cat",
        contributor_type=eya_def_header.ReportContributorType.AUTHOR,
        contribution_comments="Main author",
        completion_date=dt.date(2022, 10, 5),
    )


@pytest.fixture(scope="session")
def second_author_a() -> eya_def_header.ReportContributor:
    """Second author test case instance 'a' of ``ReportContributor``."""
    return eya_def_header.ReportContributor(
        name="Andrei Tarkovsky",
        email_address="andrei.tarkovsky@cinema.com",
        contributor_type=eya_def_header.ReportContributorType.AUTHOR,
        contribution_comments="Second author",
        completion_date=dt.date(2022, 10, 5),
    )


@pytest.fixture(scope="session")
def verifier_a() -> eya_def_header.ReportContributor:
    """Verifier test case instance 'a' of ``ReportContributor``."""
    return eya_def_header.ReportContributor(
        name="Hanns Eisler",
        email_address="hannseisler@udk-berlin.de",
        contributor_type=eya_def_header.ReportContributorType.VERIFIER,
        completion_date=dt.date(2022, 10, 6),
    )


@pytest.fixture(scope="session")
def approver_a() -> eya_def_header.ReportContributor:
    """Approver test case instance 'a' of ``ReportContributor``."""
    return eya_def_header.ReportContributor(
        name="Kurt Weill",
        email_address="weill@broadway.com",
        contributor_type=eya_def_header.ReportContributorType.APPROVER,
        completion_date=dt.date(2022, 10, 7),
    )


@pytest.fixture(scope="session")
def eya_def_a(
    issuing_organisation_a: general.Organisation,
    receiving_organisations_a: general.Organisation,
    main_author_a: eya_def_header.ReportContributor,
    second_author_a: eya_def_header.ReportContributor,
    verifier_a: eya_def_header.ReportContributor,
    approver_a: eya_def_header.ReportContributor,
    all_wind_farms: list[wind_farm.WindFarmConfiguration],
    measurement_station_a: iea43_wra_data_model.WraDataModelDocument,
    reference_wind_farm_a: reference_wind_farm.ReferenceWindFarm,
    reference_meteorological_dataset_a: iea43_wra_data_model.WraDataModelDocument,
    all_turbine_models: list[turbine_model.TurbineModelSpecifications],
    wind_resource_assessment_a: wind_resource.WindResourceAssessment,
    all_scenarios: list[scenario.Scenario],
) -> eya_def.EyaDefDocument:
    """Test case instance 'a' of ``EyaDef``."""
    return eya_def.EyaDefDocument(
        **{
            "$id": (
                "https://example.com/api/v2/eya/report/"
                "id=b1396029-e9af-49f7-9599-534db175e53c.json"
            )
        },
        uuid=uuid_.UUID("b1396029-e9af-49f7-9599-534db175e53c"),
        title="Energy yield assessment of the Barefoot Wind Farm",
        description=(
            "Wind resource and energy yield assessment of the Barefoot "
            "Wind Farm based on one on-site meteorological mast and "
            "considering two different turbine scenarios."
        ),
        comments="Update to consider further on-site measurement data.",
        project_name="Barefoot Wind Farm",
        project_country=eya_def_header.Alpha2CountryCode("GB"),
        document_id="12345678",
        document_version="B",
        issue_date=dt.date(2022, 10, 7),
        contributors=[main_author_a, second_author_a, verifier_a, approver_a],
        issuing_organisations=[issuing_organisation_a],
        receiving_organisations=[receiving_organisations_a],
        contract_reference="P/UK/000765/001/B, 2022-11-30",
        confidentiality_classification="Confidential",
        epsg_srid=32630,
        utc_offset=0.0,
        wind_farms=all_wind_farms,
        measurement_stations=[measurement_station_a],
        reference_wind_farms=[reference_wind_farm_a],
        reference_meteorological_datasets=[reference_meteorological_dataset_a],
        wind_resource_assessments=[wind_resource_assessment_a],
        turbine_models=all_turbine_models,
        scenarios=all_scenarios,
    )


@pytest.fixture(scope="session")
def eya_def_a_tmp_filepath(
    eya_def_a: eya_def.EyaDefDocument,
    json_examples_tmp_dirpath: Path,
) -> Path:
    """The temporary path of the test case instance 'a' json file.

    :return: the directory path of the temporary json file
        representation of the example test case instance 'a'
    """
    eya_def_a_json = eya_def_a.model_dump_json(
        indent=2, exclude_none=True, by_alias=True
    )

    filepath = json_examples_tmp_dirpath / "iec_61400-15-2_eya_def_example_a.json"
    with open(filepath, "w") as f:
        f.write(eya_def_a_json)
    return filepath
