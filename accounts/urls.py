from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import CustomRegister,CustomLoginVeiw 
# from .views import CustomLoginVeiw , register_user 


urlpatterns = [
  path("register/",CustomRegister.as_view(),name="sinup"),
  path("login/",CustomLoginVeiw.as_view(),name="login"),
  path('user-logout/',LogoutView.as_view(next_page = 'home'), name= 'logout' ),
]