from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.http import JsonResponse

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


swagger_urls = [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

api_urlpatterns = [
   # path('perp/', include('perpetual.urls')),
   path('auth/', include('aaa.urls')),
   path('spot/', include('spot.urls')),
   path('wallet/', include('wallet.urls')),
]

app_urls = [
   path('admin/', admin.site.urls),
   path('api/v1/', include(api_urlpatterns)),
   path('health-check/', lambda request: JsonResponse({'status': 'ok'})),
]

urlpatterns = app_urls

if settings.ENVIRONMENT in ['develop', 'local']:
   urlpatterns += swagger_urls