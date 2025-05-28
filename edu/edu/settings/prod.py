from decouple import config

from .base import *
#from cfg import DB_USER1

#DEBUG = config('DEBUG', default=False, cast=bool)
DEBUG = False

ADMINS = (
('David O', 'email@mydomain.com'),
)

ALLOWED_HOSTS = ['eduproject.com', 'www.eduproject.com']
#ALLOWED_HOSTS = ['127.0.0.1']
#ALLOWED_HOSTS = ['ip-address', 'www.your-website.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'), 
        'PASSWORD': config('POSTGRES_PASSWORD'), 
        'HOST': 'db',
        'PORT': 5432,
    }
}

CACHES = {
    'default': {
    	'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',  #PyMemcacheCache
        'LOCATION': 'memcached:11211',
        # 'TIMEOUT': 360
    }
}


"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'), 
        'PASSWORD': config('DB_PASSWORD'), 
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
"""

#STRIPE_PUBLIC_KEY = config('STRIPE_LIVE_PUBLIC_KEY')
#STRIPE_SECRET_KEY = config('STRIPE_LIVE_SECRET_KEY')

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

