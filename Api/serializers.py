from django.db.models import fields
from rest_framework import serializers
from .models import Product
from django.contrib.auth import get_user_model

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model =Product
        fields = "__all__"

