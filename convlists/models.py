from django.db import models
from core import models as core_models


class Convlist(core_models.TimeStampedModel):

    """ Convlist Model Definition """

    name = models.CharField(max_length=80)
    user = models.OneToOneField(
        "users.User", related_name="convlist", on_delete=models.CASCADE
    )
    conversations = models.ManyToManyField(
        "conversations.Conversation", related_name="convlist", blank=True
    )

    def __str__(self):
        user = self.user
        return user.first_name

    def get_conv(self):
        usernames = []
        for conv in self.conversations.all():
            usernames.append(f"({conv})")
        return usernames
