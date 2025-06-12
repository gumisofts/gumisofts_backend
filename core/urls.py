from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("jobs/", include("jobs.urls")),
    path("clients/", include("clients.urls")),
    path("projects/", include("projects.urls")),
    path("", SpectacularSwaggerView.as_view(), name="swagger"),
    path("schema", SpectacularAPIView.as_view(), name="schema"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
