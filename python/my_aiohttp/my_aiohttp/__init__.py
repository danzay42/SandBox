import logging
from typing import Callable, Awaitable

from aiohttp import web

logger = logging.getLogger(__package__)


@web.middleware
async def middleware(request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]) -> web.Response:
    logger.debug(f"{await request.text()}")
    response = await handler(request)
    logger.debug(f"{response.body}")
    return response


async def handler_func(request: web.Request) -> web.Response:
    return web.Response(text="hello world")


def config_logger():
    logging.basicConfig(level=logging.DEBUG)


def main():
    config_logger()
    app = web.Application(logger=logger, middlewares=[middleware])
    app.add_routes([web.route('*', '/{tail:.*}', handler_func)])
    web.run_app(app)
