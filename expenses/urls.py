from django.urls import path
from . import views




urlpatterns=[
    path('', views.ExpenseViewset.as_view({"get": "List_expenses", "post":"create_expense"}))
]