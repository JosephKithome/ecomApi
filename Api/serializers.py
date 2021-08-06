from django.db.models import fields
from rest_framework import serializers
from .models import Product, ProductCategory, ProductImage
from django.contrib.auth import get_user_model


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "alt_text"]


class ProductSerializer(serializers.ModelSerializer):
    product_image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "product_category",
            "slug",
            "description",
            "product_image",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("name", "slug")
