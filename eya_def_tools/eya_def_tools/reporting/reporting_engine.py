"""Reporting engine for the IEC 61400-15-2 EYA DEF.

This module provides functionality to generate report content from
instances of the EYA DEF data model.

"""

from pathlib import Path

import pandas as pd

from eya_def_tools.data_models import eya_def
from eya_def_tools.reporting import table_definitions


class ReportingEngine:
    """Engine for generating report tables from EYA DEF objects."""

    def __int__(self, output_dirpath: Path, number_precision: int) -> None:
        self.output_dirpath = output_dirpath
        self.number_precision = number_precision

    def generate_tables(
        self, energy_yield_assessment: eya_def.EyaDef
    ) -> dict[table_definitions.ReportingTableKey, pd.DataFrame]:
        """Generate IEC 61400-15-2 tables from EYA DEF document.

        :param energy_yield_assessment: the ``EnergyYieldAssessment``
            instance to generate tables for
        :return: a dictionary that maps table keys to pandas dataframe
            objects with table data
        """
        tables: dict[table_definitions.ReportingTableKey, pd.DataFrame] = {}

        # TODO placeholder function to be implemented

        return tables
