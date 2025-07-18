from rest_framework.routers import DefaultRouter

from .views import CompanyStatsViewset, MessageViewset, OrganizationViewset

router = DefaultRouter()

router.register(r"messages", MessageViewset, basename="messages")
router.register(r"company-stats", CompanyStatsViewset, basename="company-stats")
router.register(r"organization", OrganizationViewset, basename="organization")
urlpatterns = router.urls + []
