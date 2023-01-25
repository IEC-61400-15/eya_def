"""Setup and fixtures for the ``eya_def_tools`` test module.

The data model component fixtures all have the scope of the entire test
session to avoid having to build them for every individual test. The
tests should therefore not alter any of the data model component
instances, which may cause interference with other tests. Tests that
involve modifications should create their own instances or make copies.

"""

import datetime as dt
import json
from pathlib import Path
from typing import Any

import pydantic as pdt
import pytest

from eya_def_tools.data_models import energy_yield_assessment as eya
from eya_def_tools.data_models import (
    enums,
    measurement_station,
    result,
    spatial,
    turbine_model,
    wind_farm,
)

TEST_INPUT_DATA_DIRNAME = "test_input_data"


@pytest.fixture(scope="session")
def test_input_data_dirpath() -> Path:
    """The path of the directory where test input data is located.

    :return: the directory path of test input data
    """
    dirpath = Path(__file__).parent
    return dirpath / TEST_INPUT_DATA_DIRNAME


@pytest.fixture(scope="session")
def top_level_dirpath() -> Path:
    """The path of the top-level project repository directory.

    The top-level is the git repository, one level above the python
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
def pydantic_json_schema(
    energy_yield_assessment_a: eya.EnergyYieldAssessment,
) -> dict[str, Any]:
    """A ``dict`` representation of the pydantic JSON Schema.

    :param energy_yield_assessment_a: the complete example test
        instance 'a' of the top-level ``EnergyYieldAssessment`` data
        model used as the primary test case
    :return: a ``dict`` representation of the pydantic data model JSON
        Schema exported from the ``EnergyYieldAssessment`` class
    """
    return energy_yield_assessment_a.final_json_schema()


@pytest.fixture(scope="session")
def pydantic_json_schema_tmp_path(
    pydantic_json_schema: dict[str, Any], tmp_path_factory: pytest.TempPathFactory
) -> Path:
    """The path to the temporary pydantic JSON Schema file.

    :param pydantic_json_schema: a ``dict`` representation of the pydantic
        JSON Schema exported from the ``EnergyYieldAssessment`` class
    :param tmp_path_factory: the ``pytest`` ``tmp_path_factory``
    :return: the path to the temporary JSON Schema file representation
        of the pydantic data model
    """
    tmp_dirpath = tmp_path_factory.mktemp("schema")
    filepath = tmp_dirpath / "iec_61400-15-2_eya_def.schema.json"
    with open(filepath, "w") as f:
        f.write(json.dumps(pydantic_json_schema, indent=2))
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
    filename_pattern = "iec_61400-15-2_eya_def_example*.json"
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
def coordinate_reference_system_a() -> spatial.CoordinateReferenceSystem:
    """Test case instance 'a' of ``CoordinateReferenceSystem``."""
    return spatial.CoordinateReferenceSystem(
        system_label="WGS 84 / UTM zone 30N",
        epsg_srid=32630,
        wkt=(
            'PROJCS["WGS 84 / UTM zone 30N",GEOGCS["WGS 84",DATUM["WGS_1984",'
            'SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],'
            'AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,'
            'AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,'
            'AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],'
            'PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],'
            'PARAMETER["central_meridian",-3],PARAMETER["scale_factor",0.9996],'
            'PARAMETER["false_easting",500000],PARAMETER["false_northing",0],'
            'UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],'
            'AXIS["Northing",NORTH],AUTHORITY["EPSG","32630"]]))'
        ),
    )


@pytest.fixture(scope="session")
def turbine_location_wtg01_a() -> spatial.Location:
    """Turbine test case instance 'WTG01_a' of ``Location``."""
    return spatial.Location(
        location_id="c697566d-cf38-4626-9cda-bc7a77230d48",
        label="WTG01",
        description="Planned location of WTG01",
        x=419665.0,
        y=6194240.0,
    )


@pytest.fixture(scope="session")
def turbine_location_wtg01_b() -> spatial.Location:
    """Turbine test case instance 'WTG01_b' of ``Location``."""
    return spatial.Location(
        location_id="ac230650-a5dc-42c7-b10c-c5a88b0e78e9",
        label="WTG01_b",
        description="Alternative location of WTG01",
        x=419675.0,
        y=6194260.0,
    )


@pytest.fixture(scope="session")
def turbine_location_wtg02_a() -> spatial.Location:
    """Turbine test case instance 'WTG02_a' of ``Location``."""
    return spatial.Location(
        location_id="c73f2e46-ba0b-4775-a2f3-b76e3c3b5012",
        label="WTG02",
        description="Planned location of WTG02",
        x=420665.0,
        y=6194240.0,
    )


@pytest.fixture(scope="session")
def turbine_location_wtg02_b() -> spatial.Location:
    """Turbine test case instance 'WTG02_b' of ``Location``."""
    return spatial.Location(
        location_id="c73f2e46-ba0b-4775-a2f3-b76e3c3b5012",
        label="WTG02_b",
        description="Alternative location of WTG02",
        comments=(
            "Environmentally challenging location; preliminary and "
            "requires investigation"
        ),
        x=420655.0,
        y=6194220.0,
    )


@pytest.fixture(scope="session")
def turbine_location_mu_t1_a() -> spatial.Location:
    """Turbine test case instance 'Mu_T1_a' of ``Location``."""
    return spatial.Location(
        location_id="79166b5c-7e55-485b-b7e7-24f835c5e40a",
        label="Mu_T1",
        description="Turbine T1 of the operational Munro Wind Farm",
        comments=(
            "Location based on publicly available data and confirmed "
            "with satellite imagery"
        ),
        x=419665.0,
        y=6195240.0,
    )


@pytest.fixture(scope="session")
def turbine_location_mu_t2_a() -> spatial.Location:
    """Turbine test case instance 'Mu_T2_a' of ``Location``."""
    return spatial.Location(
        location_id="dc4dba73-8f1c-494f-868e-e548f2a3923f",
        label="Mu_T2",
        description="Turbine T2 of the operational Munro Wind Farm",
        comments=(
            "Location based on publicly available data and confirmed "
            "with satellite imagery"
        ),
        x=419665.0,
        y=6195240.0,
    )


# TODO translate to IEA43 metadata model
# @pytest.fixture(scope='session')
# def measurement_location_a() -> eya.Location:
#     """Wind measurement test case instance 'a' of ``Location``."""
#     return eya.Location(
#         location_id="ee15ff84-6733-4858-9656-ba995d9b1022",
#         label='M1',
#         description="Verified location of Mast M1",
#         comments=(
#             "Documented in installation report and independently "
#             "confirmed"),
#         x=420165.0,
#         y=6194740.0)
#
#
# @pytest.fixture(scope='session')
# def measurement_station_a(
#     measurement_location_a
# ) -> eya.WindMeasurementCampaign:
#     """Test case instance 'a' of ``WindMeasurementCampaign``."""
#     return eya.WindMeasurementCampaign(
#         measurement_id="BF_M1_1.0.0",
#         name="Mast M1",
#         label="M1",
#         description=(
#             "Barefoot Wind Farm on-site meteorological mast"),
#         comments="Measurements were still ongoing at time of assessment.",
#         location=measurement_location_a,
#         metadata_ref=eya.MeasurementStationMetadata(
#             "/foo/bar/metadata_ref.json"))


# TODO add valid IEA43 metadata reference
@pytest.fixture(scope="session")
def measurement_station_a() -> measurement_station.MeasurementStationMetadata:
    """Dummy test case instance 'a' of ``MeasurementStationMetadata``."""
    return measurement_station.MeasurementStationMetadata("/foo/bar/metadata_ref.json")


# TODO - placeholder to be implemented
@pytest.fixture(scope="session")
def measurement_station_basis_a() -> measurement_station.MeasurementStationBasis:
    """Test case instance 'a' of ``MeasurementStationBasis``."""
    return measurement_station.MeasurementStationBasis()


# TODO add valid turbine model performance specification reference
@pytest.fixture(scope="session")
def turbine_model_a() -> turbine_model.TurbineModel:
    """Test case instance 'a' of ``TurbineModel``."""
    return turbine_model.TurbineModel(
        turbine_model_id="6ca5bc01-04b1-421a-a033-133304d6cc7f", label="ABC165-5.5MW"
    )


# TODO add valid turbine model performance specification reference
@pytest.fixture(scope="session")
def turbine_model_b() -> turbine_model.TurbineModel:
    """Test case instance 'b' of ``TurbineModel``."""
    return turbine_model.TurbineModel(
        turbine_model_id="e2914c83-f355-4cf2-9051-8e0f34aa3c03", label="PQR169-5.8MW"
    )


# TODO add valid turbine model performance specification reference
@pytest.fixture(scope="session")
def turbine_model_c() -> turbine_model.TurbineModel:
    """Test case instance 'c' of ``TurbineModel``."""
    return turbine_model.TurbineModel(
        turbine_model_id="e3288cbd-fa3b-4241-8a4c-3856fc10c55e", label="XYZ-3.2/140"
    )


# TODO expand definition of operational restriction
@pytest.fixture(scope="session")
def operational_restriction_a() -> wind_farm.OperationalRestriction:
    """Test case instance 'a' of ``OperationalRestriction``."""
    return wind_farm.OperationalRestriction(
        label="WSM curtailment",
        description=(
            "Wind sector management (WSM) curtailment as specified"
            "by the turbine manufacturer"
        ),
    )


@pytest.fixture(scope="session")
def turbine_specification_wtg01_a(
    turbine_location_wtg01_a: spatial.Location,
    operational_restriction_a: wind_farm.OperationalRestriction,
) -> wind_farm.TurbineConfiguration:
    """Test case instance 'WTG01_a' of ``TurbineSpecification``."""
    return wind_farm.TurbineConfiguration(
        turbine_id="2bbe1cb3-e9f3-42ad-be61-3657ea2ac174",
        label="WTG01_scenA",
        description="Configuration of WTG01 in Scenario A",
        location=turbine_location_wtg01_a,
        hub_height=150.0,
        turbine_model_id="6ca5bc01-04b1-421a-a033-133304d6cc7f",
        restrictions=[operational_restriction_a],
    )


@pytest.fixture(scope="session")
def turbine_specification_wtg01_b(
    turbine_location_wtg01_b: spatial.Location,
) -> wind_farm.TurbineConfiguration:
    """Test case instance 'WTG01_b' of ``TurbineSpecification``."""
    return wind_farm.TurbineConfiguration(
        turbine_id="f5cfd507-5550-4fbb-bdca-3dc6b1c6323c",
        label="WTG01_scenB",
        description="Configuration of WTG01 in Scenario B",
        location=turbine_location_wtg01_b,
        hub_height=148.0,
        turbine_model_id="e2914c83-f355-4cf2-9051-8e0f34aa3c03",
    )


@pytest.fixture(scope="session")
def turbine_specification_wtg02_a(
    turbine_location_wtg02_a: spatial.Location,
    operational_restriction_a: wind_farm.OperationalRestriction,
) -> wind_farm.TurbineConfiguration:
    """Test case instance 'WTG02_a' of ``TurbineSpecification``."""
    return wind_farm.TurbineConfiguration(
        turbine_id="39f9dd43-6322-4738-81af-6a65766b26e3",
        label="WTG02_scenA",
        description="Configuration of WTG02 in Scenario A",
        location=turbine_location_wtg02_a,
        hub_height=160.0,
        turbine_model_id="6ca5bc01-04b1-421a-a033-133304d6cc7f",
        restrictions=[operational_restriction_a],
    )


@pytest.fixture(scope="session")
def turbine_specification_wtg02_b(
    turbine_location_wtg02_b: spatial.Location,
) -> wind_farm.TurbineConfiguration:
    """Test case instance 'WTG02_b' of ``TurbineSpecification``."""
    return wind_farm.TurbineConfiguration(
        turbine_id="a5ee87e3-5254-45fb-a057-4548b8c0424c",
        label="WTG02_scenB",
        description="Configuration of WTG02 in Scenario B",
        location=turbine_location_wtg02_b,
        hub_height=158.0,
        turbine_model_id="e2914c83-f355-4cf2-9051-8e0f34aa3c03",
    )


@pytest.fixture(scope="session")
def turbine_specification_mu_t1_a(
    turbine_location_mu_t1_a: spatial.Location,
) -> wind_farm.TurbineConfiguration:
    """Test case instance 'Mu_T1_a' of ``TurbineSpecification``."""
    return wind_farm.TurbineConfiguration(
        turbine_id="f08b05bd-f90b-4833-91a5-4284b64c80db",
        label="Mu_T1_a",
        description="Configuration of the neighbouring Mu_T1_a turbine",
        location=turbine_location_mu_t1_a,
        hub_height=125.0,
        turbine_model_id="e3288cbd-fa3b-4241-8a4c-3856fc10c55e",
    )


@pytest.fixture(scope="session")
def turbine_specification_mu_t2_a(
    turbine_location_mu_t2_a: spatial.Location,
) -> wind_farm.TurbineConfiguration:
    """Test case instance 'Mu_T2_a' of ``TurbineSpecification``."""
    return wind_farm.TurbineConfiguration(
        turbine_id="b87f21bc-e1d8-4150-a2f4-d7f019bf96fc",
        label="Mu_T2_a",
        description="Configuration of the neighbouring Mu_T2_a turbine",
        location=turbine_location_mu_t2_a,
        hub_height=125.0,
        turbine_model_id="e3288cbd-fa3b-4241-8a4c-3856fc10c55e",
    )


@pytest.fixture(scope="session")
def wind_farm_a(
    turbine_specification_wtg01_a: wind_farm.TurbineConfiguration,
    turbine_specification_wtg02_a: wind_farm.TurbineConfiguration,
) -> wind_farm.WindFarmConfiguration:
    """Test case instance 'a' of ``WindFarm``."""
    return wind_farm.WindFarmConfiguration(
        name="Barefoot Wind Farm",
        label="Barefoot",
        description="Barefoot Wind Farm configuration for Scenario A",
        turbines=[turbine_specification_wtg01_a, turbine_specification_wtg02_a],
        relevance=enums.WindFarmRelevance.INTERNAL,
        operational_lifetime_start_date=dt.date(2024, 1, 1),
    )


@pytest.fixture(scope="session")
def wind_farm_b(
    turbine_specification_wtg01_b: wind_farm.TurbineConfiguration,
    turbine_specification_wtg02_b: wind_farm.TurbineConfiguration,
) -> wind_farm.WindFarmConfiguration:
    """Test case instance 'b' of ``WindFarm``."""
    return wind_farm.WindFarmConfiguration(
        name="Barefoot Wind Farm",
        label="Barefoot",
        description="Barefoot Wind Farm configuration for Scenario B",
        comments="Secondary wind farm scenario",
        turbines=[turbine_specification_wtg01_b, turbine_specification_wtg02_b],
        relevance=enums.WindFarmRelevance.INTERNAL,
        operational_lifetime_start_date=dt.date(2024, 1, 1),
    )


@pytest.fixture(scope="session")
def neighbouring_wind_farm_a(
    turbine_specification_mu_t1_a: wind_farm.TurbineConfiguration,
    turbine_specification_mu_t2_a: wind_farm.TurbineConfiguration,
) -> wind_farm.WindFarmConfiguration:
    """Neighboring project test case instance 'a' of ``WindFarm``."""
    return wind_farm.WindFarmConfiguration(
        name="Munro Wind Farm",
        label="MWF",
        description="The operational Munro Wind Farm",
        comments="Details taken from publicly available information.",
        turbines=[turbine_specification_mu_t1_a, turbine_specification_mu_t2_a],
        relevance=enums.WindFarmRelevance.EXTERNAL,
        operational_lifetime_start_date=dt.date(2018, 7, 1),
        operational_lifetime_end_date=dt.date(2038, 6, 30),
    )


@pytest.fixture(scope="session")
def wind_spatial_model_a() -> eya.CalculationModelSpecification:
    """Spatial model test case instance 'a' of ``CalculationModelSpecification``."""
    return eya.CalculationModelSpecification(
        name="VENTOS/M",
        description="VENTOS/M is a coupled CFD-mesoscale model.",
        comments="The simulations were run using 60 representative days.",
    )


@pytest.fixture(scope="session")
def regression_model_uncertainty_component_a() -> eya.UncertaintyComponent:
    """Regression model test case 'a' of ``UncertaintyComponent``."""
    return eya.UncertaintyComponent(
        label="Regression model uncertainty",
        results=result.Result(
            label="Regression model wind speed uncertainty per measurement station",
            assessment_period=enums.AssessmentPeriod.LIFETIME,
            dimensions=(enums.ResultsDimension.MEASUREMENT,),
            statistics=[
                result.ResultStatistic(
                    statistic_type=enums.StatisticType.STANDARD_DEVIATION,
                    values=[
                        (
                            ("BF_M1_1.0.0",),
                            0.025,
                        )
                    ],
                )
            ],
        ),
    )


@pytest.fixture(scope="session")
def long_term_consistency_uncertainty_component_a() -> eya.UncertaintyComponent:
    """Long-term consistency test case 'a' of ``UncertaintyComponent``."""
    return eya.UncertaintyComponent(
        label="Long-term consistency uncertainty",
        results=result.Result(
            label=(
                "Long-term consistency wind speed uncertainty "
                "per measurement station"
            ),
            assessment_period=enums.AssessmentPeriod.LIFETIME,
            dimensions=(enums.ResultsDimension.MEASUREMENT,),
            statistics=[
                result.ResultStatistic(
                    statistic_type=enums.StatisticType.STANDARD_DEVIATION,
                    values=[
                        (
                            ("BF_M1_1.0.0",),
                            0.02,
                        )
                    ],
                )
            ],
        ),
    )


@pytest.fixture(scope="session")
def measurement_wind_uncertainty_assessment_a(
    regression_model_uncertainty_component_a: eya.UncertaintyComponent,
    long_term_consistency_uncertainty_component_a: eya.UncertaintyComponent,
) -> eya.UncertaintyAssessment:
    """Measurement test case instance 'a' of ``UncertaintyAssessment``."""
    return eya.UncertaintyAssessment(
        categories={
            enums.UncertaintyCategoryLabel.HISTORICAL: eya.UncertaintyCategory(
                components=[
                    regression_model_uncertainty_component_a,
                    long_term_consistency_uncertainty_component_a,
                ],
                category_results=[
                    result.Result(
                        label="Historical wind resource uncertainty",
                        assessment_period=enums.AssessmentPeriod.LIFETIME,
                        dimensions=(enums.ResultsDimension.MEASUREMENT,),
                        statistics=[
                            result.ResultStatistic(
                                statistic_type=enums.StatisticType.STANDARD_DEVIATION,
                                values=[
                                    (
                                        ("BF_M1_1.0.0",),
                                        0.03201,
                                    )
                                ],
                            )
                        ],
                    )
                ],
            )
        }
    )


@pytest.fixture(scope="session")
def wind_resource_assessment_a(
    measurement_wind_uncertainty_assessment_a: eya.UncertaintyAssessment,
) -> eya.WindResourceAssessment:
    """Test case instance 'a' of ``WindResourceAssessment``."""
    return eya.WindResourceAssessment(
        results=[
            result.Result(
                label="Measurement-height long-term wind",
                assessment_period=enums.AssessmentPeriod.LIFETIME,
                dimensions=(enums.ResultsDimension.MEASUREMENT,),
                statistics=[
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.MEAN,
                        values=[
                            (
                                ("BF_M1_1.0.0",),
                                6.83,
                            )
                        ],
                    )
                ],
            )
        ],
        uncertainty_assessment=measurement_wind_uncertainty_assessment_a,
    )


# TODO - placeholder to be implemented
@pytest.fixture(scope="session")
def wind_resource_assessment_basis_a() -> eya.WindResourceAssessmentBasis:
    """Test case instance 'a' of ``WindResourceAssessmentBasis``."""
    return eya.WindResourceAssessmentBasis()


@pytest.fixture(scope="session")
def turbine_wind_resource_assessment_a(
    wind_spatial_model_a: eya.CalculationModelSpecification,
) -> eya.TurbineWindResourceAssessment:
    """Test case instance 'a' of ``TurbineWindResourceAssessment``."""
    return eya.TurbineWindResourceAssessment(
        turbine_wind_resource_results=[
            result.Result(
                label="Turbine-location hub-height long-term wind",
                assessment_period=enums.AssessmentPeriod.LIFETIME,
                dimensions=(enums.ResultsDimension.TURBINE,),
                statistics=[
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.MEAN,
                        values=[
                            (
                                ("WTG01",),
                                6.91,
                            ),
                            (
                                ("WTG02",),
                                6.95,
                            ),
                        ],
                    )
                ],
            )
        ],
        wind_spatial_models=[wind_spatial_model_a],
    )


@pytest.fixture(scope="session")
def turbine_wind_resource_assessment_b(
    wind_spatial_model_a: eya.CalculationModelSpecification,
) -> eya.TurbineWindResourceAssessment:
    """Test case instance 'b' of ``TurbineWindResourceAssessment``."""
    return eya.TurbineWindResourceAssessment(
        turbine_wind_resource_results=[
            result.Result(
                label="Turbine-location hub-height long-term wind",
                assessment_period=enums.AssessmentPeriod.LIFETIME,
                dimensions=(enums.ResultsDimension.TURBINE,),
                statistics=[
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.MEAN,
                        values=[
                            (
                                ("WTG01",),
                                6.90,
                            ),
                            (
                                ("WTG02",),
                                6.94,
                            ),
                        ],
                    )
                ],
            )
        ],
        wind_spatial_models=[wind_spatial_model_a],
    )


@pytest.fixture(scope="session")
def gross_energy_assessment_a() -> eya.GrossEnergyAssessment:
    """Test case instance 'a' of ``GrossEnergyAssessment``."""
    return eya.GrossEnergyAssessment(
        results=[
            result.Result(
                label="Gross yield",
                assessment_period=enums.AssessmentPeriod.LIFETIME,
                dimensions=(enums.ResultsDimension.TURBINE,),
                statistics=[
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.MEAN,
                        values=[
                            (
                                ("WTG01",),
                                15500.0,
                            ),
                            (
                                ("WTG02",),
                                16700.0,
                            ),
                        ],
                    )
                ],
            ),
            result.Result(
                label="Gross yield",
                assessment_period=enums.AssessmentPeriod.LIFETIME,
                dimensions=None,
                statistics=[
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.MEAN,
                        values=32200.0,
                    )
                ],
            ),
        ]
    )


@pytest.fixture(scope="session")
def gross_energy_assessment_b() -> eya.GrossEnergyAssessment:
    """Test case instance 'b' of ``GrossEnergyAssessment``."""
    return eya.GrossEnergyAssessment(
        results=[
            result.Result(
                label="Gross yield",
                assessment_period=enums.AssessmentPeriod.LIFETIME,
                dimensions=(enums.ResultsDimension.TURBINE,),
                statistics=[
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.MEAN,
                        values=[
                            (
                                ("WTG01",),
                                18100.0,
                            ),
                            (
                                ("WTG02",),
                                18900.0,
                            ),
                        ],
                    )
                ],
            ),
            result.Result(
                label="Gross yield",
                assessment_period=enums.AssessmentPeriod.LIFETIME,
                dimensions=None,
                statistics=[
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.MEAN,
                        values=37000.0,
                    )
                ],
            ),
        ]
    )


@pytest.fixture(scope="session")
def plant_performance_curtailment_category_a() -> eya.PlantPerformanceCategory:
    """Curtailment test case instance 'a' of ``PlantPerformanceCategory``."""
    result_components = [
        result.ResultStatistic(
            statistic_type=enums.StatisticType.MEAN,
            values=[
                (
                    ("WTG01",),
                    0.975,
                ),
                (
                    ("WTG02",),
                    0.983,
                ),
            ],
        ),
        result.ResultStatistic(
            statistic_type=enums.StatisticType.STANDARD_DEVIATION,
            values=[
                (
                    ("WTG01",),
                    0.005,
                ),
                (
                    ("WTG02",),
                    0.005,
                ),
            ],
        ),
    ]
    return eya.PlantPerformanceCategory(
        components=[
            eya.PlantPerformanceComponent(
                basis=enums.AssessmentBasis.TIMESERIES_CALCULATION,
                variability=enums.VariabilityType.STATIC_PROCESS,
                calculation_models=[
                    eya.CalculationModelSpecification(
                        name="Timeseries tool", comments="Internal toolset"
                    )
                ],
                results=result.Result(
                    label="Loads curtailment",
                    description=(
                        "Curtailment due to a wind sector management "
                        "strategy to reduce turbine loads."
                    ),
                    comments=(
                        "Considering curtailment strategy as specified by "
                        "the turbine manufacturer."
                    ),
                    assessment_period=enums.AssessmentPeriod.LIFETIME,
                    dimensions=(enums.ResultsDimension.TURBINE,),
                    statistics=result_components,
                ),
            )
        ],
        category_results=[
            result.Result(
                label="Curtailment",
                description="Curtailment losses.",
                assessment_period=enums.AssessmentPeriod.LIFETIME,
                dimensions=(enums.ResultsDimension.TURBINE,),
                statistics=result_components,
            )
        ],
    )


@pytest.fixture(scope="session")
def plant_performance_curtailment_category_b() -> eya.PlantPerformanceCategory:
    """Curtailment test case instance 'b' of ``PlantPerformanceCategory``."""
    result_components = [
        result.ResultStatistic(
            statistic_type=enums.StatisticType.MEAN,
            values=[
                (
                    ("WTG01",),
                    0.95,
                ),
                (
                    ("WTG02",),
                    0.95,
                ),
            ],
        ),
        result.ResultStatistic(
            statistic_type=enums.StatisticType.STANDARD_DEVIATION,
            values=[
                (
                    ("WTG01",),
                    0.05,
                ),
                (
                    ("WTG02",),
                    0.05,
                ),
            ],
        ),
    ]
    return eya.PlantPerformanceCategory(
        components=[
            eya.PlantPerformanceComponent(
                basis=enums.AssessmentBasis.PROJECT_SPECIFIC_ESTIMATE,
                variability=enums.VariabilityType.STATIC_PROCESS,
                results=result.Result(
                    label="Loads curtailment",
                    description=(
                        "Expected curtailment due to a wind sector "
                        "management to reduce turbine loads."
                    ),
                    comments=(
                        "A broad estimate of curtailment losses in "
                        "the absence of details from the turbine "
                        "manufacturer."
                    ),
                    assessment_period=enums.AssessmentPeriod.LIFETIME,
                    dimensions=(enums.ResultsDimension.TURBINE,),
                    statistics=result_components,
                ),
            )
        ],
        category_results=[
            result.Result(
                label="Curtailment",
                description="Curtailment losses.",
                assessment_period=enums.AssessmentPeriod.LIFETIME,
                dimensions=(enums.ResultsDimension.TURBINE,),
                statistics=result_components,
            )
        ],
    )


@pytest.fixture(scope="session")
def plant_performance_assessment_a(
    plant_performance_curtailment_category_a: eya.PlantPerformanceCategory,
) -> eya.PlantPerformanceAssessment:
    """Test case instance 'a' of ``PlantPerformanceAssessment``."""
    curtailment_category_label = enums.PlantPerformanceCategoryLabel.CURTAILMENT
    return eya.PlantPerformanceAssessment(
        categories={
            curtailment_category_label: plant_performance_curtailment_category_a
        },
        net_energy_results=[
            result.Result(
                label="Net yield",
                assessment_period=enums.AssessmentPeriod.LIFETIME,
                dimensions=None,
                statistics=[
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.MEDIAN,
                        values=31528.6,
                    ),
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.STANDARD_DEVIATION,
                        values=3468.1,
                    ),
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.P90,
                        values=27089.4,
                    ),
                ],
            ),
            result.Result(
                label="Net yield",
                assessment_period=enums.AssessmentPeriod.ANY_ONE_YEAR,
                dimensions=None,
                statistics=[
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.MEDIAN,
                        values=31528.6,
                    ),
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.STANDARD_DEVIATION,
                        values=4729.3,
                    ),
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.P90,
                        values=25475.1,
                    ),
                ],
            ),
        ],
    )


@pytest.fixture(scope="session")
def plant_performance_assessment_b(
    plant_performance_curtailment_category_b: eya.PlantPerformanceCategory,
) -> eya.PlantPerformanceAssessment:
    """Test case instance 'b' of ``PlantPerformanceAssessment``."""
    curtailment_category_label = enums.PlantPerformanceCategoryLabel.CURTAILMENT
    return eya.PlantPerformanceAssessment(
        categories={
            curtailment_category_label: plant_performance_curtailment_category_b
        },
        net_energy_results=[
            result.Result(
                label="Net yield",
                assessment_period=enums.AssessmentPeriod.LIFETIME,
                dimensions=None,
                statistics=[
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.MEDIAN,
                        values=35150.0,
                    ),
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.STANDARD_DEVIATION,
                        values=4569.5,
                    ),
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.P90,
                        values=29301.0,
                    ),
                ],
            ),
            result.Result(
                label="Net yield",
                assessment_period=enums.AssessmentPeriod.ANY_ONE_YEAR,
                dimensions=None,
                statistics=[
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.MEDIAN,
                        values=35150.0,
                    ),
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.STANDARD_DEVIATION,
                        values=5799.8,
                    ),
                    result.ResultStatistic(
                        statistic_type=enums.StatisticType.P90,
                        values=27726.3,
                    ),
                ],
            ),
        ],
    )


@pytest.fixture(scope="session")
def scenario_a(
    wind_resource_assessment_basis_a: eya.WindResourceAssessmentBasis,
    wind_farm_a: wind_farm.WindFarmConfiguration,
    neighbouring_wind_farm_a: wind_farm.WindFarmConfiguration,
    turbine_wind_resource_assessment_a: eya.TurbineWindResourceAssessment,
    gross_energy_assessment_a: eya.GrossEnergyAssessment,
    plant_performance_assessment_a: eya.PlantPerformanceAssessment,
) -> eya.Scenario:
    """Test case instance 'a' of ``Scenario``."""
    return eya.Scenario(
        scenario_id="b6953ecb-f88b-4660-9f69-bedbbe4c240b",
        label="A",
        description="ABC165-5.5MW turbine model scenario",
        is_main_scenario=True,
        operational_lifetime_length_years=30,
        wind_farms=[wind_farm_a, neighbouring_wind_farm_a],
        wind_resource_assessment_basis=wind_resource_assessment_basis_a,
        turbine_wind_resource_assessment=turbine_wind_resource_assessment_a,
        gross_energy_assessment=gross_energy_assessment_a,
        plant_performance_assessment=plant_performance_assessment_a,
    )


@pytest.fixture(scope="session")
def scenario_b(
    wind_resource_assessment_basis_a: eya.WindResourceAssessmentBasis,
    wind_farm_b: wind_farm.WindFarmConfiguration,
    neighbouring_wind_farm_a: wind_farm.WindFarmConfiguration,
    turbine_wind_resource_assessment_b: eya.TurbineWindResourceAssessment,
    gross_energy_assessment_b: eya.GrossEnergyAssessment,
    plant_performance_assessment_b: eya.PlantPerformanceAssessment,
) -> eya.Scenario:
    """Test case instance 'b' of ``Scenario``."""
    return eya.Scenario(
        scenario_id="e27fefdf-cdd7-441f-a7a7-c4347514b4f7",
        label="B",
        description="PQR169-5.8MW turbine model scenario",
        comments="Site suitability of turbine model has not yet investigated.",
        is_main_scenario=False,
        operational_lifetime_length_years=30,
        wind_farms=[wind_farm_b, neighbouring_wind_farm_a],
        wind_resource_assessment_basis=wind_resource_assessment_basis_a,
        turbine_wind_resource_assessment=turbine_wind_resource_assessment_b,
        gross_energy_assessment=gross_energy_assessment_b,
        plant_performance_assessment=plant_performance_assessment_b,
    )


@pytest.fixture(scope="session")
def issuing_organisation_a() -> eya.Organisation:
    """Issuing organisation test case instance 'a' of ``Organisation``."""
    return eya.Organisation(
        name="The Torre Egger Consultants Limited",
        abbreviation="Torre Egger",
        address="5 Munro Road, Sgurrsville, G12 0YE, UK",
    )


@pytest.fixture(scope="session")
def receiving_organisations_a() -> eya.Organisation:
    """receiving organisation test case instance 'a' of ``Organisation``."""
    return eya.Organisation(
        name="Miranda Investments Limited",
        abbreviation="Miranda",
        address="9 Acosta St., Ivanslake, Republic of Miranda",
        contact_name="Luis Bunuel",
    )


@pytest.fixture(scope="session")
def main_author_a() -> eya.ReportContributor:
    """Main author test case instance 'a' of ``ReportContributor``."""
    return eya.ReportContributor(
        name="Joan Miro",
        email_address=pdt.EmailStr("j.miro@art.cat"),
        contributor_type="author",
        contribution_comments="Main author",
        completion_date=dt.date(2022, 10, 5),
    )


@pytest.fixture(scope="session")
def second_author_a() -> eya.ReportContributor:
    """Second author test case instance 'a' of ``ReportContributor``."""
    return eya.ReportContributor(
        name="Andrei Tarkovsky",
        email_address=pdt.EmailStr("andrei.tarkovsky@cinema.com"),
        contributor_type="author",
        contribution_comments="Second author",
        completion_date=dt.date(2022, 10, 5),
    )


@pytest.fixture(scope="session")
def verifier_a() -> eya.ReportContributor:
    """Verifier test case instance 'a' of ``ReportContributor``."""
    return eya.ReportContributor(
        name="Hanns Eisler",
        email_address=pdt.EmailStr("hannseisler@udk-berlin.de"),
        contributor_type="verifier",
        completion_date=dt.date(2022, 10, 6),
    )


@pytest.fixture(scope="session")
def approver_a() -> eya.ReportContributor:
    """Approver test case instance 'a' of ``ReportContributor``."""
    return eya.ReportContributor(
        name="Kurt Weill",
        email_address=pdt.EmailStr("weill@broadway.com"),
        contributor_type="approver",
        completion_date=dt.date(2022, 10, 7),
    )


@pytest.fixture(scope="session")
def energy_yield_assessment_a(
    coordinate_reference_system_a: spatial.CoordinateReferenceSystem,
    measurement_station_a: measurement_station.MeasurementStationMetadata,
    turbine_model_a: turbine_model.TurbineModel,
    turbine_model_b: turbine_model.TurbineModel,
    turbine_model_c: turbine_model.TurbineModel,
    wind_resource_assessment_a: eya.WindResourceAssessment,
    scenario_a: eya.Scenario,
    scenario_b: eya.Scenario,
    issuing_organisation_a: eya.Organisation,
    receiving_organisations_a: eya.Organisation,
    main_author_a: eya.ReportContributor,
    second_author_a: eya.ReportContributor,
    verifier_a: eya.ReportContributor,
    approver_a: eya.ReportContributor,
) -> eya.EnergyYieldAssessment:
    """Test case instance 'a' of ``EnergyYieldAssessment``."""
    return eya.EnergyYieldAssessment(
        **{
            "$id": (
                "https://example.com/api/v2/eya/report/"
                "id=b1396029-e9af-49f7-9599-534db175e53c.json"
            )
        },
        title="Energy yield assessment of the Barefoot Wind Farm",
        description=(
            "Wind resource and energy yield assessment of the Barefoot "
            "Wind Farm based on one on-site meteorological mast and "
            "considering two different turbine scenarios."
        ),
        comments="Update to consider further on-site measurement data.",
        project_name="Barefoot Wind Farm",
        document_id="12345678",
        document_version="B",
        issue_date=dt.date(2022, 10, 7),
        contributors=[main_author_a, second_author_a, verifier_a, approver_a],
        issuing_organisations=[issuing_organisation_a],
        receiving_organisations=[receiving_organisations_a],
        contract_reference="P/UK/000765/001/B, 2022-11-30",
        confidentiality_classification="Confidential",
        coordinate_reference_system=coordinate_reference_system_a,
        measurement_stations=[],
        reference_wind_farms=[],
        wind_resource_assessments=[wind_resource_assessment_a],
        turbine_models=[turbine_model_a, turbine_model_b, turbine_model_c],
        scenarios=[scenario_a, scenario_b],
    )


@pytest.fixture(scope="session")
def energy_yield_assessment_a_tmp_filepath(
    energy_yield_assessment_a: eya.EnergyYieldAssessment,
    json_examples_tmp_dirpath: Path,
) -> Path:
    """The temporary path of the test case instance 'a' json file.

    :return: the directory path of the temporary json file
        representation of the example test case instance 'a'
    """
    filepath = json_examples_tmp_dirpath / "iec_61400-15-2_eya_def_example_a.json"
    with open(filepath, "w") as f:
        f.write(
            energy_yield_assessment_a.json(indent=2, exclude_none=True, by_alias=True)
        )
    return filepath
