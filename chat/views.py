import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web, WSMsgType as MsgType
from auth.models import UserMySQL
from chat.models import RoomMySQL, MessageMySQL
from settings import log

from core.utils import redirect


class Rooms(web.View):
    @aiohttp_jinja2.template('chat/rooms.html')
    async def get(self):
        message = RoomMySQL()
        session = await get_session(self.request)
        if session.get('user') and session.get('room_id'):
            pass
        else:
            redirect(self.request, 'login')


class ChatList(web.View):
    @aiohttp_jinja2.template('chat/index.html')
    async def get(self):
        session = await get_session(self.request)

        if session.get('user') and session.get('room_id'):

            message = MessageMySQL(data={'user_id': session['user'], 'room_id': session['room_id'], })
            return {'messages': await message.get_messages(room_id=int(session.get('room_id')))}

        else:
            redirect(self.request, 'login')


class WebSocket(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        session = await get_session(self.request)
        user = UserMySQL(data={'id': session.get('user')})
        user = await user.get_user_by_id()

        for _ws in self.request.app['websockets']:
            _ws.send_str('%s joined' % user.login)
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.tp == MsgType.text:
                if msg.data == 'close':
                    await ws.close()
                else:
                    message = MessageMySQL(data={'user_id': session['user'], 'room_id': session['room_id'], })
                    message = await message.insert_message_to_db(msg=msg.data)
                    log.debug('result:%s' % message)
                    for _ws in self.request.app['websockets']:
                        _ws.send_str('(%s) %s' % (user.login, msg.data))
            elif msg.tp == MsgType.error:
                log.debug('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        for _ws in self.request.app['websockets']:
            _ws.send_str('%s disconected' % user.login)
        log.debug('websocket connection closed')

        return ws
