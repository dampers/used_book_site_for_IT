from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"


class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):

    """ Book Admin Definition """

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "title",
                    "description",
                    "price",
                    "deal_complete",
                    "seller",
                    "condition",
                )
            },
        ),
    )

    list_display = (
        "title",
        "seller",
        "price",
        "deal_complete",
        "condition",
        "count_photos",
        "created",
    )

    raw_id_fields = ("seller",)

    ordering = ("title", "price")

    list_filter = (
        "deal_complete",
        "condition",
    )

    search_fields = ("title",)

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"
