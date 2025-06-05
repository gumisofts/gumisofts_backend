from rest_framework.routers import DefaultRouter

from clients.views import *

router = DefaultRouter()

router.register(r"testimonals", TestimonalViewset, basename="testimonals")

urlpatterns = router.urls + []
