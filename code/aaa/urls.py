from django.urls import include, path
from utils.enums import BaseUrl

# from .backoffice.urls import backoffice_urlpatterns
from .trader.urls import user_urlpatterns

# include each section urls to the urlpatterns list
urlpatterns = [
    path(BaseUrl.TRADER, include(user_urlpatterns)),
]
