from django.urls import path,include
from . import views

urlpatterns = [


    path('me/', views.GetUser.as_view()),
    path('update', views.UserUpdate.as_view()),
    path('recover_password', views.UserRecoverPassword.as_view()),
    path('rr', views.Test.as_view()),
    path('get_referals', views.GetReferals.as_view()),




]
