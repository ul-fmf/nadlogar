from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "t2-r&t0yj0b%q$b^@ptqya=13mq0rsz1_5&h^ub-=+(ueiqsql"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
