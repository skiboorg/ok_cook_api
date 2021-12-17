from django.urls import path,include
from . import views

urlpatterns = [
    path('complects', views.GetComplects.as_view()),
    path('complect', views.GetComplect.as_view()),
    path('category', views.GetCategory.as_view()),






]
