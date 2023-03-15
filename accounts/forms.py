from django.contrib.auth.forms import UserChangeForm, UserCreationForm 
from .models import CustomUserModel

class CustomUserCreationForm(UserCreationForm):
  class Mete:
    model  = CustomUserModel
    fields = UserCreationForm.Meta.fields

class CustomUserChangeForm(UserChangeForm):
  class Mete:
    model  = CustomUserModel
    fields = "__all__"