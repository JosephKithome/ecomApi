from django.db.models import fields
from rest_framework import serializers
from .models import Product, ProductCategory, ProductImage,OrderItem,Order
from django.contrib.auth import get_user_model

#Serializes the ImageModel
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "alt_text"]



class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value

#Serializes  Product 
class ProductSerializer(serializers.ModelSerializer):

    # attaches a product to the image serializer and sets readOnly to true,
    # this way we can return a product with its attached data
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
            'regular_price'
        ]

# serializes category to return name and slug 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("name", "slug")

class AddToCartSerializer(serializers.ModelSerializer):    
    class Meta:
        model = OrderItem
        fields = "__all__"  


class OrderItemSerializer(serializers.ModelSerializer):  
    item = StringSerializer()
    item_obj = serializers.SerializerMethodField()
    final_item_total = serializers.SerializerMethodField()
  
    class Meta:
        model = OrderItem 
        fields = (
            'id',
            'product',
            'quantity',
            'item_obj',
            'final_item_total',

        )  
    #Grabs item from product model and returns it if its in the order    
    def get_item_obj(self,obj):
        return ProductSerializer(obj.item.all(),many=True).data    

    # calls the item total i.e 1 * X  method specified in the Models 
    # and returns it as a field in the order serializer    
    def get_total(self,obj):
        return obj.get_final_item_total()   

   
class OrderSerializer(serializers.ModelSerializer):  
    order_items = serializers.SerializerMethodField()
    cart_total = serializers.SerializerMethodField()
  
    class Meta:
        model = Order 
        fields =(
            'id',
            'order_items',
            'cart_total'
        )  
    # calls the orderItem Serializer returns the items present in the order    
    def get_order_items(self,obj):
        return OrderItemSerializer(obj.items.all(),many=True).data
    # calls the cart total method in the Models and returns a serialized field in the OrderSeralizer    
    def get_cart_total(self,obj):
        return obj.get_cart_total()    


