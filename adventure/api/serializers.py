import csv
from io import TextIOWrapper
from datetime import datetime
from django.utils import timezone
from rest_framework import serializers
from adventure.models import TransactionFile, Transaction, Customer

ctz = timezone.get_current_timezone()

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
            Transaction.objects.create(
                customer = row['customer'],
                item = row['item'],
                quantity = row['quantity'],
                total_price = row['total'],
                date = ctz.localize(datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S.%f')), # чтобы не выдавало предупреждение Datetime naive
                tfile=file,
            )

            qs = Customer.objects.filter(username=row['customer'])
            if qs.count() == 1:
                user = qs.first()
                user.spent_money += float(row['total'])
                user.gems.append(row['item']) if row['item'] not in user.gems else None
                '''
                todo:   т.к. камни покупаются несколько раз. Думаю лучше всего делать для них словарь, 
                        записывать сколько раз был куплен тот или иной камень
                '''
                user.save()
            else:
                Customer.objects.create(
                    username=row['customer'],
                    spent_money=float(row['total']),
                    gems=[row['item']])
        return data

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'