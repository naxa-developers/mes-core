import os
print('local')
os.environ["DJANGO_SECRET_KEY"] = "dl25chokhr!)n*_yy(ezcoqef2755=h&gq4&^5n_fb^&-86fqf"
os.environ["KOBOCAT_MONGO_HOST"] = "localhost"
os.environ["CSRF_COOKIE_DOMAIN"] = "localhost"
os.environ["ENKETO_URL"] = 'http://localhost:8005'
os.environ["ENKETO_VERSION"] = 'express'
from onadata.settings.kc_environ import *
# os.environ['S3_USE_SIGV4'] = 'True'
KOBOCAT_URL = os.environ.get('KOBOCAT_URL', 'http://localhost:8001')

KOBOCAT_INTERNAL_HOSTNAME = "localhost"
# ENKETO_PROTOCOL = os.environ.get('ENKETO_PROTOCOL', 'https')
# ENKETO_PROTOCOL = os.environ.get('ENKETO_PROTOCOL', 'http')
ENKETO_PROTOCOL = 'http'
ENKETO_API_ENDPOINT_SURVEYS = '/survey'

ENKETO_URL = os.environ.get('ENKETO_URL', 'http://localhost:8005')
XML_VERSION_MAX_ITER = 6


os.environ["ENKETO_API_TOKEN"] = 'enketorules'


# TESTING_MODE = True
# ANGULAR_URL = '/ng/'
# ANGULAR_ROOT = os.path.join(BASE_DIR, 'ng/')

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

KOBOCAT_URL = 'http://localhost:8001'
CORS_ORIGIN_ALLOW_ALL = True
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'onadata1',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


KPI_URL = 'http://localhost:8000'
KPI_LOGOUT_URL = KPI_URL + 'accounts/logout/'


CORS_ORIGIN_WHITELIST = (
    'dev.ona.io',
    'google.com',
    'localhost:8001',
    '127.0.0.1:8000'
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'X-OpenRosa-Version',
)

TIME_ZONE = 'Asia/Kathmandu'

from onadata.settings.common import REST_FRAMEWORK
REST_FRAMEWORK.update({'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated',]})


# DEBUG_TOOLBAR_CONFIG = {
#     'INTERCEPT_REDIRECTS': True
# }


# DEBUG = False

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dl25chokhr!)n*_yy(ezcoqef2755=h&gq4&^5n_fb^&-86fqf')
SESSION_COOKIE_NAME = 'mes_cookie'
# SESSION_COOKIE_DOMAIN = '192.168.1.17'
SESSION_COOKIE_DOMAIN = 'localhost'
DEFAULT_DEPLOYMENT_BACKEND = 'localhost'

FRONTEND_ENVIRONMENT_DEV_MODE = True




