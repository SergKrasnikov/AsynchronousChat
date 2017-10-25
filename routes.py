from core.views import Redirect
from auth.views import Login, SignIn, SignOut, Admin, Room
from chat.views import ChatList, WebSocket


routes = [
    ('GET',        '/',          Redirect,   'redirect'),
    ('GET',        '/chat/',     ChatList,   'main'),
    ('GET',        '/ws/',       WebSocket,  'chat'),
    ('*',          '/admin/',    Admin,      'admin'),
    ('*',          '/rooms/',    Room,       'rooms'),
    ('*',          '/login/',    Login,      'login'),
    ('*',          '/signin/',   SignIn,     'signin'),
    ('*',          '/signout/',  SignOut,    'signout'),
]
