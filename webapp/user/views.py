from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from django.shortcuts import render
from .forms import RegisterUserForm

def land_page(request):
    u = User.objects.get(username = 'test')
    print(u.username)
    return render(request,'land_page.html')

def login(request):
    return render(request,'login.html')

def register(request):
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        print(username)
        form = RegisterUserForm(request.POST)
        if (form.is_valid()):
            print('abc')
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            user = User.objects.create_user(username = username, email = email, password = password)
            user.save()
    return render(request,'register.html')