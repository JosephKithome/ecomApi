from django.urls import path
from .views import ProductList,ProductDetail
from  rest_framework.routers import SimpleRouter

#using normal urls
urlpatterns =[
    path('api/v1/product/',ProductList.as_view()),
    path('api/v1/product/<int:pk>/',ProductDetail.as_view()),
]