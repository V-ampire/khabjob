from aiohttp import web


class Vacancies(web.View):
    """View for vacancies resource."""

    async def get(self):
        """Get publiched vacancies list."""
        return web.json_response({'status': 'ok'})