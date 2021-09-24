from aiohttp.web import middleware

from api.auth import authenticate_request


@middleware
async def jwt_auth_middleware(request, handler):
    """
    Middleware for jwt authentication.
    
    Middleware set user as request['user'] and token as request['token']
    """
    authenticated_request = await authenticate_request(request)
    return await handler(authenticated_request)
    