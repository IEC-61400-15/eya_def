"""Test the ``data_models.dataset`` module.

"""

from eya_def_tools.data_models.dataset import ExceedanceLevelStatisticType


def test_exceedance_level_statistic_type_p_value() -> None:
    exceedance_level_statistic_type = ExceedanceLevelStatisticType(
        exceedance_level=0.999
    )
    assert exceedance_level_statistic_type.p_value_str == "P99.9"
