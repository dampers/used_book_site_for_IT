from django import forms
from . import models


class SearchForm(forms.Form):

    title = forms.CharField(initial="book title")
    price = forms.IntegerField(required=False)
    deal_complete = forms.BooleanField(required=False)


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("file",)

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        book = models.Book.objects.get(pk=pk)
        photo.book = book
        photo.save()


class CreateBookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = (
            "title",
            "price",
            "description",
            "condition",
        )

    def save(self, *args, **kwargs):
        book = super().save(commit=False)
        return book
