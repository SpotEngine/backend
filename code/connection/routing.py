from django.urls import re_path

from .consumers import SpotAccountConsumer, SpotMarketConsumer

websocket_urlpatterns = [
    re_path(r"ws/spot/account/$", SpotAccountConsumer.as_asgi()),
    re_path(r"ws/spot/market/$", SpotMarketConsumer.as_asgi()),
    # re_path(r"ws/spot/(?P<room_name>\w+)/$", SpotConsumer.as_asgi()),
]