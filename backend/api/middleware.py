from aiohttp.web import middleware

from api.auth import check_authentication


@middleware
async def jwt_auth_middleware(request, handler):
    """
    Middleware for jwt authentication.
    
    Middleware set user as request['user'] and token as request['token']
    """
    authenticated_request = await check_authentication(request)
    return await handler(authenticated_request)
    