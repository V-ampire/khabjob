from aiohttp import web
from aiopg.sa import create_engine

from api.routes import setup_routes

from core.db.utils import get_postgres_dsn

from typing import Dict


async def setup_db(app: web.Application):
    """Setup datatbase for application."""
    engine = await create_engine(get_postgres_dsn())

    app['db'] = engine

    try:
        yield
    finally:
        app['db'].close()
        await app['db'].wait_closed()


async def init_app(config: Dict={}) -> web.Application:
    """Initializae apllication."""
    app = web.Application()

    setup_routes(app)

    app.cleanup_ctx.append(setup_db)

    return app


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = init_app({})
    web.run_app(app)