from django.urls import path

from .views import ProductViewset, SalesViewSet, ProductCreateView, ListSales, UpdateViewSet, LossViewSet


urlpatterns=[
    # path("products/", ProductViewset.as_view({"get": "list", "post": "create_product"})),
    path("products/", ProductCreateView.as_view()),
    path("products/<int:id>/", ProductViewset.as_view({"patch": "edit_product", "delete":"remove", "get":"retrieve"})),
    path("sales/", UpdateViewSet.as_view({"post": "update_product"})),
    path("sales/List/",ListSales.as_view({"get": "retriev"})),
    path("loss/", LossViewSet.as_view({"get": "ListLoss", "post":"CreateLoss"})),
]