from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from django.urls import path
from . import views

urlpatterns = [

    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
 
]
