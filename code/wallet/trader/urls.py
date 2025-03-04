from rest_framework.routers import DefaultRouter
from .apis import (
    BlockchainWalletViewSet,
    AssetViewSet,
    TokenViewSet
)

router = DefaultRouter()
router.register('blockchain-wallet', BlockchainWalletViewSet, basename='blockchain-wallet')
router.register('asset', AssetViewSet, basename='asset')
router.register('token', TokenViewSet, basename='token')

trader_urlpatterns = router.urls