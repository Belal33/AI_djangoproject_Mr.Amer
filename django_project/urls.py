from django.contrib import admin
from django.urls import path ,include
from .views import HomePage,chat_view

urlpatterns = [
    path("admin-my-one/", admin.site.urls),
    path("",chat_view, name="home"),
    path("accounts/", include("accounts.urls")),
]
