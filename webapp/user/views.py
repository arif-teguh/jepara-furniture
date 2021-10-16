from .models import FurnitureModels, ReviewModels , ChatTopicModels,ChatContentModels
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .forms import RegisterUserForm 
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
    return render(request,'user/login.html')

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
            return redirect('/login')
    return render(request,'user/register.html')


@login_required
def logout_user(request):
    logout(request)
    return render(request,'user/land_page.html')


def view_furniture(request,kategori):
    furniture = FurnitureModels.objects.filter(kategori=kategori)
    return render(request,'user/furniture_list.html',{"furniture" : furniture})


def view_furniture_details(request,kategori,id):
    furniture = FurnitureModels.objects.get(kategori=kategori,id=id)
    reviews = ReviewModels.objects.filter(furniture=furniture)
    return render(request,'user/furniture_detail.html',{"furniture" : furniture, "reviews": reviews})

@login_required
def review_furniture(request,kategori,id):
    furniture = FurnitureModels.objects.get(kategori=kategori,id=id)
    curr_user = User.objects.get(id = request.user.id)
    rating = request.POST['rating']
    notes = request.POST['notes']
    review = ReviewModels.objects.create(furniture = furniture , user = curr_user, notes = notes , rating = rating)
    review.save()
    all_review = ReviewModels.objects.filter(furniture=furniture)
    return render(request,'user/furniture_detail.html',{"furniture" : furniture, "reviews": all_review})

@login_required
def chat(request):
    curr_user = User.objects.get(id = request.user.id)
    try :
        topic = ChatTopicModels.objects.get(user = curr_user)
    except ObjectDoesNotExist:
        topic = ChatTopicModels.objects.create(user = curr_user)
        topic.save()
    if (request.method == "POST"):
        content = request.POST['content']
        cahat_content = ChatContentModels.objects.create(user = curr_user,topic = topic, content = content)
        cahat_content.save()
    all_chat = ChatContentModels.objects.filter(topic = topic)
    return render(request,'user/chat_board.html',{"contents" : all_chat})