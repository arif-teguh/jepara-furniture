
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.land_page),
    path('login', views.login_user),
    path('register', views.register_user),
    path('chair/add',views.addNewChair),
    path('logout',views.logout_user),
]
