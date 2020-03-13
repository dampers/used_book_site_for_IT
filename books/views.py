from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView, FormView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from users import mixins as user_mixins
from . import models, forms

PER_PAGE = 1


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Book
    paginate_by = 8
    paginate_orphans = 0
    ordering = "-created"
    context_object_name = "books"


class BookDetail(DetailView):

    """ BookDeatail Definition """

    model = models.Book


class SearchView(View):

    """Search Definition"""

    form_class = forms.SearchForm

    def get(self, request):
        title = request.GET.get("title", "")

        if title != "":
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                price = form.cleaned_data.get("price")
                deal_complete = form.cleaned_data.get("deal_complete")

                filter_args = {}

                if price is not None:
                    filter_args["price__lte"] = price
                if deal_complete is True:
                    filter_args["deal_complete"] = True
                qs = models.Book.objects.filter(title__icontains=title).order_by(
                    "-updated"
                )
                paginator = Paginator(qs, 8, orphans=0)
                page = request.GET.get("page", 1)
                try:
                    books = paginator.page(page)
                except PageNotAnInteger:
                    books = paginator.page(PER_PAGE)
                except EmptyPage:
                    books = paginator.page(paginator.num_pages)
                return render(
                    request,
                    "books/search.html",
                    {"form": form, "books": books, "title": title},
                )
        else:
            form = forms.SearchForm()
        print(form)
        return render(request, "books/search.html", {"form": form})


class EditBookView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Book
    template_name = "books/book_edit.html"
    fields = (
        "title",
        "price",
        "description",
        "condition",
        "deal_complete",
    )

    def get_object(self, queryset=None):
        book = super().get_object(queryset=queryset)
        if book.seller.pk != self.request.user.pk:
            raise Http404()
        return book


class BookPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Book
    template_name = "books/book_photos.html"

    def get_object(self, queryset=None):
        book = super().get_object(queryset=queryset)
        if book.seller.pk != self.request.user.pk:
            raise Http404()
        return book


@login_required
def delete_photo(request, book_pk, photo_pk):
    user = request.user
    try:
        book = models.Book.objects.get(pk=book_pk)
        if book.seller.pk != user.pk:
            messages.error(request, "Cant delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
        return redirect(reverse("books:photos", kwargs={"pk": book_pk}))
    except models.Book.DoesNotExist:
        return redirect(reverse("core:home"))


@login_required
def delete_book(request, book_pk):
    user = request.user
    try:
        book = models.Book.objects.get(pk=book_pk)
        if book.seller.pk != user.pk:
            messages.error(request, "Cant delete that book")
        else:
            book.delete()
        return redirect(reverse("users:profile", kwargs={"pk": user.pk}))
    except models.Book.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "books/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Updated"
    fields = ("caption",)

    def get_success_url(self):
        book_pk = self.kwargs.get("book_pk")
        return reverse("books:photos", kwargs={"pk": book_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    model = models.Photo
    template_name = "books/photo_create.html"
    fields = ("caption", "file")
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(pk)
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("books:photos", kwargs={"pk": pk}))


class CreateBookView(user_mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateBookForm
    template_name = "books/book_create.html"

    def form_valid(self, form):
        book = form.save()
        book.seller = self.request.user
        book.save()
        form.save_m2m()
        messages.success(self.request, "Book Uploaded")
        return redirect(reverse("books:photos", kwargs={"pk": book.pk}))
