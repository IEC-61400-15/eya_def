# -*- coding: utf-8 -*-
"""Script to render graphical representations of the EYA DEF data model.

The graphics are rendered based on the `pydantic` data models in
`eya_def_tools.data_model` using the `erdantic` package.

"""

import erdantic as erd

from eya_def_tools import data_model


data_model.EnergyAssessmentReport.update_forward_refs(**locals())

diagram = erd.create(
    data_model.EnergyAssessmentReport,
    termini=[
        data_model.CoordinateReferenceSystem,
        data_model.WindMeasurementCampaign,
        data_model.TurbineModel,
        data_model.MeasurementWindResourceAssessment,
        data_model.ReferenceTurbineAssessment,
        data_model.Scenario,
        data_model.ReportContributor
    ])
diagram.draw("eya_def_top_level.png")
diagram.draw("eya_def_top_level.svg")

diagram = erd.create(data_model.WindMeasurementCampaign)
diagram.draw("wind_measurement_campaign.png")
diagram.draw("wind_measurement_campaign.svg")

diagram = erd.create(data_model.Results)
diagram.draw("results.png")
diagram.draw("results.svg")
