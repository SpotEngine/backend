from django.urls import include, path
from utils.enums import BaseUrl

# from .backoffice.urls import backoffice_urlpatterns
from .trader.urls import trader_urlpatterns

# include each section urls to the urlpatterns list
urlpatterns = [
    path(BaseUrl.TRADER, include(trader_urlpatterns)),
]
