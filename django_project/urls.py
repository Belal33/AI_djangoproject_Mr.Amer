from django.contrib import admin
from django.urls import path ,include
from .views import HomePage

urlpatterns = [
    path("admin-my-one/", admin.site.urls),
    path("",HomePage.as_view(), name="home"),
    path("accounts/", include("accounts.urls")),
]
