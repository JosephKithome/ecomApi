import json
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import UsersSerializer

from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

# Create your views here.


class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UsersSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UsersSerializer


def get_csrf(request):
    response = JsonResponse({"info": "Success - Set CSRF cookie"})
    response["X-CSRFToken"] = get_token(request)
    return response


def loginView(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if username is None or password is None:
            return JsonResponse({"info": "Username and password is needed"})
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({"info": "User does not exist"}, status=400)
        login(request, user)
        return JsonResponse({"info": "User logged in successfully"})


class WhoAMIView(APIView):
    authentication_classes=[SessionAuthentication]
    permission_classes=[IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        print(request.user.username)
        return JsonResponse({"Username",request.user.username})