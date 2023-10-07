from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from .models import Product, Sale, Loss
from .serializers import ProductSerializer, SalesSerializer, LossSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.generics import DestroyAPIView, ListCreateAPIView, ListAPIView
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from accounts.models import GameZoneUser
# Create your views here.


class ProductViewset(ViewSet):

    
    queryset=Product.objects.all()
    permission_classes=[IsAuthenticatedOrReadOnly]
    # CREATE PRODUCT
    def create_product(self, request, *args, **kwargs):
        data = request.data
        
        # Convert 'price' and 'quantity' to integers
        data['price'] = int(data['price'])
        data['quantity'] = int(data['quantity'])
        print(data)

        serializer = ProductSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response({"error": "Data passed is invalid"})

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
    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs):
        # Use the nocache method
        products=Product.objects.filter(sold_out=False).all()
        print(self.queryset)
        serializer = ProductSerializer(self.queryset, many=True)
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
    @method_decorator(never_cache)
    def remove(self, request, *args, **kwargs):
        try:
            product = get_object_or_404(Product, id=kwargs.get("id"))
            product.delete()
            return Response({"message": "Product deleted successfully"})
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=404)
        except Exception as e:
            return Response({"message": str(e)}, status=500)



class ProductCreateView(ListCreateAPIView):

 
    queryset=Product.objects.all()
    print(queryset)
    serializer_class=ProductSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]


class ProductDeleteView(DestroyAPIView):
   
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field="pk"
    permission_classes=[IsAuthenticatedOrReadOnly]

class UpdateViewSet(ViewSet):


    queryset=Sale.objects.all()

    def update_product(self, request):
        data_passed=request.data
        print(data_passed)
        product=get_object_or_404(Product, id=data_passed['id'])
        print(product)

        if product:
            if product.quantity > data_passed["quantity_sold"] or product.quantity == data_passed["quantity_sold"]:
    
                sale = Sale(
                    product=product,
                    quantity_sold=data_passed["quantity_sold"],
                    sale_price=data_passed["sale_price"]
                )
                
                sale.save()
                sale.product.quantity =sale.product.quantity - int(data_passed["quantity_sold"])
                if int(sale.product.quantity) == 0:
                    sale.product.sold_out=True
                
                return Response({"MESSAGE": "OK"})
            return Response({"error": "quantity error, reduce quantity"})
        return Response({"error":"product does not exist"})
                


class SalesViewSet(ListCreateAPIView):

 
    queryset=Sale.objects.all()
    permission_classes=[IsAuthenticatedOrReadOnly]
    serializer_class=SalesSerializer


    def create(self, request, *args, **kwargs):
        # Get the data from the request
        quantity_sold = request.data.get("quantity_sold")
        sale_price = request.data.get("sale_price")
        product_id = request.data.get("id")
        print(product_id, sale_price, quantity_sold)

        try:
            # Retrieve the product by its ID
            product = Product.objects.get(id=product_id)
            print(product.quantity)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"})

        if quantity_sold <= 0:
            print("less")
            return Response({"detail": "Quantity sold must be greater than zero"})

        if quantity_sold > product.quantity:
            print("greater")
            return Response({"detail": "Quantity sold cannot exceed available quantity"})

        # Create a new sale
        sale = Sale(
            product=product,
            quantity_sold=quantity_sold,
            sale_price=sale_price,
        )
        sale.save()

        # Update the product's quantity
        product.quantity -= quantity_sold
        if product.quantity <= 0:
            product.sold_out=True
        product.save()



        serializer = SalesSerializer(sale)
        return Response(serializer.data)

print(Sale.objects.all())



class ListSales(ViewSet):


 
    queryset=Sale.objects.all()
    def retriev(self, request):
        serializer=SalesSerializer(self.queryset, many=True)
        return Response(serializer.data)


class LossViewSet(ViewSet):
    pass

    queryset=Loss.objects.all()

    def ListLoss(self, request):
        serializer=LossSerializer(self.queryset, many=True)
        return Response(serializer.data)

   

    def CreateLoss(self, request):
        data=request.data
        name = data["loss_name"]
        amount = int(data["loss_amount"])  # Convert to integer
        description = data["loss_description"]
        product_associated = data["loss_to_product"]

        product = Product.objects.filter(name=product_associated).first()
        print(data)
        if product is not None:
            loss=Loss.objects.create(loss_name=name, loss_amount=amount, loss_description=description, loss_to_product=product)
            loss.save()
            return Response({"ok": "ok"})
        else:
            loss=Loss(loss_name=name, loss_amount=amount, loss_description=description)
            loss.save()
            return Response({"ok": "ok"})