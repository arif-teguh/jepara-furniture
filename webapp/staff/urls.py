
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.land_page),
    path('login', views.login_staff),
    path('furniture/add',views.addNewFurniture),
    path('logout',views.logout_staff),
]
