from django.db import models
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_description = models.CharField(max_length=255)
    product_quantity = models.IntegerField()
    product_image = models.ImageField(upload_to="media")
    
    class Meta:
        db_table = 'Products'
