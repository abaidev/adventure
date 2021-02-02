import csv
from io import TextIOWrapper
from datetime import datetime
from django.utils import timezone
ctz = timezone.get_current_timezone()
from rest_framework import serializers

from adventure.models import TransactionFile, Transaction

class TransactionListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='adventure-api:rud', lookup_field='pk')
    class Meta:
        model = Transaction
        fields = "__all__"
        depth = 1

class TransRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

class TransCreateSerializer(serializers.Serializer):
    tfile = serializers.FileField(label="CSV file")

    def create(self, data):
        file = TransactionFile.objects.create(file=data['tfile'])
        enc_file = TextIOWrapper(file.file.file, encoding='utf-8')
        read_dict = csv.DictReader(enc_file)
        for row in read_dict:
            print(row['item'], row['customer'], row['quantity'])
            Transaction.objects.create(
                customer = row['customer'],
                item = row['item'],
                quantity = row['quantity'],
                total_price = row['total'],
                date = ctz.localize(datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S.%f')), # чтобы не выдавало предупреждение Datetime naive
                tfile=file,
            )
        return data