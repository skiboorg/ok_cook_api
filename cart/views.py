from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *


def get_cart(request,session_id):
    print(request.user.is_authenticated)

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
        #print(cart)
        #print(data)
        for item in data.get('cart'):
            CartItem.objects.create(cart=cart,item_id=item['id'],amount=item['items_added'])
            #print(item['id'])
            #print(item['items_added'])
        return Response(status=200)