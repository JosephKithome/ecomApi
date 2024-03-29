from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from mptt.admin import MPTTModelAdmin

# Register your models here.
from .models import (
    Product,
    ProductCategory,
    ProductSpecification,
    ProductType,
    ProductImage,
    ProductSpecificationValue,
    OrderItem,
    Order
)

admin.site.register(ProductCategory, MPTTModelAdmin)


#Sticking product specification to Product
class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ProductSpecificationInline] 


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationInlineValue(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInlineValue,
        ProductImageInline,
    ]

admin.site.register(OrderItem)   
admin.site.register(Order) 
