from django.shortcuts import render
from django.urls.conf import include
from rest_framework import generics
from .models import Product, ProductCategory
from . import models
from .permissions import IsAuthorOrReadOnly
from django.http import JsonResponse,response
from django.shortcuts import get_object_or_404
from .models import Order,OrderItem

from .serializers import ProductSerializer, CategorySerializer

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from django.utils import timezone
from rest_framework import status
from datetime import datetime
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
        return models.Product.objects.filter(product_category__in=ProductCategory.objects.get(slug=self.kwargs["slug"]).get_descendants(include_self=True))


# LISTAPIView allows a read only
class CategoryListView(generics.ListAPIView):
    queryset = ProductCategory.objects.filter(level=1)
    serializer_class = CategorySerializer



class AddtoOrderItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        item = get_object_or_404(Product, pk=pk)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=self.request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=self.request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]

            if order.items.filter(item__pk=item.pk).exists():
                order_item.quantity += 1
                order_item.save()
                return Response({"message": "Quantity is added",
                                 },
                                status=status.HTTP_200_OK
                                )
            else:
                order.items.add(order_item)
                return Response({"message": " Item added to your cart", },
                                status=status.HTTP_200_OK,
                                )
        else:
            ordered_date = datetime.now()
            order = Order.objects.create(user=self.request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            return Response({"message": "Order is created & Item added to your cart", },
                            status=status.HTTP_200_OK,
                            )
