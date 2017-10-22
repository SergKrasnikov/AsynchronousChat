import json
from time import time
from bson.objectid import ObjectId

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from auth.models import UserMySQL
from chat.models import RoomMySQL

from settings import log
from core.utils import redirect


def set_session(session, user_id, ):
    session['user'] = str(user_id)
    session['last_visit'] = time()


def convert_json(message):
    return json.dumps({'error': message})


class Login(web.View):

    @aiohttp_jinja2.template('auth/login.html')
    async def get(self, *args, **kwargs):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'main')
        return {'content': 'Please enter login or email'}

    async def post(self, *args, **kwargs):
        data = await self.request.post()

        user = UserMySQL(data)
        result = await user.check_user()

        dict_response = {'content_type': 'application/json',
                         'status': 200,
                         'charset': 'utf-8', }

        if isinstance(result, UserMySQL, ):
            session = await get_session(self.request, )
            set_session(session=session, user_id=result.id, )

            if result.is_admin:
                dict_response.update({'text': json.dumps({'result': 'Ok', 'redirect': '/admin/', }, ), }, )
            else:
                dict_response.update({'text': json.dumps({'result': 'Ok', 'redirect': '/rooms/', }, ), }, )

        else:
            dict_response.update({'text': convert_json(result, ), }, )

        return web.Response(**dict_response)


class SignIn(web.View):

    @aiohttp_jinja2.template('auth/sign.html')
    async def get(self, **kw):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'main')
        return {'content': 'Please enter your data'}

    async def post(self, **kw):
        data = await self.request.post()
        log.debug('SignIn: POST')
        log.debug(data)
        user = await UserMySQL(self.request.db, data, )
        log.debug(self.request.db)
        log.debug(user)
        result = await user.create_user()
        if isinstance(result, ObjectId):
            session = await get_session(self.request)
            set_session(session=session, user_id=result.id, )
        else:
            return web.Response(content_type='application/json', text=convert_json(result))


class SignOut(web.View):

    async def get(self, **kw):
        session = await get_session(self.request)
        if session.get('user'):
            del session['user']
            redirect(self.request, 'login')
        else:
            raise web.HTTPForbidden(body=b'Forbidden')


class Admin(web.View):

    @aiohttp_jinja2.template('auth/admin.html', )
    async def get(self, *args, **kwargs):
        log.debug('2222222222222222222')
        session = await get_session(self.request, )
        if session.get('user'):
            user = UserMySQL(data={'id': session['user'], }, )
            user = await user.get_user_by_id()
            return {'content': 'Please select room',
                    'user': user,
                    'rooms': RoomMySQL.select(), }
        else:
            log.debug('!!!!!!!!!!!!!!!!!!!!!')
            raise web.HTTPForbidden(body=b'Forbidden', )

    async def post(self, *args, **kwargs):
        log.debug('111111111111111111111111')
        data = await self.request.post()

        log.debug(data)

        room = RoomMySQL()
        name = data.get('name', False)
        log.debug(name)

        if name:
            room = await room.create_room(name=name)
            log.debug(room)

            # result = await user.check_user()

        # dict_response = {'content_type': 'application/json',
        #                  'status': 200,
        #                  'charset': 'utf-8', }
