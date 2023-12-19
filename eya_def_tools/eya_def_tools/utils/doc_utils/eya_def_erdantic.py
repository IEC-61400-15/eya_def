"""Adaptation of the erdantic package for the EYA DEF.

"""

from typing import Annotated, Any, List, Optional, Union, get_origin

import erdantic as erd
import erdantic.base as erd_base
import erdantic.typing as erd_typing
import pydantic as pdt

from eya_def_tools.data_models import reference_wind_farm
from eya_def_tools.data_models.base_model import EyaDefBaseModel
from eya_def_tools.data_models.reference_met_data import (
    ReferenceMeteorologicalDatasetMetadata,
)


class IEATask43WraDataModel:
    pass


class IEC61400x16PowerCurveDataModel:
    pass


# The ``erdantic`` package currently does not support the ``Literal``
# type, so the models ``SingleSourceDatasetClassification`` and
# ``DerivedDatasetClassification`` need a workaround here
class SingleSourceDatasetClassification(EyaDefBaseModel):
    data_type: reference_wind_farm.OperationalDataType = pdt.Field(
        default=...,
        description=(
            "The type of operational data, categorised as 'scada' for "
            "data from a Supervisory Control and Data Acquisition "
            "(SCADA) system, 'metered' for data from a production "
            "meter and 'environmental_measurement' for data from an "
            "(on-site) environmental measurement station such as a "
            "meteorological mast or a remote sensing device (RSD)."
        ),
    )
    data_source_type: reference_wind_farm.OperationalDataSourceType = pdt.Field(
        default=...,
        description=(
            "The type of the operational data source. Primary data, "
            "such as primary SCADA data, comes directly from the "
            "source without any intermediary. Secondary data covers "
            "all other types of data sources, where the data does not "
            "come directly from the source, such as secondary SCADA "
            "data provided in harmonised form by a data management "
            "service provider."
        ),
    )


class DerivedDatasetClassification(EyaDefBaseModel):
    data_type: reference_wind_farm.OperationalDataType = pdt.Field(
        default=reference_wind_farm.OperationalDataType.DERIVED,
        description=(
            "The type of operational data, categorised as 'derived' "
            "for all derived operational datasets (e.g. operational "
            "reports or databases with aggregate data). Details of "
            "the data type shall be included in the description of "
            "the operational dataset, including the type of derived "
            "dataset (e.g. an operational report), who produced it "
            "(e.g. the turbine OEM) and any relevant details known "
            "about how the data were processed."
        ),
    )
    data_source_type: reference_wind_farm.OperationalDataSourceType = pdt.Field(
        default=reference_wind_farm.OperationalDataSourceType.SECONDARY,
        description="The data source type, which for derived data is 'secondary'.",
    )


class PydanticField(erd.pydantic.PydanticField):  # type: ignore
    @property
    def type_obj(self) -> Union[type, erd_typing.GenericAlias]:
        """Return abbreviated form of annotations for diagrams."""
        if self.name == "measurement_stations":
            return Annotated[Optional[list[dict[str, Any]]], IEATask43WraDataModel]

        if self.name == "turbine_models":
            return Annotated[
                Optional[list[dict[str, Any]]], IEC61400x16PowerCurveDataModel
            ]

        if self.name == "reference_meteorological_datasets":
            return Optional[
                list[
                    ReferenceMeteorologicalDatasetMetadata
                    | Annotated[list[dict[str, Any]], IEATask43WraDataModel]
                ]
            ]

        # The ``erdantic`` package currently does not support the
        # ``Literal`` type, so the operational dataset classification
        # field needs a workaround
        if (
            self.name == "classification"
            and "Classification of the type of data" in self.field.description
        ):
            return SingleSourceDatasetClassification | DerivedDatasetClassification

        if (
            self.name == "values"
            and "Dataset value(s)" in self.field.description
            and get_origin(self.field.annotation) == Union
        ):
            return Union[
                float,
                list[tuple[list[Union[int, float, str]], float]],
            ]

        return super().type_obj


class PydanticModel(erd.pydantic.PydanticModel):  # type: ignore
    @property
    def fields(self) -> List[erd_base.Field]:
        return [
            PydanticField(name=name, field_info=field_info)
            for name, field_info in self.model.model_fields.items()
        ]


def use_custom_representations() -> None:
    """Use custom EYA DEF representations of pydantic models."""
    erd_base.register_model_adapter("pydantic")(PydanticModel)
