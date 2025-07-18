from django.urls import path
from rest_framework.routers import DefaultRouter

from projects.views import *

router = DefaultRouter()
router.register(r"projects", ProjectsViewset, basename="projects")

urlpatterns = router.urls
