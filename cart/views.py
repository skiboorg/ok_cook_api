from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *


def calcCartPrice(cart):
    complects = cart.complects.all()
    price = 0
    items_count = 0
    for complect in complects:
        price += complect.price * complect.amount
        complect_items_count = 0
        for item in complect.items.all():
            complect_items_count += item.amount
        items_count += complect_items_count * complect.amount
    cart.price = price
    cart.items_count = items_count
    cart.save()
    return

def get_cart(request,session_id):
    # print(request.user.is_authenticated)

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            print('found user cart')
        except Cart.DoesNotExist:
            print('not found user cart')
            cart = Cart.objects.filter(session_id=session_id).first()
            if cart:
                cart.user = request.user
                cart.save(update_fields=['user'])
                print('set current cart for user')
            else:
                cart = Cart.objects.create(user=request.user)
                print('create new cart for user')
    else:
        cart, created = Cart.objects.get_or_create(session_id=session_id)
        print(session_id)
        if created:
            print('guest cart created')
    return cart


class GetCart(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        return get_cart(self.request, self.request.query_params.get('session_id'))


class RemoveComplect(APIView):
    def post(self, request):
        data = request.data
        cart = get_cart(self.request, data.get('session_id'))
        complect = CartComplect.objects.get(id=data.get('id'))
        complect.delete()
        calcCartPrice(cart)

        return Response(status=200)


class EraseCart(APIView):
    def post(self, request):
        data = request.data
        cart = get_cart(self.request, data.get('session_id'))
        cart.items.all().delete()
        return Response(status=200)

class AddToCart(APIView):
    def post(self,request):
        data = request.data
        cart = get_cart(self.request, data.get('session_id'))
        # print(cart)
        # print(data)
        items = data.get('complect_items')
        cart_complect, created = CartComplect.objects.get_or_create(uid=data.get('complect_uid'),
                                                                    cart=cart,
                                                                    complect_id=data.get('complect_id')
                                                                    )

        if created:
            # print(items)
            price = 0
            for item in items:
                item = CartComplectItem.objects.create(item_id=item['id'],cart_complect=cart_complect,amount=item['items_added'])
                price += item.price
                cart_complect.price = price
                cart_complect.save()

        else:
            cart_complect.amount += 1
            cart_complect.save()
        calcCartPrice(cart)

        return Response(status=200)