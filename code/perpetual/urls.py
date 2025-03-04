from django.urls import include, path
from utils.enums import BaseUrl

from .trader.urls import trader_urlpatterns
from .market.urls import market_urlpatterns

urlpatterns = [
    path(BaseUrl.TRADER, include(trader_urlpatterns)),
    path(BaseUrl.MARKET, include(market_urlpatterns)),
]
