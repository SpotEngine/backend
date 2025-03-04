from .conf import ENVIRONMENT

if not ENVIRONMENT == "local":
    raise Exception(f"Environment: {ENVIRONMENT} not set to local")

SECRET_KEY = 'vf6(ny22ty1fc!tcqp_u3l=@85wp$*)p_m-d4m+=mt%1kqsq@*'
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
