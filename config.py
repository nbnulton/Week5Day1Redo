import os

class Config():
    REGISTERED_USERS = {
        'kevinb@codingtemple.com':{"name":"Kevin", "password":"abc123"}
    }

SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"