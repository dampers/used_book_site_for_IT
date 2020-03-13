from django.urls import path
from . import views

app_name = "conversations"

urlpatterns = [
    path("<int:pk>/", views.ConversationDetailView.as_view(), name="detail"),
]
