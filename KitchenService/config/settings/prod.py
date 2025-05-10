from .base import *

#DEBUG = os.environ.get("DJANGO_DEBUG", "") != "False"
# SECURITY WARNING: don't run with debug turned on in production!

#ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DEBUG = False
# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
   ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': int(os.environ['POSTGRES_DB_PORT']),
    }
}
