"""Script to render graphical representations of the EYA DEF data model.

The graphics are rendered based on the ``pydantic`` data models in
``eya_def_tools.data_model.energy_yield_assessment`` using the
``erdantic`` package.

"""

import erdantic as erd

import eya_def_tools.data_models.wind_resource_assessment
from eya_def_tools.data_models import energy_yield_assessment as eya
from eya_def_tools.data_models import (
    organisation,
    reference_wind_farm,
    report_metadata,
    result,
    spatial,
    turbine_model,
)


def draw_eya_def_all_levels() -> None:
    """Draw diagram of all levels of the schema."""
    diagram = erd.create(eya.EnergyYieldAssessment)
    diagram.draw("eya_def_all_level.png")
    diagram.draw("eya_def_all_level.svg")


def draw_eya_def_top_level() -> None:
    """Draw diagram of the top level schema."""
    eya.EnergyYieldAssessment.update_forward_refs(**locals())

    diagram = erd.create(
        eya.EnergyYieldAssessment,
        termini=[
            report_metadata.ReportContributor,
            organisation.Organisation,
            spatial.CoordinateReferenceSystem,
            reference_wind_farm.ReferenceWindFarm,
            eya_def_tools.data_models.wind_resource_assessment.WindResourceAssessment,
            turbine_model.TurbineModel,
            eya.Scenario,
        ],
    )
    diagram.draw("eya_def_top_level.png")
    diagram.draw("eya_def_top_level.svg")


def draw_scenario() -> None:
    """Draw diagram of the scenario level schema."""
    diagram = erd.create(eya.Scenario)
    diagram.draw("scenario.png")
    diagram.draw("scenario.svg")


def draw_reference_wind_farm() -> None:
    """Draw diagram of the reference wind farm schema."""
    diagram = erd.create(reference_wind_farm.ReferenceWindFarm)
    diagram.draw("reference_wind_farm.png")
    diagram.draw("reference_wind_farm.svg")


def draw_results() -> None:
    """Draw diagram of the results level schema."""
    diagram = erd.create(result.Result)
    diagram.draw("results.png")
    diagram.draw("results.svg")


if __name__ == "__main__":
    draw_eya_def_all_levels()
    draw_eya_def_top_level()
    draw_scenario()
    draw_reference_wind_farm()
    draw_results()
