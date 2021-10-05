from typing import DefaultDict
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from Auth.models import CustomUser

# Create your models here.


class ProductCategory(MPTTModel):
    """
    Products category implemented using  mptt.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_("Category safe URL"), max_length=255, unique=True
    )

    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")
    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])    

    def __str__(self) -> str:
        return self.name


class ProductType(models.Model):
    """ "
    Table aimed at providing a list of the
    different types of products available forsale
    """

    name = models.CharField(
        verbose_name=_("Product Name"), help_text="Required", max_length=255
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self) -> str:
        return self.name


class ProductSpecification(models.Model):
    """
    The product specification holds the
     product specification or the features for the product.
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(
        verbose_name=_("Specification Name"), help_text=_("Required"), max_length=255
    )

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """
    This table holds all the product items
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name=_("Product Title"),
        help_text=_("Required"),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_("Product Description"), help_text=_("Not Required"), blank=True
    )

    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_("Regular Price"),
        help_text=_("Maximum 9999999.99"),
        error_messages={
            "name": {
                "max_length_error": _("The price must be between 0 and 9999999.99"),
            },
        },
        max_digits=7,
        decimal_places=2,
    )

    # To create its table later
    discount_price = models.DecimalField(
        verbose_name=_("Discount Price"),
        help_text=_("Maximum 9999999.99"),
        error_messages={
            "name": {
                "max_length_error": _("The price must be between 0 and 9999999.99"),
            },
        },
        max_digits=7,
        decimal_places=2,
    )

    is_active = models.BooleanField(
        verbose_name=_("Product Visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )
    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, editable=False
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self) -> str:
        return self.title


class ProductSpecificationValue(models.Model):
    """
    This table holds the specification value of each of the products individual
    specification or bespoke features.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("Value"),
        help_text=_("Product specification value (maximum of 255 characters)"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Value")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    """
    Table that holds product images

    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image"
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        help_text=_("Upload product image"),
        upload_to="media/",
        default="media/default.jpg",
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative text"),
        help_text=_("Please add alternative text!"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


# class OrderItem(models.Model) :
#     user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True, blank=True)
#     ordered = models.BooleanField(default=False)
#     item = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
#     quantity = models.IntegerField(default=1)


#     def __str__(self):
#         return f"{self.quantity} of {self.item.title}"

# class Order(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
#     items = models.ManyToManyField(OrderItem,blank=True, null=True)
#     start_date = models.DateTimeField(auto_now_add=True)
#     ordered_date = models.DateTimeField()
#     ordered = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.email


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping    


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_final_item_total(self):
        total = self.product.regular_price * self.quantity
        return total
    @property
    def get_total_discount_item_price(self):
        return self.product.discount_price  
    @property
    def get_amount_saved(self):
        return self.get_total()-self.get_total_discount_item_price()    


class ShippingAddress(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.address)