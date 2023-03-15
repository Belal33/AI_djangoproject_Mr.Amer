from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm,CustomUserChangeForm
from .models import CustomUserModel
# Register your models here.

class CustomUserAdmin(UserAdmin):
  model= CustomUserModel
  add_form = CustomUserCreationForm
  add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
  form = CustomUserChangeForm
  fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name","age", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
  list_display = ("username","age", "email", "first_name", "last_name", "is_staff")

admin.site.register(CustomUserModel,CustomUserAdmin)