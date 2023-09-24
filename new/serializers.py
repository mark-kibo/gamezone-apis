from rest_framework import serializers
from .models import Product, Sale, Loss




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=[
            'id',
            'name',
            'category',
            'description',
            'price',
            'quantity'
        ]
    
class SalesSerializer(serializers.ModelSerializer):
    product_name=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Sale
        fields=[   
            'id',
            'product_name',
            "quantity_sold",
            "sale_price",
            'sale_date'
        ]



    def get_product_name(self, instance):
        return instance.product.name

        
class LossSerializer(serializers.ModelSerializer):
    class Meta:
        model=Loss
        fields="__all__"

