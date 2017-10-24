from time import time
import json


def set_session(session, **kwargs):
    value = kwargs.popitem()
    session[value[0]] = str(value[1])
    session['session_last_update'] = time()


def convert_json(message):
    return json.dumps({'error': message})
