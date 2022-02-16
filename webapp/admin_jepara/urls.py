
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    # path('', views.land_page),
    # path('login', views.login_staff),
    # path('chair/add',views.addNewChair),
    # path('logout',views.logout_staff),
    path('login', views.login_admin),
    path('logout',views.logout_admin),
    path('staff/add',views.add_staff),
    path('staff',views.staff_list),
    path('user',views.user_list),
    path('user/delete/<int:id>',views.delete_user),
    path('order',views.order_list),
    path('order/<int:order_id>',views.confirm_order),
    path('orders/detail/<int:order_id>',views.order_detail),
    path('furniture',views.furniture_list),

    path('kategori',views.kategori_list),
    path('kategori/add',views.addNewKategori),

    path('chat/<int:user_id>',views.reply_chat),
    path('furniture/add',views.addNewFurniture),
    path('furniture/delete/<int:furtniture_id>',views.delete_furniture),
    path('furniture/edit/<int:furtniture_id>',views.edit_furniture),
    path('profile/other-view/<int:id_user>',views.view_profile),
    path('',views.base),
]
