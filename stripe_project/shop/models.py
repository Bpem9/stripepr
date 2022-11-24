from django.db import models
from django.db.models import Sum, F


class Order(models.Model):
    items = models.ManyToManyField('Item', verbose_name='Товары')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def list_items(self):
        return ', '.join([item.name for item in self.items.all()])

    def total_price(self):
        return self.items.aggregate(Sum('price'))['price__sum']

class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name}: {self.price}'
