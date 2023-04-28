"""Script to render graphical representations of the EYA DEF data model.

The graphics are rendered based on the ``pydantic`` data models in
``eya_def_tools.data_model.energy_yield_assessment`` using the
``erdantic`` package.

"""

import erdantic as erd

from eya_def_tools.data_models import assessment_results
from eya_def_tools.data_models import eya_def as eya
from eya_def_tools.data_models import (
    organisation,
    reference_wind_farm,
    report_metadata,
    spatial,
    turbine_model,
    wind_resource,
)


def draw_eya_def_all_levels() -> None:
    """Draw diagram of all levels of the schema."""
    diagram = erd.create(eya.EyaDef)
    diagram.draw("eya_def_all_levels.png")
    diagram.draw("eya_def_all_levels.svg")


def draw_eya_def_top_level() -> None:
    """Draw diagram of the top level schema."""
    eya.EyaDef.update_forward_refs(**locals())

    diagram = erd.create(
        eya.EyaDef,
        termini=[
            report_metadata.ReportContributor,
            organisation.Organisation,
            spatial.CoordinateReferenceSystem,
            reference_wind_farm.ReferenceWindFarm,
            wind_resource.WindResourceAssessment,
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
    diagram = erd.create(assessment_results.Result)
    diagram.draw("results.png")
    diagram.draw("results.svg")


if __name__ == "__main__":
    draw_eya_def_all_levels()
    draw_eya_def_top_level()
    draw_scenario()
    draw_reference_wind_farm()
    draw_results()
