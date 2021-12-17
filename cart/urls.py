from django.urls import path,include
from . import views

urlpatterns = [
    path('add', views.AddToCart.as_view()),
    path('get', views.GetCart.as_view()),
    path('remove', views.RemoveComplect.as_view()),
    path('erase', views.EraseCart.as_view()),





]
