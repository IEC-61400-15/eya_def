"""Configuration file for the Sphinx documentation builder."""

import sys
from pathlib import Path

file_dirpath = Path(__file__).parent
top_level_dirpath = file_dirpath.parent
sys.path.insert(0, str(top_level_dirpath.absolute()))

project = "IEC 61400-15-2 Reporting Digital Exchange Format (DEF) Python toolset"
copyright = "2022, IEC"
author = "Christian Jonsson et al."
release = "0.0.1"

extensions = ["sphinx.ext.duration", "sphinx.ext.autodoc", "sphinx.ext.autosummary"]

autosummary_generate = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "nature"
html_static_path = ["_static"]
