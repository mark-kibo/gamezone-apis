from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Expense
from .serializers import ExpenseSerializer
# Create your views here.



class ExpenseViewset(ViewSet):
    queryset=Expense.objects.all()


    def create_expense(self, request):
        data=request.data
        data["amount"] = int(data["amount"])

        serializer=ExpenseSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response({
            "error":"data passed  is invalid"}
        )
    

    def List_expenses(self, request):

        serializer=ExpenseSerializer(self.queryset, many=True)
        return Response(serializer.data)