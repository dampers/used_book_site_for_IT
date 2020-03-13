from django.db import models
from core import models as core_models


class List(core_models.TimeStampedModel):

    """ List Model Definition """

    name = models.CharField(max_length=80)
    user = models.OneToOneField(
        "users.User", related_name="list", on_delete=models.CASCADE
    )
    books = models.ManyToManyField("books.Book", related_name="lists", blank=True)

    def __str__(self):
        return self.name

    def count_books(self):
        return self.books.count()

    count_books.short_description = "Number of Books"
