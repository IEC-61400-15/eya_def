# -*- coding: utf-8 -*-
"""Script to render graphical representations of the EYA DEF data model.

The graphics are rendered based on the ``pydantic`` data models in
``eya_def_tools.data_model`` using the ``erdantic`` package.

"""

import erdantic as erd

from eya_def_tools import data_model


def draw_eya_def_top_level() -> None:
    """Draw diagram representation of the top level data model.

    """
    data_model.EnergyYieldAssessment.update_forward_refs(**locals())

    diagram = erd.create(
        data_model.EnergyYieldAssessment,
        termini=[
            data_model.ReportContributor,
            data_model.Organisation,
            data_model.CoordinateReferenceSystem,
            data_model.ReferenceWindFarm,
            data_model.WindResourceAssessment,
            data_model.TurbineModel,
            data_model.Scenario,
        ])
    diagram.draw("eya_def_top_level.png")
    diagram.draw("eya_def_top_level.svg")


def draw_results() -> None:
    """Draw diagram representation of the results level data model.

    """
    diagram = erd.create(data_model.Results)
    diagram.draw("results.png")
    diagram.draw("results.svg")


if __name__ == "__main__":
    draw_eya_def_top_level()
    draw_results()
