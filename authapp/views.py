from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from new.models import Product, Sale, Loss
from accounts.models import GameZoneUser
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import datetime
# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer


class ProductAggregateAPIView(ViewSet):

    queryset=Product.objects.all()
    def get_overview(self, request, *args, **kwargs):
        # Calculate the aggregate (e.g., sum of all product prices)
        aggregate_result =self.queryset.aggregate(total_price=Sum('price'))
        total_users=GameZoneUser.objects.count()
        total_products=Product.objects.count()
        total_sales_revenue=Sale.objects.aggregate(total_price=Sum('sale_price'))
       
    #    get profit earned
        total_profit = Sale.objects.aggregate(total_profit=Sum('product__price'))['total_profit']
       
        top_products_by_quantity = Product.objects.annotate(total_quantity_sold=Sum('quantity')).order_by('total_quantity_sold')[:5]

        # //losses
        total_loss_incurred=Loss.objects.aggregate(total_loss=Sum('loss_amount'))['total_loss']
        if total_profit != None:
            total_profit = int(total_sales_revenue["total_price"])- int(total_loss_incurred)
# If you want to handle cases where there are no sales, you can provide a default value
        if total_profit is None:
            total_profit = 0


        return Response(
            {
                "total_loss": total_loss_incurred or 0,
                "total_revenue": total_sales_revenue["total_price"] or 0,
                "profit" : total_profit or 0,
            "aggregate_results": aggregate_result or 0,
             "totalusers":  total_users or 0,
             "total_products": total_products or 0
            }
        )
    permission_classes=[IsAuthenticatedOrReadOnly]