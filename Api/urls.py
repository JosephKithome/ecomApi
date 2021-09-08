from django.urls import path
from .views import CategoryListView, ProductList, ProductDetail, CategoryItemView,AddtoOrderItemView
from rest_framework.routers import SimpleRouter

app_name = "store"

# using normal urls
urlpatterns = [
    path("", ProductList.as_view(), name="home"),
    path("<slug:slug>/", ProductDetail.as_view(), name="product"),
    # returns all the categories
    path("category", CategoryListView.as_view(), name="categories"),
    # Returns products in a particular category(filtered by slug which is category name)
    path("category/<slug:slug>/", CategoryItemView.as_view(), name="category_items"),
    path('cart/',AddtoOrderItemView.as_view(),name='orderItems')
]
