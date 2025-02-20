"""Reporting engine for the IEC 61400-15-2 EYA DEF.

This module provides functionality to generate report content from
instances of the EYA DEF data model.

"""

from collections.abc import Mapping

import pandas as pd

from eya_def_tools.data_models import eya_def
from eya_def_tools.data_models.power_curve_schema import PowerCurveDocument
from eya_def_tools.data_models.wind_farm import WindFarmRelevance


def generate_iec_table_a(eya_def_document: eya_def.EyaDefDocument) -> pd.DataFrame:
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
        columns=[scenario.label for scenario in eya_def_document.scenarios],
        dtype=str,
    )

    for scenario in eya_def_document.scenarios:
        internal_wind_farms = [
            wind_farm
            for wind_farm in eya_def_document.wind_farms
            if wind_farm.id in scenario.wind_farm_ids
            and wind_farm.relevance == WindFarmRelevance.INTERNAL
        ]
        internal_turbines = [
            turbine
            for wind_farm in internal_wind_farms
            for turbine in wind_farm.turbines
        ]
        internal_turbine_count = sum(
            len(wind_farm.turbines) for wind_farm in internal_wind_farms
        )
        internal_turbine_model_names = list(
            set(turbine.turbine_model for turbine in internal_turbines)
        )
        internal_turbine_hub_heights = sorted(
            list(set(f"{turbine.hub_height:.1f}" for turbine in internal_turbines))
        )

        power_curve_document_map = {
            power_curve["turbine"]["model_name"]: power_curve
            for power_curve in eya_def_document.power_curves
            if power_curve["turbine"]["model_name"] in internal_turbine_model_names
        }
        turbine_power_ratings = list(
            set(
                "{:.2f}".format(
                    _get_turbine_power_rating(
                        power_curve_document=power_curve_document_map[
                            turbine.turbine_model
                        ],
                        baseline_operating_mode=turbine.baseline_operating_mode,
                    )
                    * 1e-6  # Convert from W to MW
                )
                for turbine in internal_turbines
            )
        )
        rotor_diameters = list(
            set(
                "{:.1f}".format(float(power_curve["turbine"]["rotor_diameter"]))
                for power_curve in power_curve_document_map.values()
            )
        )

        installed_capacity_mw = (
            sum(wind_farm.installed_capacity for wind_farm in internal_wind_farms)
            * 1e-6  # Convert from W to MW
        )
        export_capacity_mw = (
            sum(
                (
                    wind_farm.export_capacity
                    if wind_farm.export_capacity is not None
                    else wind_farm.installed_capacity
                )
                for wind_farm in internal_wind_farms
            )
            * 1e-6  # Convert from W to MW
            if any(
                wind_farm.export_capacity is not None
                for wind_farm in internal_wind_farms
            )
            else ""
        )

        iec_table_a.at["Installed capacity [MW]", scenario.label] = (
            f"{installed_capacity_mw:.2f}"
        )
        iec_table_a.at["Export capacity [MW]", scenario.label] = (
            f"{export_capacity_mw:.2f}"
            if isinstance(export_capacity_mw, float)
            else str(export_capacity_mw)
        )
        iec_table_a.at["Number of turbines", scenario.label] = str(
            internal_turbine_count
        )
        iec_table_a.at["Turbine model(s)", scenario.label] = ", ".join(
            internal_turbine_model_names
        )
        iec_table_a.at["Turbine rated power [MW]", scenario.label] = ", ".join(
            turbine_power_ratings
        )
        iec_table_a.at["Turbine rotor diameter [m]", scenario.label] = ", ".join(
            rotor_diameters
        )
        iec_table_a.at["Turbine hub height [m]", scenario.label] = ", ".join(
            internal_turbine_hub_heights
        )

    return iec_table_a


def _get_turbine_power_rating(
    power_curve_document: PowerCurveDocument,
    baseline_operating_mode: str,
) -> float:
    for operating_mode in power_curve_document["power_curves"]["operating_modes"]:
        if operating_mode["label"] != baseline_operating_mode:
            continue

        overrides = operating_mode.get("overrides", None)
        if not isinstance(overrides, Mapping):
            continue

        rated_power = overrides.get("rated_power", None)
        if rated_power is not None:
            return float(rated_power)

    return float(power_curve_document["turbine"]["rated_power"])
