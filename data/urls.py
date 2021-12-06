from django.urls import path,include
from . import views

urlpatterns = [
    path('menu_type', views.GetMenuType.as_view()),
    path('category', views.GetCategory.as_view()),






]
