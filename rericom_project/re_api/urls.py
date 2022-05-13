from re_api.views import MessageCreateView, MessageConfirmView
from django.urls import path

urlpatterns = [
    path('message/', MessageCreateView.as_view()),
    path('message_confirmation/', MessageConfirmView.as_view()),
               ]