from os.path import isfile
from envparse import env
import logging


log = logging.getLogger('app')
log.setLevel(logging.DEBUG)

f = logging.Formatter('[F:%(pathname)-75s][L:%(lineno)-4d]# %(levelname)-8s [%(asctime)s]  %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(f)
log.addHandler(ch)

if isfile('.env'):
    env.read_envfile('.env')

DEBUG = env.bool('DEBUG', default=True)

SITE_HOST = env.str('HOST')
SITE_PORT = env.int('PORT')
SECRET_KEY = env.str('SECRET_KEY')
DB_HOST = env.str('DB_HOST')
DB_PORT = input(env.str('DB_PORT'))
DB_LOGIN = env.str('DB_LOGIN')
DB_PASSWD = env.str('DB_PASSWD')
DB_NAME = env.str('DB_NAME')

MESSAGE_COLLECTION = 'messages'
USER_COLLECTION = 'users'
