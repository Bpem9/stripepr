from rest_framework import routers
from django.urls import path, include
from .views import *


urlpatterns = [
    path('item/', ItemListView.as_view(), name='items'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item'),
    path('buy/<int:pk>/', create_checkout_session, name='buy'),
    path('order/', OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('intent/<int:pk>/', CreatePaymentIntent.as_view(), name='intent'),
    path('success_payment', success_payment, name='success_payment'),
    path('cancel_payment', cancel_payment, name='cancel_payment'),
    path('create_products', create_product, name='create_products'),

]
