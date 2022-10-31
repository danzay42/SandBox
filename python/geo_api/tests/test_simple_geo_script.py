import pytest
from script import Service


@pytest.mark.parametrize('tz1, tz2, res', [
    ("Europe/Moscow", "Asia/Tomsk", (-240.0, "-04:00")),
    ("Europe/Moscow", "Europe/Volgograd", (0.0, "+00:00")),
    ("Europe/Moscow", "Europe/Paris", (120.0, "+02:00")),
    ("US/Eastern", "Europe/Moscow", (-480.0, "-08:00")),
    ])
def test_timezone_diff(tz1, tz2, res):
    assert Service.timezone_diff(tz1, tz2) == res


