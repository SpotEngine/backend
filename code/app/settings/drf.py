from datetime import timedelta


REST_REGISTRATION = {
    # https://django-rest-registration.readthedocs.io/en/latest/quickstart.html
    'USER_LOGIN_FIELDS': [],
    'USER_LOGIN_FIELDS_UNIQUE_CHECK_ENABLED': False,
    'REGISTER_VERIFICATION_ENABLED': False,
    'REGISTER_EMAIL_VERIFICATION_ENABLED': False,
    'RESET_PASSWORD_VERIFICATION_ENABLED': False,
    'REGISTER_VERIFICATION_AUTO_LOGIN': True,
    'REGISTER_SERIALIZER_CLASS': 'aaa.trader.serializers.UserRegister',
    # 'LOGIN_SERIALIZER_CLASS': 'aaa.user.serializers.UserLogin',
    # 'USER_PUBLIC_FIELDS': ['email', 'is_active'],

    # 'LOGIN_RETRIEVE_TOKEN': True,
    # 'AUTH_TOKEN_MANAGER_CLASS': 'aaa.user.logics.AuthTokenManager',

    'REGISTER_VERIFICATION_URL': 'https://frontend-host/verify-user/',
    'RESET_PASSWORD_VERIFICATION_URL': 'https://frontend-host/reset-password/',
    'REGISTER_EMAIL_VERIFICATION_URL': 'https://frontend-host/verify-email/',
    'VERIFICATION_FROM_EMAIL': 'no-reply@example.com',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,   
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

SIMPLE_JWT = {
    # "TOKEN_OBTAIN_SERIALIZER": "aaa.user.serializers.ObtainTokenSerializer",
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=10),
}