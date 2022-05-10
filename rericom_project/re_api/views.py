from django.shortcuts import render

class TokenCreateView(generics.CreateAPIView):
    serializer_class = TokenSerializer
