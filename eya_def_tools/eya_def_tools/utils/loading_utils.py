"""Utilities for loading data."""

import json
import urllib.request as urllib_request
from collections.abc import Mapping
from typing import Any


def load_json_schema(json_schema_uri: str) -> Mapping[str, Any]:
    """Load and parse an external JSON Schema into a mapping.

    :param json_schema_uri: the URI of the external JSON Schema to load
    """
    with urllib_request.urlopen(json_schema_uri) as url:
        json_schema = json.load(url)

    return json_schema
