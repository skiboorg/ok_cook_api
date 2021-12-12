from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import *
from data.models import *
from user.models import *
from .serializers import *
import requests
import settings
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from user.services import create_random_string
from yoomoney import Quickpay







class CreateOrder(APIView):
    def post(self,request):

        data = request.data
        print(data)
        comment = data['order_data']['comment']
        cart = Cart.objects.get(user=self.request.user)
        code = create_random_string(digits=False, num=2) +\
               '-' + create_random_string(digits=True, num=6)

        new_order = Order.objects.create(user=request.user,
                                         code=code,
                                         menu_type_id=data.get('menu_type_id'),
                                         address=data['order_data']['delivery_address'],
                                         city=data['order_data']['city'],
                                         phone=data['order_data']['phone'],
                                         company_name=data['order_data']['company_name'],
                                         company_address=data['order_data']['company_address'],
                                         company_inn=data['order_data']['company_inn'],
                                         company_kpp=data['order_data']['company_kpp'],
                                         company_contact=data['order_data']['company_contact'],
                                         comment=data['order_data']['comment'],
                                         )
        for item in cart.items.all():
            OrderItem.objects.create(order=new_order,
                                     item=item.item,
                                     amount=item.amount)
            item.delete()

        # request.user.total_spend += new_order.menu_type.price
        # request.user.save(update_fields=['total_spend'])
        # calcRefBonuses(request.user,new_order.menu_type.price)

        quickpay = Quickpay(
            receiver="410019014512803",
            quickpay_form="shop",
            targets=f'Оплата заказа №{new_order.id}',
            paymentType="SB",
            sum=new_order.menu_type.price,
        )
        print(quickpay.base_url)
        print(quickpay.redirected_url)

        return Response({'url':quickpay.redirected_url}, status=200)


class GetOrders(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class PaymentNotify(APIView):
    def post(self, request):
        print(request.data)
        return Response('ОК', status=200)
