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
from cart.views import calcCartPrice


class OrderDone(APIView):
    def post(self, request):
        order = Order.objects.get(id=request.data.get('id'))
        order.is_done=True
        order.save()
        return Response(status=200)
class CreateOrder(APIView):
    def post(self,request):
        data = request.data
        #print(data)
        cart = Cart.objects.get(user=self.request.user)
        delivery_price = 0 if cart.items_count >= 25 else 1000
        complects  = cart.complects.all()

        code = create_random_string(digits=False, num=2).upper() + '-' + create_random_string(digits=True, num=6)

        new_order = Order.objects.create(user=request.user,
                                         code=code,
                                         address=data['order_data']['delivery_address'],
                                         delivery_time=data['order_data']['delivery_time'],
                                         city=data['order_data']['city'],
                                         phone=data['order_data']['phone'],
                                         company_name=data['order_data']['company_name'],
                                         company_address=data['order_data']['company_address'],
                                         company_inn=data['order_data']['company_inn'],
                                         company_kpp=data['order_data']['company_kpp'],
                                         company_contact=data['order_data']['company_contact'],
                                         comment=data['order_data']['comment'],
                                         )
        price = 0
        for complect in complects:
            price += complect.price * complect.amount
            for item in complect.items.all():
                order_item, created = OrderItem.objects.get_or_create(item_id=item.item.id,order=new_order)
                if created:
                    order_item.amount = item.amount
                else:
                    order_item.amount += item.amount
                order_item.save()
        #print(price)
        new_order.price = price
        new_order.delivery_price = delivery_price
        new_order.save()
        complects.delete()
        calcCartPrice(cart)
        quickpay = Quickpay(
            receiver=settings.YA_WALLET,
            quickpay_form="shop",
            label=code,
            targets=f'Оплата заказа №{new_order.id}',
            paymentType="SB",
            successURL=settings.successURL + code,
            sum=price + delivery_price,
        )
        #
        #
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


class GetAllOrders(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.query_params.get('is_done') == 'done':
            orders = Order.objects.filter(is_pay=True, is_done=True).order_by('-created_at')
        else:
            orders = Order.objects.filter(is_pay=True, is_done=False).order_by('-created_at')
        return orders


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
