from aiohttp.web import middleware

from api.auth import authenticate


@middleware
async def jwt_auth_middleware(request, handler):
    """
    Middleware for jwt authentication.
    
    Middleware set user as request['user'] and token as request['token']
    """
    user, token = await authenticate(request)
    request['user'] = user
    request['token'] = token
    return await handler(request)