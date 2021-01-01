from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    re_path(r"^i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("searches/", include("searchindexesapp.urls")),
    path("enterprises/", include("enterprisesapp.urls")),
)
