from django.contrib import admin
from .models import Transaction, TransactionFile

admin.site.register(Transaction)
admin.site.register(TransactionFile)