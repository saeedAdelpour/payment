from . import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

ALLOWED_HOSTS = []


SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool)
