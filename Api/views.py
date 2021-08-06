from django.shortcuts import render
from rest_framework import generics
from .models import Product, ProductCategory
from . import models
from .permissions import IsAuthorOrReadOnly

from .serializers import ProductSerializer, CategorySerializer

from rest_framework import viewsets

# Create your views here.
class ProductList(generics.ListAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Product.objects.all()
    lookup_field = "slug"
    serializer_class = ProductSerializer


class CategoryItemView(generics.ListAPIView):
    serializer_class = ProductSerializer

    """""
    get product in that specified category by filtering with a slug that is category
    name in lower case.

    Note we use category__slug to transverse from category slug and match it with the provided slug 
    for filtering """

    def get_queryset(self):
        return models.Product.objects.filter(product_category__slug=self.kwargs["slug"])


# LISTAPIView allows a read only
class CategoryListView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer
