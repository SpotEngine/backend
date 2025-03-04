from .conf import ENVIRONMENT

if not ENVIRONMENT == "develop":
    raise Exception(f"Environment: {ENVIRONMENT} not set to develop")

SECRET_KEY = 'l#^abq@w55q$28j!%llvpw5q+v305n6qqmz_#lv$!#jf0(7nid'
DEBUG = True
ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = ['http://*', 'https://*']
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    '*',
]
