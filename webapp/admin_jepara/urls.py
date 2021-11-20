
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    # path('', views.land_page),
    # path('login', views.login_staff),
    # path('chair/add',views.addNewChair),
    # path('logout',views.logout_staff),
    path('staff/add',views.add_staff),
    path('staff',views.staff_list),
    path('user',views.user_list),
    path('furniture',views.furniture_list),
    path('chat/<int:user_id>',views.reply_chat),
    path('furniture/add',views.addNewFurniture),
    path('furniture/delete/<int:furtniture_id>',views.delete_furniture),
    path('',views.base),
]
