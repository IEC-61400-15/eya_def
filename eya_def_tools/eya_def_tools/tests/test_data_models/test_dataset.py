"""Test the ``data_models.dataset`` module.

"""

from eya_def_tools.data_models.dataset import ExceedanceLevelStatistic


def test_exceedance_level_statistic_type_p_value() -> None:
    exceedance_level_statistic_type = ExceedanceLevelStatistic(probability=0.999)
    assert exceedance_level_statistic_type.p_value_str == "P99.9"
