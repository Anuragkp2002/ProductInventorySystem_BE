import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField


# class User(AbstractUser):
#     email = models.EmailField(unique=True)

#     def __str__(self):
#         return self.username


class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    ProductID = models.BigIntegerField(unique=True)    
    ProductCode = models.CharField(max_length=255, unique=True)
    ProductName = models.CharField(max_length=255)    
    ProductImage = VersatileImageField(upload_to="uploads/", blank=True, null=True)    
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(blank=True, null=True)
    CreatedUser = models.ForeignKey(User, related_name="user%(class)s_objects", on_delete=models.CASCADE)    
    IsFavourite = models.BooleanField(default=False)
    Active = models.BooleanField(default=True)    
    HSNCode = models.CharField(max_length=255, blank=True, null=True)    
    TotalStock = models.DecimalField(default=0.00, max_digits=20, decimal_places=8, blank=True, null=True)
    
    class Meta:
        db_table = "products_product"
        verbose_name = ("product")
        verbose_name_plural = ("products")
        unique_together = (("ProductCode", "ProductID"),)
        ordering = ("-CreatedDate", "ProductID")

class ProductsVariation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Product = models.ForeignKey(Products, related_name="variations", on_delete=models.CASCADE)
    DisplayName = models.CharField(max_length=255)
    ProductCode = models.CharField(max_length=255)
    ProductImage = VersatileImageField(upload_to="uploads/variations/", blank=True, null=True)
    TotalStock = models.DecimalField(default=0.00, max_digits=20, decimal_places=8)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(blank=True, null=True)
    IsDeleted = models.BooleanField(default=False)
    IsActive = models.BooleanField(default=True)

    class Meta:
        db_table = "products_variation"
        ordering = ("-CreatedDate",)

class Attributes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    AttributeName = models.CharField(max_length=255)

    class Meta:
        db_table = "products_attribute"

class AttributeValues(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Attribute = models.ForeignKey(Attributes, related_name="values", on_delete=models.CASCADE)
    AttributeValue = models.CharField(max_length=255)

    class Meta:
        db_table = "products_attribute_value"

class VariationAttributes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Variation = models.ForeignKey(ProductsVariation, related_name="attributes", on_delete=models.CASCADE)
    AttributeValue = models.ForeignKey(AttributeValues, related_name="variations", on_delete=models.CASCADE)

    class Meta:
        db_table = "products_variation_attribute"

