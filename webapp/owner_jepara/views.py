from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
import user.models as userModel
from .middleware import user_is_owner

@user_is_owner
def admin_list(request):
    user_in_admin = User.objects.filter(is_superuser=True)
    admin_profile = userModel.ProfileModels.objects.filter(user__in = user_in_admin )
    return render(request,'owner/admin_list.html',{'admins':admin_profile})



@user_is_owner
def order_list(request):
    payment = userModel.PaymentModels.objects.filter(status = "Completed")
    return render( request, 'admin/order_list.html',{'payment':payment})
    