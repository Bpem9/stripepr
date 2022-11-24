from django.shortcuts import render, redirect
from rest_framework import generics, mixins, status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .utils import StripeManager


class ItemListView(generics.ListCreateAPIView):
    """Отображение списка товаров с возможностью создания"""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetailView(generics.RetrieveAPIView):
    """Детальное отображение товара с кнопкой оплаты на кастомном HTML-шаблоне"""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shop/item.html'


class OrderListView(generics.ListCreateAPIView):
    """Отображение списка заказов с возможностью создания"""
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    def list(self, request, *args, **kwargs):
        serializer = OrderListSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class OrderDetailView(generics.RetrieveAPIView):
    """Детальный просмотр заказа с кнопкой оплаты на кастомном HTML-шаблоне"""
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shop/order.html'


def create_checkout_session(request, *args, **kwargs):
    """Функция создания платежной сессии, выполняется при переходе по кнопке buy со страницы товара"""
    sm = StripeManager
    sm.create_checkout_session(request, *args, **kwargs)
    return redirect(sm.checkout_session.url, code=303)

def success_payment(request):
    """Рендер страницы успешного платежа"""
    return render(request, template_name='shop/success_payment.html')

def cancel_payment(request):
    """Рендер страницы отмененного платежа"""
    return render(request, template_name='shop/cancel_payment.html')

def create_product(request):
    """Создание товаров в базе данных stripe"""
    sm = StripeManager
    sm.create_products()
    return redirect('items')

class CreatePaymentIntent(APIView):
    """Создание денежного перевода, выполняется при переходе по кнопке buy со страницы заказа"""
    def get(self, request, *args, **kwargs):
        return Response({
                            'Это страница-заглушка для запуска платежной сессии. '
                            'Вот так вот просто переходить сюда через метод GET не надо'
                         })

    def post(self, request, *args, **kwargs):
        sm = StripeManager
        intent = sm.create_paymentintent(request, *args, **kwargs)
        if intent:
            return Response({f'Платежная сессия не создана, потому что: {intent[0]} : {intent[1]}'})
        else:
            return redirect('orders')

