from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from new.models import Product
from accounts.models import GameZoneUser
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
        print(total_users, total_products)
        return Response(
            {
                "aggregate_results": aggregate_result,
             "totalusers":  total_users,
             "total_products": total_products}
        )
    permission_classes=[IsAuthenticatedOrReadOnly]