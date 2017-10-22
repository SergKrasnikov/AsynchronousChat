import aiohttp_jinja2
from aiohttp_session import get_session
from aiohttp import web, WSMsgType as MsgType
from auth.models import UserMySQL
from chat.models import RoomMySQL, Message, MessageMySQL
from settings import log


class Rooms(web.View):
    @aiohttp_jinja2.template('chat/rooms.html')
    async def get(self):
        message = RoomMySQL()
        messages = await message.get_messages()
        return {'messages': messages}


class ChatList(web.View):
    @aiohttp_jinja2.template('chat/index.html')
    async def get(self):
        # message = MessageMySQL()
        # messages = await message.get_messages() # 'messages': messages
        return {}


class WebSocket(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        session = await get_session(self.request)
        user = UserMySQL(self.request.db, {'id': session.get('user')})
        login = await user.get_login()

        for _ws in self.request.app['websockets']:
            _ws.send_str('%s joined' % login)
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.tp == MsgType.text:
                if msg.data == 'close':
                    await ws.close()
                else:
                    message = Message(self.request.db)
                    result = await message.save(user=login, msg=msg.data)
                    log.debug('result:%s' % result)
                    for _ws in self.request.app['websockets']:
                        _ws.send_str('(%s) %s' % (login, msg.data))
            elif msg.tp == MsgType.error:
                log.debug('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        for _ws in self.request.app['websockets']:
            _ws.send_str('%s disconected' % login)
        log.debug('websocket connection closed')

        return ws
