from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("complements/", include("complements.urls")),
    path("app_users/", include("app_user.urls")),
]
