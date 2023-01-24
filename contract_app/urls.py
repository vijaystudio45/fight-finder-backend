from contract_app.views import (
    ContractViewSet,
    PersonViewSet,
    CompanyViewSet,
    ProductViewSet,
    BillingViewSet
    )
from rest_framework import routers



router = routers.SimpleRouter()
router.register(r'contract', ContractViewSet)
router.register(r'person', PersonViewSet)
router.register(r'company', CompanyViewSet)
router.register(r'product', ProductViewSet)
router.register(r'billing', BillingViewSet)


urlpatterns = [
    
]
urlpatterns += router.urls 