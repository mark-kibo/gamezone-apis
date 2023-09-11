from django.urls import path

from .views import ProductViewset


urlpatterns=[
    path("products/", ProductViewset.as_view({"get": "list", "post": "create_product"})),
    path("products/<int:id>/", ProductViewset.as_view({"patch": "edit_product", "delete":"remove", "get":"retrieve"})),
]