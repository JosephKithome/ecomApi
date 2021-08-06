from django.urls import path
from .views import UserList, UserDetail

# using normal urls
urlpatterns = [
    # users endpoints
    path("", UserList.as_view()),
    path("<int:pk>/", UserDetail.as_view()),
]
