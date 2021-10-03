from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from user.forms import RegisterUserForm 
from django.contrib.auth.decorators import login_required
from staff.models import IsStaffModel
from .middleware import user_is_admin
from django.contrib import messages
# Create your views here.
@user_is_admin
def add_staff(request):
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        print(username)
        form = RegisterUserForm(request.POST)
        if (form.is_valid()):
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            user = User.objects.create_user(username = username, email = email, password = password)
            user.save()
            staff = IsStaffModel.objects.create(user = user)
            staff.save()
            return redirect('/admin/staff')
    return render(request,'admin/register_staff.html')

@user_is_admin
def staff_list(request):
    staffs = IsStaffModel.objects.all()

    return render(request,'admin/staff_list.html',{'staffs':staffs})