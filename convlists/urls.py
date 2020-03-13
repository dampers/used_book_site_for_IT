from django.urls import path
from . import views

app_name = "convlists"

urlpatterns = [
    path(
        "add/<int:a_pk>/<int:b_pk>/", views.save_conversation, name="save-conversation",
    ),
    path("convs/", views.SeeConvView.as_view(), name="see-convs"),
]
