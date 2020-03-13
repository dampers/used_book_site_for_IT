from django.contrib import admin
from . import models


@admin.register(models.Convlist)
class ConvlistAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "get_conv",
    )

    search_fields = ("name",)
