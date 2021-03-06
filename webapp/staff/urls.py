
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.land_page),
    path('login', views.login_staff),
    path('logout',views.logout_staff),
    path('chat',views.chat_list),
    path('chat/<int:user_id>',views.reply_chat),
    path('chat/<int:user_id>/reload',views.reply_chat_reload),
    path('complain',views.complain_list),
    path('preorder',views.preorder_list),
    path('complain/delete/<int:complain_id>',views.delete_complain),
    path('preorder/delete/<int:preorder_id>',views.delete_preorder),
    path('preorder/accept/<int:preorder_id>',views.accept_preorder),
]