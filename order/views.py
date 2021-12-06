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



class CreateOrder(APIView):
    def post(self,request):

        data = request.data
        print(data)
        comment = data['order_data']['comment']
        cart = Cart.objects.get(user=self.request.user)


        new_order = Order.objects.create(user=request.user,
                                         code=create_random_string(digits=True,num=6),
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

        return Response({'code':new_order.code},status=200)


class GetOrders(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class PaymentNotify(APIView):
    def post(self, request):
        print(request.data)
        data = request.data
        payment_success = data['Success']
        if payment_success:
            order_id = data['OrderId']
            print(order_id)
            order = Order.objects.get(id=order_id)
            order.is_pay = True
            order.save()

            msg_html = render_to_string('order.html', {'order': order})

            send_mail('Ваш заказ', None, settings.SMTP_FROM, [order.user.email,settings.ADMIN_EMAIL],
                      fail_silently=False, html_message=msg_html)

        return Response('ОК', status=200)
