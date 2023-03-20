from django.contrib import admin
from django.urls import path ,include

urlpatterns = [
    path("", include("chatai.urls")),
    path("accounts/", include("accounts.urls")),
    path("admin-my-one/", admin.site.urls),
]

