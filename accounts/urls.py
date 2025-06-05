from rest_framework.routers import DefaultRouter

from .views import MessageViewset

router = DefaultRouter()

router.register(r"message", MessageViewset, basename="message")
urlpatterns = router.urls + []
