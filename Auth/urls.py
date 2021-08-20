from django.urls import path
from rest_framework import views
from .views import UserList, UserDetail
from . import views

# using normal urls
urlpatterns = [
    # users endpoints
    path("", UserList.as_view(), name="user"),
    path("<int:pk>/", UserDetail.as_view(), name="users/id"),
    path("csrftoken/", views.get_csrf, name="api_csrf"),
    path("login/", views.loginView, name="login"),
]
