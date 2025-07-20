from rest_framework.routers import DefaultRouter

from clients.views import *

router = DefaultRouter()

router.register(r"testimonials", TestimonalViewset, basename="testimonials")
router.register(r"services", ServiceViewset, basename="services")

urlpatterns = router.urls + []
