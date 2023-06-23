"""Reporting engine for the IEC 61400-15-2 EYA DEF.

This module provides functionality to generate report content from
instances of the EYA DEF data model.

"""

from pathlib import Path
from typing import TypeAlias

import pandas as pd

from eya_def_tools.data_models import eya_def

ReportingTableKey: TypeAlias = str  # TODO define enums


class ReportingEngine:
    """Engine for generating report tables from EYA DEF objects."""

    def __int__(self, output_dirpath: Path, number_precision: int) -> None:
        self.output_dirpath = output_dirpath
        self.number_precision = number_precision

    def generate_tables(
        self, eya_def_doc: eya_def.EyaDefDocument
    ) -> dict[ReportingTableKey, pd.DataFrame]:
        """Generate IEC 61400-15-2 tables from EYA DEF document.

        :param eya_def_doc: the ``EyaDef`` instance to generate tables for
        :return: a dictionary that maps table keys to pandas dataframe
            objects with table data
        """
        tables: dict[ReportingTableKey, pd.DataFrame] = {}
        print(eya_def_doc)
        # TODO placeholder function to be implemented

        return tables
