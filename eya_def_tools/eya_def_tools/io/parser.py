"""Parsing module for the EYA DEF."""

import json
from pathlib import Path

import ruamel.yaml as ryaml

from eya_def_tools.data_models.eya_def import EyaDefDocument


def parse_file(filepath: Path) -> EyaDefDocument:
    """Parse a JSON or YAML file into an EYA DEF document instance.

    Note that only YAML files that are fully compatible with JSON and
    JSON Schema are supported. It is recommended to serialize EYA DEF
    documents as JSON rather than YAML to ensure safe serialization and
    deserialization without compatibility issues.

    :param filepath: the path to the file to pase
    :return: an ``EyaDefDocument`` instance representation of the file
        contents
    """
    match filepath.suffix.lower():
        case ".json":
            return _parse_json_file(filepath=filepath)
        case ".yaml" | ".yml":
            return _parse_yaml_file(filepath=filepath)
        case _:
            raise ValueError(
                f"The EYA DEF parser does not support reading from the file format "
                f"'{filepath.suffix.lower()}'; only 'json' and 'yaml' are supported."
            )


def _parse_json_file(filepath: Path) -> EyaDefDocument:
    with open(filepath) as f:
        json_dict = json.load(f)

    return EyaDefDocument(**json_dict)


def _parse_yaml_file(filepath: Path) -> EyaDefDocument:
    yaml = ryaml.YAML(typ="safe")
    with open(filepath) as f:
        yaml_dict = yaml.load(f)

    return EyaDefDocument(**yaml_dict)
