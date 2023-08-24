"""Adaptation of the erdantic package for the EYA DEF.

"""

from typing import Annotated, Any, List, Optional, Union

import erdantic as erd
import erdantic.base as erd_base
import erdantic.typing as erd_typing


class IEATask43WraDataModel:
    pass


class IEC61400x16PowerCurveDataModel:
    pass


class PydanticField(erd.pydantic.PydanticField):  # type: ignore
    @property
    def type_obj(self) -> Union[type, erd_typing.GenericAlias]:
        # Return abbreviated form of annotations for diagrams
        if self.name == "measurement_stations":
            return Annotated[Optional[list[dict[str, Any]]], IEATask43WraDataModel]
        if self.name == "turbine_models":
            return Annotated[
                Optional[list[dict[str, Any]]], IEC61400x16PowerCurveDataModel
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
