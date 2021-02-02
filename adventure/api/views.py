from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from adventure.models import Transaction, Customer
from .serializers import (TransactionListSerializer,
                          TransRUDSerializer,
                          TransCreateSerializer,
                          CustomerSerializer,)

class TransactionListAPIView(ListAPIView):
    serializer_class = TransactionListSerializer
    queryset = Transaction.objects.all()


class TransactionRUDAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransRUDSerializer
    queryset = Transaction.objects.all()


class TransactionCreateAPIView(CreateAPIView):
    serializer_class = TransCreateSerializer
    queryset = Transaction.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = TransCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"upload success": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomersTopListAPIView(ListAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all().order_by('-spent_money')[:5]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({"response": serializer.data}, status=status.HTTP_200_OK)
