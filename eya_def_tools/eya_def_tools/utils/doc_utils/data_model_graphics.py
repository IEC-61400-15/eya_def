"""Script to render graphical representations of the EYA DEF data model.

The graphics are rendered based on the ``pydantic`` data models in
``eya_def_tools.data_model.energy_yield_assessment`` using the
``erdantic`` package.

"""

import erdantic as erd

from eya_def_tools.data_models import energy_yield_assessment, results


def draw_eya_def_all_levels() -> None:
    """Draw diagram representation of all levels of the data model."""
    diagram = erd.create(energy_yield_assessment.EnergyYieldAssessment)
    diagram.draw("eya_def_all_level.png")
    diagram.draw("eya_def_all_level.svg")


def draw_eya_def_top_level() -> None:
    """Draw diagram representation of the top level data model."""
    energy_yield_assessment.EnergyYieldAssessment.update_forward_refs(**locals())

    diagram = erd.create(
        energy_yield_assessment.EnergyYieldAssessment,
        termini=[
            energy_yield_assessment.ReportContributor,
            energy_yield_assessment.Organisation,
            energy_yield_assessment.CoordinateReferenceSystem,
            energy_yield_assessment.ReferenceWindFarm,
            energy_yield_assessment.WindResourceAssessment,
            energy_yield_assessment.TurbineModel,
            energy_yield_assessment.Scenario,
        ],
    )
    diagram.draw("eya_def_top_level.png")
    diagram.draw("eya_def_top_level.svg")


def draw_scenario() -> None:
    """Draw diagram representation of the scenario level data model."""
    diagram = erd.create(energy_yield_assessment.Scenario)
    diagram.draw("scenario.png")
    diagram.draw("scenario.svg")


def draw_results() -> None:
    """Draw diagram representation of the results level data model."""
    diagram = erd.create(results.Results)
    diagram.draw("results.png")
    diagram.draw("results.svg")


if __name__ == "__main__":
    draw_eya_def_all_levels()
    draw_eya_def_top_level()
    draw_scenario()
    draw_results()
