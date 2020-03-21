from django import template
from django.http import  HttpResponse
from lists import models as list_models
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render


register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, book):
    user = context.request.user
    try:
        the_list = list_models.List.objects.get(user=user, name="My Favourites")
    except list_models.List.DoesNotExist:
        the_list = None
        return None
    return book in the_list.books.all()
