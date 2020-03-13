from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            "custom fields",
            {
                "fields": (
                    "student_number",
                    "avatar",
                    "IT_depart",
                    "oasis",
                    "email_verified",
                    "email_secret",
                    "login_method",
                )
            },
        ),
    )
    list_filter = ("IT_depart",) + UserAdmin.list_filter

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "IT_depart",
        "is_superuser",
        "email_verified",
        "login_method",
    )


# admin.site.register(models.User, CustomUserAdmin) == @admin.register(models.User)
