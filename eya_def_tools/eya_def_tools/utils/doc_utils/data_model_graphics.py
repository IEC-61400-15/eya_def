"""Script to render graphical representations of the EYA DEF data model.

The graphics are rendered based on the ``pydantic`` data models in
``eya_def_tools.data_model.energy_yield_assessment`` using the
``erdantic`` package.

"""

import erdantic as erd

from eya_def_tools.data_models.energy_assessment import EnergyAssessment
from eya_def_tools.data_models.eya_def import EyaDefDocument
from eya_def_tools.data_models.plant_performance import PlantPerformanceCategory
from eya_def_tools.data_models.reference_met_data import ReferenceMeteorologicalDataset
from eya_def_tools.data_models.reference_wind_farm import ReferenceWindFarm
from eya_def_tools.data_models.report_metadata import Organisation, ReportContributor
from eya_def_tools.data_models.result import Result
from eya_def_tools.data_models.scenario import Scenario
from eya_def_tools.data_models.turbine_model import TurbineModel
from eya_def_tools.data_models.wind_farm import WindFarmConfiguration
from eya_def_tools.data_models.wind_resource import (
    TurbineWindResourceAssessment,
    WindResourceAssessment,
)


def draw_eya_def_all_levels() -> None:
    """Draw diagram of all levels of the schema."""
    diagram = erd.create(EyaDefDocument)
    diagram.draw("eya_def_all_levels.png")
    diagram.draw("eya_def_all_levels.svg")


def draw_eya_def_top_level() -> None:
    """Draw diagram of the top level schema."""
    EyaDefDocument.update_forward_refs(**locals())

    diagram = erd.create(
        EyaDefDocument,
        termini=[
            ReportContributor,
            Organisation,
            ReferenceWindFarm,
            ReferenceMeteorologicalDataset,
            WindResourceAssessment,
            TurbineModel,
            Scenario,
        ],
    )
    diagram.draw("eya_def_top_level.png")
    diagram.draw("eya_def_top_level.svg")


def draw_scenario() -> None:
    """Draw diagram of the scenario level schema."""
    diagram = erd.create(Scenario)
    diagram.draw("scenario.png")
    diagram.draw("scenario.svg")


def draw_scenario_reduced() -> None:
    """Draw reduced diagram of the scenario level schema."""
    diagram = erd.create(
        Scenario,
        termini=[
            WindFarmConfiguration,
            TurbineWindResourceAssessment,
            EnergyAssessment,
        ],
    )
    diagram.draw("scenario_reduced.png")
    diagram.draw("scenario_reduced.svg")


def draw_plant_performance_category() -> None:
    """Draw diagram of the plant performance category level schema."""
    diagram = erd.create(PlantPerformanceCategory)
    diagram.draw("plant_performance_category.png")
    diagram.draw("plant_performance_category.svg")


def draw_reference_wind_farm() -> None:
    """Draw diagram of the reference wind farm schema."""
    diagram = erd.create(ReferenceWindFarm)
    diagram.draw("reference_wind_farm.png")
    diagram.draw("reference_wind_farm.svg")


def draw_results() -> None:
    """Draw diagram of the schema for results."""
    diagram = erd.create(Result)
    diagram.draw("results.png")
    diagram.draw("results.svg")


def draw_wind_resource_assessment() -> None:
    """Draw diagram of the wind resource assessment schema."""
    diagram = erd.create(WindResourceAssessment)
    diagram.draw("wind_resource_assessment.png")
    diagram.draw("wind_resource_assessment.svg")


def draw_turbine_wind_resource_assessment() -> None:
    """Draw diagram of the turbine wind resource assessment schema."""
    diagram = erd.create(TurbineWindResourceAssessment)
    diagram.draw("turbine_wind_resource_assessment.png")
    diagram.draw("turbine_wind_resource_assessment.svg")


if __name__ == "__main__":
    draw_eya_def_all_levels()
    draw_eya_def_top_level()
    draw_scenario()
    draw_scenario_reduced()
    draw_plant_performance_category()
    draw_reference_wind_farm()
    draw_results()
    draw_wind_resource_assessment()
    draw_turbine_wind_resource_assessment()
