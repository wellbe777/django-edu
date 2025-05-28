from .base import *

DEBUG = True

#ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',   # use str() if it can't find database
        #"NAME": os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

CACHES = {
    'default': {
    	'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',  #PyMemcacheCache
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11212',
        # 'TIMEOUT': 360
    }
}

