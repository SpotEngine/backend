from .conf import ENVIRONMENT

if not ENVIRONMENT == "production":
    raise Exception(f"Environment: {ENVIRONMENT} not set to production")

SECRET_KEY = 'ymskzcb1p!atwb%g1r+&ilk_un41h-v(t#%#6b4+(nmz9%hi1e'
DEBUG = False
ALLOWED_HOSTS = []

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
