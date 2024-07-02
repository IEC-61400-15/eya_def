"""Script to render graphical representations of the EYA DEF data model.

The graphics are rendered based on the ``pydantic`` data models in
``eya_def_tools``, using the ``erdantic`` package.

"""

import re
from typing import Final

from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.dataset import Dataset
from eya_def_tools.data_models.energy_assessment import EnergyAssessment
from eya_def_tools.data_models.eya_def import EyaDefDocument
from eya_def_tools.data_models.eya_def_header import ReportContributor
from eya_def_tools.data_models.general import Organisation
from eya_def_tools.data_models.plant_performance import PlantPerformanceAssessment
from eya_def_tools.data_models.reference_wind_farm import ReferenceWindFarm
from eya_def_tools.data_models.scenario import Scenario
from eya_def_tools.data_models.wind_farm import WindFarmConfiguration
from eya_def_tools.data_models.wind_resource import (
    TurbineWindResourceAssessment,
    WindResourceAssessment,
)
from eya_def_tools.utils.doc_utils import eya_def_erdantic

eya_def_erdantic.register_plugin()


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

    diagram = eya_def_erdantic.create(
        EyaDefDocument,
        terminal_models=[
            ReportContributor,
            Organisation,
            WindFarmConfiguration,
            ReferenceWindFarm,
            WindResourceAssessment,
            Scenario,
        ],
    )

    draw_to_files(diagram=diagram, filename="eya_def_document_top_level")


def draw_scenario_reduced() -> None:
    """Draw reduced diagram of the scenario level schema."""
    diagram = eya_def_erdantic.create(
        Scenario,
        terminal_models=[
            TurbineWindResourceAssessment,
            EnergyAssessment,
        ],
    )

    draw_to_files(diagram=diagram, filename="scenario_reduced")


def get_filename_for_model_class(model_class: type[EyaDefBaseModel]) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", model_class.__name__).lower()


def draw_full_diagram_for_model_class(model_class: type[EyaDefBaseModel]) -> None:
    diagram = eya_def_erdantic.create(model_class)
    filename = get_filename_for_model_class(model_class=model_class)
    draw_to_files(diagram=diagram, filename=filename)


def draw_to_files(
    diagram: eya_def_erdantic.EyaDefEntityRelationshipDiagram,
    filename: str,
) -> None:
    diagram.draw(f"{filename}.svg")
    diagram.draw(f"{filename}.png")


def main() -> None:
    draw_eya_def_top_level()
    draw_scenario_reduced()

    for model_class in MODEL_CLASSES_TO_DRAW:
        draw_full_diagram_for_model_class(model_class=model_class)


if __name__ == "__main__":
    main()
