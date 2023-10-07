from django.db import models
import datetime

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=255, null=True)
    quantity = models.IntegerField(default=0)
    price=models.IntegerField(default=90)
    image = models.ImageField(upload_to="media", null=True, blank=True)
    sold_out=models.BooleanField(default=False)
    date_recorded=models.DateTimeField(auto_now_add=True)
    



class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale of {self.quantity_sold} {self.product.name}"

    def save(self, *args, **kwargs):
        # Update the product quantity when a sale is made
        self.product.quantity -= self.quantity_sold
        self.product.save()
        super().save(*args, **kwargs)


class Loss(models.Model):
    loss_name=models.CharField(max_length=255, default=None)
    loss_amount=models.IntegerField(default=0)
    loss_description = models.CharField(max_length=255, default=None)
    loss_to_product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, default=None)


    def __str__(self):
        return super().loss_mame