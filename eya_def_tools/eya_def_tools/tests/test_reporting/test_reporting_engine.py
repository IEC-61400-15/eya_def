import pandas as pd
import pandas.testing as pd_testing

from eya_def_tools.data_models import eya_def
from eya_def_tools.reporting import reporting_engine


def test_generate_iec_table_a_returns_correct_values(
    eya_def_a: eya_def.EyaDefDocument,
) -> None:
    iec_table_a = reporting_engine.generate_iec_table_a(eya_def_document=eya_def_a)

    expected_iec_table_a = pd.DataFrame(
        data={
            "A": [
                "11.00",
                "",
                "2",
                "ABC165-5.5MW",
                "5.50",
                "165.0",
                "150.0, 160.0",
            ],
            "B": [
                "11.60",
                "11.50",
                "2",
                "PQR169-5.8MW",
                "5.80",
                "169.0",
                "148.0, 158.0",
            ],
        },
        index=[
            "Installed capacity [MW]",
            "Export capacity [MW]",
            "Number of turbines",
            "Turbine model(s)",
            "Turbine rated power [MW]",
            "Turbine rotor diameter [m]",
            "Turbine hub height [m]",
        ],
    )

    pd_testing.assert_frame_equal(left=iec_table_a, right=expected_iec_table_a)
