from aiohttp import web, PAYLOAD_REGISTRY

from aiopg.sa import create_engine

from api.middleware import jwt_auth_middleware
from api.routes import setup_routes
from api.payloads import JsonPayload

import logging
from typing import Dict, Mapping, Optional
from types import MappingProxyType

from core.db.utils import get_postgres_dsn


async def setup_db(app: web.Application):
    """Setup datatbase for application."""
    engine = await create_engine(get_postgres_dsn())

    app['db'] = engine

    try:
        yield
    finally:
        app['db'].close()
        await app['db'].wait_closed()


def init_app(config: Optional[Dict]=None) -> web.Application:
    """Initialize apllication."""
    app = web.Application(middlewares=[jwt_auth_middleware])

    setup_routes(app)

    app.cleanup_ctx.append(setup_db)

    # Serializing json in http response.
    PAYLOAD_REGISTRY.register(JsonPayload, (Mapping, MappingProxyType))

    return app


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = init_app()
    web.run_app(app)