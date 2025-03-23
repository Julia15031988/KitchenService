from .base import *

#DEBUG = os.environ.get("DJANGO_DEBUG", "") != "False"
# SECURITY WARNING: don't run with debug turned on in production!

#ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DEBUG = True
# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = []
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}