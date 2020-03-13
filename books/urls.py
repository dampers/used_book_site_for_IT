from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
    path("create/", views.CreateBookView.as_view(), name="create"),
    path("<int:pk>", views.BookDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditBookView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.BookPhotosView.as_view(), name="photos"),
    path(
        "<int:book_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:book_pk>/photos/<int:photo_pk>/edit/",
        views.EditPhotoView.as_view(),
        name="edit-photo",
    ),
    path("<int:book_pk>/delete/", views.delete_book, name="delete-book"),
    path("<int:pk>/photos/add", views.AddPhotoView.as_view(), name="add-photo"),
    path("search/", views.SearchView.as_view(), name="search"),
]
