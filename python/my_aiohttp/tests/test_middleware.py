import pytest
from aiohttp import web

from my_aiohttp import middleware
from unittest.mock import AsyncMock


@pytest.mark.parametrize()
async def test_middleware():
    request = web.Request()
    response = web.Response()

    mock = AsyncMock(return_value=response)

    result = await middleware(request, mock)

    assert result == response

