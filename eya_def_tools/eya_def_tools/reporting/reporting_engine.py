"""Reporting engine for the IEC 61400-15-2 EYA DEF.

This module provides functionality to generate report content from
instances of the EYA DEF data model.

"""

import pandas as pd

from eya_def_tools.data_models import eya_def
from eya_def_tools.data_models.wind_farm import WindFarmRelevance


def generate_iec_table_a(eya_def_doc: eya_def.EyaDefDocument) -> pd.DataFrame:
    iec_table_a = pd.DataFrame(
        index=[
            "Installed capacity [MW]",
            "Export capacity [MW]",
            "Number of turbines",
            "Turbine model(s)",
            "Turbine rated power [MW]",
            "Turbine rotor diameter [m]",
            "Turbine hub height [m]",
        ],
        columns=[scenario.label for scenario in eya_def_doc.scenarios],
        dtype=str,
    )

    for scenario in eya_def_doc.scenarios:
        internal_wind_farms = [
            wind_farm
            for wind_farm in eya_def_doc.wind_farms
            if wind_farm.id in scenario.wind_farm_ids
            and wind_farm.relevance == WindFarmRelevance.INTERNAL
        ]
        internal_turbines = [
            turbine
            for wind_farm in internal_wind_farms
            for turbine in wind_farm.turbines
        ]

        installed_capacity = sum(
            wind_farm.installed_capacity for wind_farm in internal_wind_farms
        )

        export_capacity = (
            sum(
                (
                    wind_farm.export_capacity
                    if wind_farm.export_capacity is not None
                    else wind_farm.installed_capacity
                )
                for wind_farm in internal_wind_farms
            )
            if any(
                wind_farm.export_capacity is not None
                for wind_farm in internal_wind_farms
            )
            else ""
        )

        turbine_count = sum(
            len(wind_farm.turbines) for wind_farm in internal_wind_farms
        )

        iec_table_a.at["Installed capacity [MW]", scenario.label] = (
            f"{installed_capacity:.2f}"
        )

        iec_table_a.at["Export capacity [MW]", scenario.label] = (
            f"{export_capacity:.2f}"
            if isinstance(export_capacity, float)
            else str(export_capacity)
        )

        iec_table_a.at["Number of turbines", scenario.label] = str(turbine_count)

        iec_table_a.at["Turbine model(s)", scenario.label] = ""  # TODO

        iec_table_a.at["Turbine rated power [MW]", scenario.label] = ""  # TODO

        iec_table_a.at["Turbine rotor diameter [m]", scenario.label] = ""  # TODO

        iec_table_a.at["Turbine hub height [m]", scenario.label] = ", ".join(
            sorted(
                list(set(f"{turbine.hub_height:.1f}" for turbine in internal_turbines))
            )
        )

    return iec_table_a
