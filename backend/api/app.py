"""
Aiohttp application initialization handler.
"""
from aiohttp import web, PAYLOAD_REGISTRY

import aiohttp_cors

from aiopg.sa import create_engine

from api.middleware import jwt_auth_middleware
from api.routes import setup_routes
from api.payloads import JsonPayload

from typing import Dict, Mapping, Optional
from types import MappingProxyType

from core.db.utils import get_postgres_dsn

from config import CORS_CONFIG


async def setup_db(app: web.Application):
    """Setup datatbase for application."""
    engine = await create_engine(get_postgres_dsn())

    app['db'] = engine

    try:
        yield
    finally:
        app['db'].close()
        await app['db'].wait_closed()

    
def setup_cors(app: web.Application):
    """Set up CORS policy."""
    defaults = {
        origin: aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_methods='*',
            allow_headers='*',
        ) for origin in CORS_CONFIG['CORS_ALLOWED_ORIGINS']
    }
    
    cors = aiohttp_cors.setup(app, defaults=defaults)

    for route in list(app.router.routes()):
        cors.add(route)


def init_app(config: Optional[Dict] = None) -> web.Application:
    """Initialize apllication."""
    middlewares = [
        jwt_auth_middleware,
    ]

    app = web.Application(middlewares=middlewares)

    setup_routes(app)
    setup_cors(app)

    app.cleanup_ctx.append(setup_db)

    # Serializing json in http response.
    PAYLOAD_REGISTRY.register(JsonPayload, (Mapping, MappingProxyType))

    return app
