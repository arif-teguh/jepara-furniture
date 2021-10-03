from user.models import FurnitureModels
from .models import IsStaffModel
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .forms import AddFurnitureForm
from django.contrib.auth.decorators import login_required
from .middleware import user_is_staff

home_staff = '/staff'
home = '/'
#from .models import ChairMode
@user_is_staff
def land_page(request):
    return render(request,'staff/land_page.html')

def login_staff(request):
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        staff = IsStaffModel.objects.get(user = user)
        if user is not None and staff is not None:
            login(request, user)
            return redirect(home_staff)
    return render(request,'staff/login.html')

@user_is_staff
def addNewFurniture(request):
    if (request.method == "POST"):
        name = request.POST['nama']
        harga = request.POST['harga']
        kategori = request.POST['kategori'].lower()
        gambar =request.FILES['file']
        form = AddFurnitureForm(request.POST)
        if(form.is_valid()):
            chair = FurnitureModels.objects.create(nama =  name , harga = harga, gambar = gambar, kategori = kategori)
            chair.save()
            return redirect(home_staff)
    print('haha')
    return render(request, 'staff/addfurniture.html')

@login_required
def logout_staff(request):
    logout(request)
    return render(request,'staff/login.html')



