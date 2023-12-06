"""Script to render graphical representations of the EYA DEF data model.

The graphics are rendered based on the ``pydantic`` data models in
``eya_def_tools``, using the ``erdantic`` package.

"""

import re
from typing import Final

import erdantic as erd

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.dataset import Dataset
from eya_def_tools.data_models.energy_assessment import EnergyAssessment
from eya_def_tools.data_models.eya_def import EyaDefDocument
from eya_def_tools.data_models.eya_def_header import ReportContributor
from eya_def_tools.data_models.general import Organisation
from eya_def_tools.data_models.plant_performance import PlantPerformanceAssessment
from eya_def_tools.data_models.reference_met_data import (
    ReferenceMeteorologicalDatasetMetadata,
)
from eya_def_tools.data_models.reference_wind_farm import ReferenceWindFarm
from eya_def_tools.data_models.scenario import Scenario
from eya_def_tools.data_models.wind_farm import WindFarmConfiguration
from eya_def_tools.data_models.wind_resource import (
    TurbineWindResourceAssessment,
    WindResourceAssessment,
)
from eya_def_tools.utils.doc_utils import eya_def_erdantic

eya_def_erdantic.use_custom_representations()


MODEL_CLASSES_TO_DRAW: Final[list[type[EyaDefBaseModel]]] = [
    EyaDefDocument,
    WindFarmConfiguration,
    ReferenceWindFarm,
    WindResourceAssessment,
    Scenario,
    TurbineWindResourceAssessment,
    PlantPerformanceAssessment,
    Dataset,
]


def draw_eya_def_top_level() -> None:
    """Draw diagram of the top level schema."""
    EyaDefDocument.model_rebuild(**locals())

    diagram = erd.create(
        EyaDefDocument,
        termini=[
            ReportContributor,
            Organisation,
            WindFarmConfiguration,
            ReferenceWindFarm,
            ReferenceMeteorologicalDatasetMetadata,
            WindResourceAssessment,
            Scenario,
        ],
    )

    diagram.draw("eya_def_document_top_level.png")
    diagram.draw("eya_def_document_top_level.svg")


def draw_scenario_reduced() -> None:
    """Draw reduced diagram of the scenario level schema."""
    diagram = erd.create(
        Scenario,
        termini=[
            TurbineWindResourceAssessment,
            EnergyAssessment,
        ],
    )
    diagram.draw("scenario_reduced.png")
    diagram.draw("scenario_reduced.svg")


def get_filename_for_model_class(model_class: type[EyaDefBaseModel]) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", model_class.__name__).lower()


def draw_full_diagram_for_model_class(model_class: type[EyaDefBaseModel]) -> None:
    diagram = erd.create(model_class)
    filename = get_filename_for_model_class(model_class=model_class)
    diagram.draw(f"{filename}.png")
    diagram.draw(f"{filename}.svg")


def main() -> None:
    draw_eya_def_top_level()
    draw_scenario_reduced()

    for model_class in MODEL_CLASSES_TO_DRAW:
        draw_full_diagram_for_model_class(model_class=model_class)


if __name__ == "__main__":
    main()
