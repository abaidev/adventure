from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from adventure.models import Transaction, TransactionFile
from .serializers import TransactionListSerializer, TransRUDSerializer, TransCreateSerializer
from rest_framework import status
from rest_framework.response import Response

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

