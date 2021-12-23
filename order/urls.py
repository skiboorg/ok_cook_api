from django.urls import path,include
from . import views

urlpatterns = [
    path('create', views.CreateOrder.as_view()),
    path('get', views.GetOrders.as_view()),
    path('pay_notify', views.PaymentNotify.as_view()),
    path('all', views.GetAllOrders.as_view()),
    path('order_done', views.OrderDone.as_view()),

]
