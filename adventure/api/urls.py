from django.urls import path
from .views import (TransactionListAPIView,
                    TransactionCreateAPIView,
                    TransactionRUDAPIView,
                    CustomersTopListAPIView, )

app_name = 'adventure-api'

urlpatterns = [
    path('list/', TransactionListAPIView.as_view(), name='list'),
    path('create/', TransactionCreateAPIView.as_view(), name='create'),
    path('detail/<int:pk>/', TransactionRUDAPIView.as_view(), name='rud'),
    path('top/', CustomersTopListAPIView.as_view(), name="top"),
]




