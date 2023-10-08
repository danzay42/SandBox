import pytest
from pytest_mock import MockFixture

from main import Context, Creator

def test_build(mocker: MockFixture):
    runner = mocker.MagicMock()
     
    mocker.patch.object(Creator, "__init__", return_value=None)
    cm = mocker.patch.object(Creator, "cm", mocker.Mock(), create=True)
    cm.__enter__ = mocker.Mock(return_value=runner)
    cm.__exit__ = mocker.Mock()
    
    Creator(Context()).build()
    
    print(runner.mock_calls)
    assert runner.call_count == 1
