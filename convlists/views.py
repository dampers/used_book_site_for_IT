from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from users import models as user_models
from conversations import models as conversations_models
from . import models


def save_conversation(request, a_pk, b_pk):
    try:
        user_one = user_models.User.objects.get(pk=a_pk)
    except user_models.DoesNotExist:
        user_one = None
    try:
        user_two = user_models.User.objects.get(pk=b_pk)
    except user_models.DoesNotExist:
        user_two = None
    if user_one is not None and user_two is not None and user_one != user_two:
        the_list1, created = models.Convlist.objects.get_or_create(
            user=user_one, name=user_one
        )
        the_list2, created = models.Convlist.objects.get_or_create(
            user=user_two, name=user_two
        )
        convq = conversations_models.Conversation.objects.filter(
            participants=user_one
        ).filter(participants=user_two)
        if convq.exists():
            return redirect(reverse("conversations:detail", kwargs={"pk": convq[0].pk}))
        else:
            conversation = conversations_models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)
            the_list1.conversations.add(conversation)
            the_list2.conversations.add(conversation)
            return redirect(
                reverse("conversations:detail", kwargs={"pk": conversation.pk})
            )


class SeeConvView(TemplateView):

    template_name = "conversations/conv_list.html"
