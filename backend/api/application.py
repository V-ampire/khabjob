from aiohttp.web import Application

from api.routes import setup_routes

from typing import Dict


async def init_app(config: Dict) -> Application:
    """Initializae apllication."""
    app = Application()

    setup_routes(app)

    return app