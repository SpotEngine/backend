from rest_framework.routers import DefaultRouter
from .apis import (
    OrderViewSet,
    TradeViewSet,
    SymbolViewSet
)

router = DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register('symbol', SymbolViewSet, basename='symbol')
router.register('trade', TradeViewSet, basename='trade')

trader_urlpatterns = router.urls