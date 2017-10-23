from aiohttp import web
from aiohttp_session import get_session

from core.utils import redirect
from auth.models import UserMySQL


class Redirect(web.View):

    async def get(self, *args, **kwargs):
        session = await get_session(self.request)
        if session.get('user'):
            user = UserMySQL(data={'id': session['user'], }, )
            user = await user.get_user_by_id()
            if user.is_admin:
                redirect(self.request, 'admin')
            else:
                redirect(self.request, 'rooms')
        else:
            redirect(self.request, 'login')
