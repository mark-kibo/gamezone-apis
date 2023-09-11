from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.


class ProductViewset(ViewSet):
    queryset=Product.objects.all()
    permission_classes=[IsAuthenticatedOrReadOnly]
    # CREATE PRODUCT
    def create_product(self, request, *args, **kwargs):
        data = request.data
        serializer=ProductSerializer(data=data)
        # chack if data passed is valid and return a product response
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response({
            "error":"data passed is invalid"
        })
    
      # edit PRODUCT
    def edit_product(self, request, *args, **kwargs):
        product=get_object_or_404(Product, id=kwargs.get("id"))
        data = request.data
        if product is not None:
            serializer=ProductSerializer(instance=product,
                                         data=data)
            # chack if data passed is valid and return a product response
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response({
                "error":"data passed is invalid"
            })
        return Response({
            "error":"product does not exist"
        })
    



    # LIST PRODUCTS

    def list(self, request, *args, **kwargs):
        serializer=ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)
    

    # Retrieve product
    def retrieve(self, request, *args, **kwargs):
        product=get_object_or_404(Product, id=kwargs.get("id"))
        if product is not None:
            serializer=ProductSerializer(product)
            return Response(serializer.data)
        return Response({
            "error":"Products are not available"
        })
    
    # destroy product
    def remove(self, request, *args, **kwargs):
        product=get_object_or_404(Product, id=kwargs.get("id"))
        if product is not None:
            product.delete()
            return Response({
                "message":f"product {product.name} successfully deleted"
            })
        
        return Response({
            "error":"product does not exist"
        })
    

