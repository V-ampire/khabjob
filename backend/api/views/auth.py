from aiohttp import web

from api.validation.utils import validate_request_data
from api.validation.auth import UserCredentials, ResetPasswordData
from api.views.mixins import DbViewMixin, AuthenticatedRequiredMixin
from api.auth import authenticate_user, make_jwt_token_for_user

from core.services.auth import blacklist_token, update_user


class LoginView(DbViewMixin, web.View):
    """View to obtain jwt token for user."""

    async def post(self):
        """
        Obtain token for access to private api.
        
        Return {'user': <username>, 'jwt_token': <token>}
        """
        credentials = await self.request.json()
        validated_data = validate_request_data(
            UserCredentials,
            credentials,
        )
        async with self.db.acquire() as conn:
            user = await authenticate_user(conn, **validated_data)
        
        token = make_jwt_token_for_user(user.id)

        return web.Response(body={'user': user.username, 'jwt_token': token})


class LogoutView(AuthenticatedRequiredMixin, DbViewMixin, web.View):
    """View to logout user via add jwt token to blacklist."""

    async def get(self):
        """Blacklist jwt token."""
        jwt_token = self.request['token']

        async with self.db.acquire() as conn:
            await blacklist_token(conn, jwt_token)

        return web.Response(body={'status': 'logout'})


class ResetPasswordView(DbViewMixin, web.View):
    """View to reset password."""
    
    async def post(self):
        """Reset password."""
        reset_data = await self.request.json()
        validated_data = validate_request_data(
            ResetPasswordData,
            reset_data,
        )

        async with self.db.acquire() as conn:
            user = await authenticate_user(
                conn,
                username=validated_data['username'],
                password=validated_data['old_password']
            )
            updated_user = await update_user(
                conn,
                user.id,
                password=validated_data['new_password1']
            )

        return web.Response(body=updated_user)


