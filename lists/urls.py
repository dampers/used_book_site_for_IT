from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("toggle/<int:book_pk>", views.toggle_book, name="toggle-book"),
    path("favs/", views.SeeFavsView.as_view(), name="see-favs"),
]
