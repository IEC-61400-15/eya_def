import datetime

import pytest

from eya_def_tools.data_models.eya_def_header import (
    EyaDefHeader,
    ReportContributor,
    ReportContributorType,
)
from eya_def_tools.data_models.general import Organisation


def test_invalid_epsg_raises_error() -> None:
    with pytest.raises(expected_exception=ValueError, match="Invalid EPSG SRID code"):
        _ = EyaDefHeader(
            title="My EYA report",
            project_name="My project",
            project_country="DE",
            issue_date=datetime.date.fromisoformat("2024-07-13"),
            contributors=[
                ReportContributor(
                    name="The author",
                    email_address="the.author@wind.eya",
                    contributor_type=ReportContributorType.AUTHOR,
                ),
            ],
            issuing_organisations=[
                Organisation(
                    name="My organisation",
                    abbreviation="MyOrg",
                    address="My address",
                    contact_name="The author",
                ),
            ],
            epsg_srid=-1,  # invalid
            utc_offset=0.0,
        )
