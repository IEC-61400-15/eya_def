"""Writer module for the EYA DEF.

"""

import json
from pathlib import Path

import ruamel.yaml as ryaml

from eya_def_tools.data_models.eya_def import EyaDefDocument


def write_file(model: EyaDefDocument, filepath: Path) -> None:
    """Write an EYA DEF document instance to file.

    The JSON and YAML file formats are supported. It is recommended to
    use JSON, to ensure safe serialization and deserialization without
    compatibility issues.

    :param model: the ``EyaDefDocument`` model instance to export
    :param filepath: the path of the file to write to, which must have
        the suffix 'json' or 'yaml' and will be overwritten if an
        existing path
    """
    match filepath.suffix.lower():
        case ".json":
            _write_json_file(model=model, filepath=filepath)
        case ".yaml" | ".yml":
            _write_yaml_file(model=model, filepath=filepath)
        case _:
            raise ValueError(
                f"The EYA DEF writer does not support output to the file format "
                f"'{filepath.suffix.lower()}'; only 'json' and 'yaml' are supported."
            )


def _write_json_file(model: EyaDefDocument, filepath: Path) -> None:
    with open(filepath, "w") as f:
        f.write(model.model_dump_json(indent=2, exclude_none=True, by_alias=True))


def _write_yaml_file(model: EyaDefDocument, filepath: Path) -> None:
    # Pydantic does not have built-in support for YAML serialisation;
    # lacking that, this instead uses the pydantic JSON serializer,
    # converts back to a JSON-compliant dictionary and then passes that
    # to ruamel.yaml to serialize as YAML
    model_json = model.model_dump_json(exclude_none=True, by_alias=True)
    model_dict = json.loads(model_json)

    yaml_dumper = _get_default_yaml_dumper()

    with open(filepath, "w") as f:
        yaml_dumper.dump(model_dict, f)


def _get_default_yaml_dumper() -> ryaml.YAML:
    yaml = ryaml.YAML(typ="safe")

    yaml.default_flow_style = False
    yaml.width = 500

    return yaml
