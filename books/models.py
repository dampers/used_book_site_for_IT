from django.db import models
from django.urls import reverse
from core import models as core_models
from users import models as user_models


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="book_photos")
    book = models.ForeignKey("Book", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


class Book(core_models.TimeStampedModel):

    """ Book Model Definition """

    CONDITION_A = "A"
    CONDITION_B = "B"
    CONDITION_C = "C"
    CONDITION_CHOICES = (
        (CONDITION_A, "A"),
        (CONDITION_B, "B"),
        (CONDITION_C, "C"),
    )

    title = models.CharField(max_length=140)
    description = models.TextField()
    price = models.IntegerField()
    deal_complete = models.BooleanField(default=False)
    seller = models.ForeignKey(
        user_models.User, related_name="books", on_delete=models.CASCADE
    )
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=2, default="B")

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #   super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("books:detail", kwargs={"pk": self.pk})

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos
