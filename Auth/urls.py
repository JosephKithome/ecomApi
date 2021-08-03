from django.urls import path
from .views import UserList,UserDetail

#using normal urls
urlpatterns =[
    #users endpoints
    path('api/v1/users/',UserList.as_view()),
    path('api/v1/users/<int:pk>/',UserDetail.as_view()),
]