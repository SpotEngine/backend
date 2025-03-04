from rest_framework.routers import DefaultRouter
from .apis import (
    OrderViewSet,
    PositionViewSet,
    TradeViewSet,
    SetupViewSet,
    ContractViewSet,
    PerpWalletViewSet
)

router = DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register('position', PositionViewSet, basename='position')
router.register('trade', TradeViewSet, basename='trade')
router.register('setup', SetupViewSet, basename='setup')
router.register('contract', ContractViewSet, basename='contract')
router.register('wallet', PerpWalletViewSet, basename='wallet')

trader_urlpatterns = router.urls