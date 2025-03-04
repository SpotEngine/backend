from rest_framework.routers import DefaultRouter
from .apis import (
    SymbolViewSet,
)

router = DefaultRouter()
router.register('symbol', SymbolViewSet, basename='symbol')
# router.register('order-book', OrderBookViewSet, basename='order-book')
# router.register('trade', TradeViewSet, basename='trade')

market_urlpatterns = router.urls