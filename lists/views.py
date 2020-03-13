from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from books import models as book_models
from . import models


def toggle_book(request, book_pk):
    action = request.GET.get("action", None)
    try:
        book = book_models.Book.objects.get(pk=book_pk)
    except book_models.Book.DoesNotExist:
        book = None

    if book is not None and action is not None:
        the_list, _ = models.List.objects.get_or_create(
            user=request.user, name=request.user.first_name
        )
        if action == "add":
            the_list.books.add(book)
        elif action == "remove":
            the_list.books.remove(book)
    return redirect(reverse("books:detail", kwargs={"pk": book_pk}))


class SeeFavsView(TemplateView):

    template_name = "lists/list_detail.html"
