from django.contrib import admin
from .models import Transaction, TransactionFile, Customer

admin.site.register(Transaction)
admin.site.register(TransactionFile)
admin.site.register(Customer)