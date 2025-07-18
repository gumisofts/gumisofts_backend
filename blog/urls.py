from rest_framework.routers import DefaultRouter

from .views import (
    AuthorViewSet,
    BlogPostViewSet,
    CategoryViewSet,
    NewsletterSubscriberViewset,
    TagViewSet,
)

router = DefaultRouter()
router.register(r"newsletter", NewsletterSubscriberViewset, basename="newsletter")
router.register(r"posts", BlogPostViewSet, basename="blogpost")
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tags", TagViewSet, basename="tag")

urlpatterns = router.urls + []
