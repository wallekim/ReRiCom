from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from re_api.serializers import MessageSerializer, MessageStatusSerializer
from re_api.models import Messages
from re_api.authentication import PermissionCheck


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer


class MessageConfirmView(generics.CreateAPIView):
    serializer_class = MessageStatusSerializer
    permission_classes = [PermissionCheck]




