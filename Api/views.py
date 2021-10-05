from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.urls.conf import include
from rest_framework import generics
from .models import Product, ProductCategory
from . import models
from .permissions import IsAuthorOrReadOnly
from django.http import JsonResponse,response
from django.shortcuts import get_object_or_404
from .models import Order,OrderItem

from .serializers import OrderSerializer, ProductSerializer, CategorySerializer
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
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
    queryset = ProductCategory.objects.filter(level=2)
    serializer_class = CategorySerializer



class AddtoOrderItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args,**kwargs):
        slug = request.data.get('slug',None)

        if slug is None:
            return Response({'message':'invalid request'},status=HTTP_400_BAD_REQUEST)

        item = get_object_or_404(Product, slug=slug)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=self.request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=self.request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]

            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                return Response({"message": "item was added to cart",
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


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes=(permissions.IsAuthenticated)


    def get_object(self):
         try:
             order =Order.objects.get(user=self.request.user,ordered=False)
             return order

         except ObjectDoesNotExist:
             return Response({'message':'You do not have an active order'})    