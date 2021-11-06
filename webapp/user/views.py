from typing import overload
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
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/login"
#from .models import ChairMode
def land_page(request):
    return render(request,'user/home.html')

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


@login_required(login_url = "/login")
def logout_user(request):
    logout(request)
    return render(request,'user/land_page.html')


def view_furniture(request,kategori):
    furnitures = FurnitureModels.objects.filter(kategori=kategori)
    final_furnitures = []
    for each in furnitures :
        furnitur = {}
        furnitur["nama"] = each.nama
        furnitur["harga"] = each.harga
        furnitur["info"] = each.info
        furnitur["gambar"] = (str(each.gambar)).replace("static/","")
        furnitur["rating"] = calculate_rating(each)
        furnitur["kategori"] = each.kategori
        furnitur["id"] = each.id
        final_furnitures.append(furnitur)
    return render(request,'user/furniture_list.html',{"furnitures" : final_furnitures})


def view_furniture_details(request,kategori,id):
    furniture = FurnitureModels.objects.get(id=id)
    gambar_furniture = []
    gambar_furniture.append((str(furniture.gambar)).replace("static/",""))
    reviews = ReviewModels.objects.filter(futniture = furniture)
    rating = calculate_rating(furniture) 
    return render(request,'user/detail.html',{"furniture" : furniture, "reviews": reviews, "rating":rating,"gambar_furniture":gambar_furniture})

@login_required(login_url = "/login")
def review_furniture(request,kategori,id):
    furniture = FurnitureModels.objects.get(kategori=kategori,id=id)
    curr_user = User.objects.get(id = request.user.id)
    rating = request.POST['rating']
    notes = request.POST['notes']
    review = ReviewModels.objects.create(furniture = furniture , user = curr_user, notes = notes , rating = rating)
    review.save()
    all_review = ReviewModels.objects.filter(furniture=furniture)
    return render(request,'user/furniture_detail.html',{"furniture" : furniture, "reviews": all_review})

@login_required(login_url = "/login")
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
    return render(request,'user/chat.html',{"contents" : all_chat})

@login_required(login_url = "/login")
def call(request):
    return render(request,'user/call.html')


@login_required(login_url = "/login")
def complain(request):
    return render(request,'user/complain.html')


@login_required(login_url = "/login")
def preorder(request):
    return render(request,'user/preorder.html')

@login_required(login_url = "/login")
def checkout(request):
    return render(request,'user/checkout.html')


@login_required(login_url = "/login")
def payment(request):
    return render(request,'user/payment.html')


def calculate_rating(furniture):
    reviews = ReviewModels.objects.filter(futniture = furniture)
    tmp_value = 0
    for review in reviews:
        tmp_value += review.rating
    final_value = "-"
    if reviews :
        final_value = str(tmp_value/reviews.count())
    return final_value