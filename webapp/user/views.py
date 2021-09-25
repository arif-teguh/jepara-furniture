from .models import chairModels
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .forms import RegisterUserForm  ,AddChairForm
from django.contrib.auth.decorators import login_required
home = '/'
#from .models import ChairMode
def land_page(request):
    return render(request,'land_page.html')

def login_user(request):
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(home)
    return render(request,'login.html')

def register_user(request):
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
    return render(request,'register.html')

def addNewChair(request):
    if (request.method == "POST"):
        name = request.POST['name']
        harga = request.POST['harga']
        form = AddChairForm(request.POST)
        #if(form.is_valid()):
        chair = chairModels.objects.create(nama =  name , harga = harga)
        chair.save()
        return redirect(home)
    return render(request,'addchair.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('/login')



