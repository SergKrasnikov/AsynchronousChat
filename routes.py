from chat.views import Rooms, ChatList, WebSocket
from auth.views import Login, SignIn, SignOut, Admin


routes = [
    ('GET',        '/chat/',     ChatList,   'main'),
    ('GET',        '/ws/',       WebSocket,  'chat'),
    ('*',          '/admin/',    Admin,      'admin'),
    ('*',          '/rooms/',    Rooms,      'rooms'),
    ('*',          '/login/',    Login,      'login'),
    ('*',          '/signin/',   SignIn,     'signin'),
    ('*',          '/signout/',  SignOut,    'signout'),
]
