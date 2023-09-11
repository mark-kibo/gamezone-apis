from django.db import models
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, default=None)
    description = models.CharField(max_length=255, null=True)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to="media", null=True, blank=True)
    
    class Meta:
        db_table = 'Products'
