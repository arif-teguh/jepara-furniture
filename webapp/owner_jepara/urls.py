
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    # path('', views.land_page),
    # path('login', views.login_staff),
    # path('chair/add',views.addNewChair),
    # path('logout',views.logout_staff),
    path('admin', views.admin_list),
    path('order',views.order_list),
]
