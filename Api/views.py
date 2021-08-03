from django.shortcuts import render
from rest_framework import generics
from .models import Product
from .permissions import IsAuthorOrReadOnly

from .serializers import ProductSerializer

from rest_framework import viewsets

# Create your views here.
class ProductList(generics.ListAPIView):
    permission_classes =(IsAuthorOrReadOnly,)
    queryset=Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.ListAPIView):
    permission_classes =(IsAuthorOrReadOnly,)
    queryset=Product.objects.all()
    serializer_class = ProductSerializer
