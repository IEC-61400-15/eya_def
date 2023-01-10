"""Base models for the IEC 61400-15-2 EYA DEF.

"""


from typing import Any, Mapping

import pydantic as pdt


class JsonPointerRef(str):
    """JSON Pointer reference."""

    def dict(self) -> dict[str, str]:
        """Get a ``dict`` representation of the reference.

        :return: a dict of the form ``{"$ref": "<reference_uri>"}``
        """
        return {"$ref": self.format()}

    def json(self) -> str:
        """Get a json ``str`` representation of the reference.

        :return: a string of the form ``{"$ref": "<reference_uri>"}``
        """
        return '{"$ref": "' + self.format() + '"}'


class BaseModelWithRefs(pdt.BaseModel):
    """Base model variant that includes JSON Pointer references."""

    @classmethod
    def get_ref_field_labels(cls) -> list[str]:
        """Get a list of the field labels that are references."""
        if len(cls.__fields__) == 0:
            return []
        ref_field_labels = []
        for field_key, field_val in cls.__fields__.items():
            if issubclass(field_val.type_, JsonPointerRef):
                ref_field_labels.append(field_key)
        return ref_field_labels

    @pdt.root_validator(pre=True)
    def convert_json_pointer_to_str(cls, values: Mapping[Any, Any]) -> dict[Any, Any]:
        """Convert all JSON Pointer references to ´str´.

        :param values: the pre-validation values (arguments) passed to
            the constructor
        :return: a ``dict`` copy of ``values`` where each JSON Pointer
            reference value of the form ``{"$ref": "<reference>"}`` is
            replaced by the ``str`` value of ``<reference>``
        """
        validated_values = {}
        for key, value in values.items():
            if (
                key in cls.get_ref_field_labels()
                and isinstance(value, dict)
                and len(value) == 1
                and isinstance(list(value.keys())[0], str)
                and list(value.keys())[0] == "$ref"
                and isinstance(list(value.values())[0], str)
            ):
                validated_values[key] = list(value.values())[0]
            elif key in cls.get_ref_field_labels() and isinstance(value, list):
                for item in value:
                    if (
                        isinstance(item, dict)
                        and len(item) == 1
                        and isinstance(list(item.keys())[0], str)
                        and list(item.keys())[0] == "$ref"
                        and isinstance(list(item.values())[0], str)
                    ):
                        if key not in validated_values:
                            validated_values[key] = [list(item.values())[0]]
                        else:
                            validated_values[key].append(list(item.values())[0])
                    else:
                        if key not in validated_values:
                            validated_values[key] = [item]
                        else:
                            validated_values[key].append(item)
            else:
                validated_values[key] = value
        return validated_values

    def dict(self, *args, **kwargs) -> dict:
        """A ``dict`` representation of the model instance.

        :param args: any positional arguments for
            ``pydantic.BaseModel.json``
        :param kwargs: any key-worded arguments for
            ``pydantic.BaseModel.json``
        :return: a ``dict`` representing the model instance
        """
        dict_repr = super().dict(*args, **kwargs)
        for ref_field_label in self.get_ref_field_labels():
            if (
                ref_field_label in dict_repr.keys()
                and dict_repr[ref_field_label] is not None
            ):
                field = getattr(self, ref_field_label)
                if isinstance(field, list):
                    dict_repr[ref_field_label] = []
                    for item in field:
                        dict_repr[ref_field_label].append(item.dict())
                else:
                    dict_repr[ref_field_label] = field.dict()
        return dict_repr

    def json(self, *args, **kwargs) -> str:
        """A json ``str`` representation of the model instance.

        :param args: any positional arguments for
            ``pydantic.BaseModel.json``
        :param kwargs: any key-worded arguments for
            ``pydantic.BaseModel.json``
        :return: a json ``str`` representing the model instance
        """
        json_repr = super().json(*args, **kwargs)
        for ref_field_label in self.get_ref_field_labels():
            field = getattr(self, ref_field_label)
            if isinstance(field, list):
                for item in set(field):
                    raw_ref_str = '"' + item.format() + '"'
                    ref_str = item.json()
                    json_repr = json_repr.replace(raw_ref_str, ref_str)
            else:
                raw_ref_str = '"' + getattr(self, ref_field_label).format() + '"'
                ref_str = getattr(self, ref_field_label).json()
                json_repr = json_repr.replace(raw_ref_str, ref_str)
        return json_repr
