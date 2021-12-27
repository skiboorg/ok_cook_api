import pydf
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
from django.utils.timezone import now


def generateCalcPdf(orders):
    items = []
    for order in orders:
        for item in order.order_items.all():
            if [element for element in items if element['item_name'] == item.item.name]:
                x = [element for element in items if element['item_name'] == item.item.name]
                index = next((i for i, xx in enumerate(items) if xx["item_name"] == item.item.name), None)
                items[index]['amount'] += item.amount

            else:
                items.append({'item_name':item.item.name,'amount':item.amount})

    html = render_to_string('calc.html',
                            {   'date':now().date(),
                                'items': items
                            })

    pdf = pydf.generate_pdf(html)
    filename = f'media/calc-{now().date()}-{now().time()}.pdf'
    with open(filename, mode= 'wb') as f:
        f.write(pdf)
    return filename


def generateSkladPdf(orders):
    html = render_to_string('order.html',
                            {
                                'orders': orders

                            })
    pdf = pydf.generate_pdf(html)
    filename = f'media/sklad-{now().date()}-{now().time()}.pdf'
    with open(filename, mode= 'wb') as f:
        f.write(pdf)
    return filename

def generateTransportPdf(orders):
    html = render_to_string('transport.html',
                            {
                                'orders': orders

                            })
    pdf = pydf.generate_pdf(html)
    filename = f'media/transport-{now().date()}-{now().time()}.pdf'
    with open(filename, mode= 'wb') as f:
        f.write(pdf)
    return filename

class OrderDone(APIView):
    def post(self, request):
        if request.data.get('action') == 'all':
            orders = Order.objects.filter(is_pay=True, is_done=False).order_by('sector')
            for order in orders:
                order.is_done = True
                order.save()
            calc_filename = generateCalcPdf(orders)
            sklad_filename = generateSkladPdf(orders)
            transport_filename = generateTransportPdf(orders)
            result = {'sklad_filename':sklad_filename,
                      'transport_filename':transport_filename,
                      'calc_filename':calc_filename,
                      }
        else:
            order = Order.objects.get(id=request.data.get('id'))
            order.is_done = True
            order.save()
            result = {}
        return Response(result,status=200)



class CreateOrder(APIView):
    def post(self,request):
        data = request.data
        city_id = data['order_data']['city']['id']
        sector_id = data['order_data']['sector']['id']

        cart = Cart.objects.get(user=self.request.user)
        delivery_price = 0 if cart.items_count >= 25 else 1000
        complects  = cart.complects.all()

        code = create_random_string(digits=False, num=2).upper() + '-' + create_random_string(digits=True, num=6)

        new_order = Order.objects.create(user=request.user,
                                         code=code,
                                         address=data['order_data']['delivery_address'],
                                         delivery_time=data['order_data']['delivery_time'],
                                         city_id=city_id,
                                         sector_id=sector_id,
                                         phone=data['order_data']['phone'],
                                         company_name=data['order_data']['company_name'],
                                         company_address=data['order_data']['company_address'],
                                         company_inn=data['order_data']['company_inn'],
                                         company_kpp=data['order_data']['company_kpp'],
                                         company_contact=data['order_data']['company_contact'],
                                         comment=data['order_data']['comment'],
                                         )
        price = 0
        items_count=0
        for complect in complects:
            price += complect.price * complect.amount
            for item in complect.items.all():
                order_item, created = OrderItem.objects.get_or_create(item_id=item.item.id,order=new_order)
                if created:
                    print('created')

                    order_item.amount = item.amount * complect.amount

                else:
                    print('early created')
                    order_item.amount += item.amount * complect.amount


                order_item.save()
        #print(price)

        for item in new_order.order_items.all():
            items_count += item.amount

        new_order.price = price
        new_order.total_items_count = items_count
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

                for item in order.order_items.all():
                    item.item.ostatok -= item.amount
                    item.item.save()

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


class GetCities(generics.ListAPIView):
    serializer_class = OrderCitySerializer
    queryset = OrderCity.objects.all()