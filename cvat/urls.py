from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cvat.apps.engine.urls")),
    path("api/server/health/", include("health_check.urls")),
    path("api/test/", include("cvat.apps.test.urls")),
]
