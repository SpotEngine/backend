from rest_framework.routers import DefaultRouter
from .apis import (
    ContractViewSet,
)

router = DefaultRouter()
router.register('contract', ContractViewSet, basename='contract')

market_urlpatterns = router.urls