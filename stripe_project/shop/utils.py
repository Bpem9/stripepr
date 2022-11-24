import os

import stripe
from django.shortcuts import render, redirect
from django.urls import reverse

from .serializers import *
from .models import *


stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

class StripeManager:
    HOST = os.getenv('HOST')
    items = Item.objects.all()

    @classmethod
    def create_products(cls):
        """Создание объектов товаров в платежной системе"""
        for item in cls.items:
            stripe.Product.create(
                name=item.name,
                description=item.description,
                default_price_data={
                    'unit_amount_decimal': str(item.price).replace('.', ''),
                    'currency': 'rub',
                }
            )
            print('Готово')

    @classmethod
    def create_checkout_session(cls, request, *args, **kwargs):
        """Создание платежной сессии конкретизированного товара"""
        item = Item.objects.get(pk=kwargs['pk'])
        product_data = {
                        'name': item.name,
                        'description': item.description
                        }
        try:
            cls.checkout_session = stripe.checkout.Session.create(
                line_items=[
                                {
                                    'price_data': {
                                        'currency': 'rub',
                                        'product_data': product_data,
                                        'unit_amount_decimal': str(item.price).replace('.', ''),
                                                    },
                                    'quantity': 1,
                                },
                            ],
                mode='payment',
                success_url=cls.HOST + reverse('success_payment'),
                cancel_url=cls.HOST + reverse('cancel_payment'),
            )
        except Exception as e:
            raise serializers.ValidationError(e)

    @classmethod
    def create_paymentintent(cls, request, *args, **kwargs):
        """Создание объекта PaymentIntent - стоимости заказа"""
        try:
            order = Order.objects.get(pk=kwargs['pk'])
            serializer = OrderDetailSerializer(order)
            intent = stripe.PaymentIntent.create(
                                                    amount=int(serializer.data['total_price']),
                                                    currency="eur",
                                                    automatic_payment_methods={"enabled": True},
                                                )
            print(f'Создан платеж на сумму: {intent.amount}{intent.currency}.')
        except Exception as e:
            return (e.__class__.__name__, e)



