
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.land_page),
    path('login', views.login_user),
    path('register', views.register_user),
    path('logout',views.logout_user),
    path('accounts/login/*',views.login_user),
    path('view/furniture/<str:kategori>-<int:id>',views.view_furniture_details),
    path('view/furniture/<str:kategori>',views.view_furniture),
    path('review/furniture/<str:kategori>-<int:id>',views.review_furniture),
    path('checkout',views.checkout_all),
    path('checkout/<int:id_furniture>',views.checkout_fast),
    path('payment',views.payment),
    path('chat',views.chat),
    path('chat/reload',views.chat_reload),
    path('call',views.call),
    path('complain',views.complain),
    path('preorder',views.preorder),
    path('profile',views.profile),
    path('profile/edit',views.edit_profile),
]

