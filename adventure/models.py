from django.db import models
from django.contrib.postgres.fields import ArrayField


class TransactionFile(models.Model):    # для того чтобы сохранять файл только в одном instance
    file = models.FileField(upload_to='transactions')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID: {self.id}. FILE_NAME: {self.file.name}. DATE: {self.date}"


class Transaction(models.Model):
    customer = models.CharField(max_length=250)
    item = models.CharField(max_length=500)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    date = models.DateTimeField()
    tfile = models.ForeignKey(TransactionFile, on_delete=models.CASCADE)
    def __str__(self):
        return f"USER: {self.customer}. ITEM: {self.item}. DATE: f{self.date}. FILE_NAME: {self.tfile.file.name}"

    def save(self,  *args, **kwargs):
        self.total_price = round(float(self.total_price), 0)
        super(Transaction, self).save( *args, **kwargs)

'''
по идее лучше всего чтобы модель Transaction брала ForeignKey от модели Customer
'''
class Customer(models.Model):
    username = models.CharField(max_length=250)
    spent_money = models.FloatField(default=0)
    gems = ArrayField(models.CharField(max_length=500), blank=True, null=True)

    def __str__(self):
        return f"{self.username}. MONEY: {str(self.spent_money)}. GEMS: {len(self.gems)}"