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
from .services import calcRefBonuses
from yoomoney import Quickpay







class CreateOrder(APIView):
    def post(self,request):

        data = request.data
        # print(data)
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
            receiver=settings.YA_WALLET,
            quickpay_form="shop",
            label=code,
            targets=f'Оплата заказа №{new_order.id}',
            paymentType="SB",
            successURL=settings.successURL + code,
            sum=new_order.menu_type.price,
        )
        print(quickpay.base_url)
        print(quickpay.redirected_url)

        # msg_html = render_to_string('new_order.html', {
        #     'order': new_order,
        # })
        # title = 'Новый заказ'
        #
        # send_mail(title, None, settings.SMTP_FROM, [settings.ADMIN_EMAIL, 'dimon.skiborg@gmail.com'],
        #           fail_silently=False, html_message=msg_html)

        return Response({'url':quickpay.redirected_url}, status=200)


class GetOrders(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class PaymentNotify(APIView):
    def post(self, request):

        code = request.data.get('label')
        codepro = request.data.get('codepro')
        unaccepted = request.data.get('unaccepted')
        if not unaccepted or codepro:
            order = Order.objects.get(code=code)
            if not order.is_pay:
                order.is_pay = True
                order.save(update_fields=['is_pay'])
                order.user.total_spend += order.menu_type.price
                order.user.save(update_fields=['total_spend'])
                calcRefBonuses(order.user,order.menu_type.price)
                msg_html = render_to_string('new_order.html', {
                    'order': order,
                })
                title = 'Новый заказ'

                send_mail(title, None, settings.SMTP_FROM, [settings.ADMIN_EMAIL,'dimon.skiborg@gmail.com'],
                          fail_silently=False, html_message=msg_html)
        return Response('ОК', status=200)
