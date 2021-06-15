from .settings import *

DEBUG = True

INSTALLED_APPS += [
    "nplusone.ext.django",
]

MIDDLEWARE = [
    "nplusone.ext.django.NPlusOneMiddleware",
] + MIDDLEWARE

INTERNAL_IPS = ["127.0.0.1", "localhost"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME", "postgres"),
        'USER': os.environ.get("DB_USER", "postgres"),
        'PASSWORD': os.environ.get("DB_PASSWORD", "postgres"),
        # 'HOST': '127.0.0.1',
        'HOST': 'db',
        'PORT': '5432',
    }
}

NPLUSONE_LOGGER = logging.getLogger('nplusone')
NPLUSONE_LOG_LEVEL = logging.WARN