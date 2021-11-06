from typing import overload

from django.http.response import HttpResponseNotAllowed
from .models import FurnitureModels, OrderModels, ReviewModels, ChatTopicModels, ChatContentModels, OrderModels,ShoppingCartModels
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .forms import RegisterUserForm
from django.contrib.auth.decorators import login_required
import random
home = "/"
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/login"
# from .models import ChairMode
def land_page(request):
    return render(request, "user/home.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(home)
    return render(request, "user/login.html")


def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        print(username)
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            email = request.POST["email"]
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect("/login")
    return render(request, "user/register.html")


@login_required(login_url="/login")
def logout_user(request):
    logout(request)
    return render(request, "user/land_page.html")


def view_furniture(request, kategori):
    furnitures = FurnitureModels.objects.filter(kategori=kategori)
    final_furnitures = []
    for each in furnitures:
        furnitur = {}
        furnitur["furniture"] = each
        furnitur["rating"] = calculate_rating(each)
        final_furnitures.append(furnitur)
    return render(request, "user/furniture_list.html", {"furnitures": final_furnitures})


def view_furniture_details(request, kategori, id):
    furniture = FurnitureModels.objects.get(id=id)
    gambar_furniture = []
    gambar_furniture.append((str(furniture.gambar)).replace("static/", ""))
    reviews = ReviewModels.objects.filter(futniture=furniture)
    rating = calculate_rating(furniture)
    all_furniture = list(FurnitureModels.objects.all())
    count = 4 if len(all_furniture) >= 4 else len(all_furniture)
    random_furniture = random.sample(all_furniture, count)
    return render(
        request,
        "user/detail.html",
        {"furniture": furniture, "reviews": reviews, "rating": rating, "gambar_furniture": gambar_furniture, "other_furniture" : random_furniture },
    )


@login_required(login_url="/login")
def review_furniture(request, kategori, id):
    furniture = FurnitureModels.objects.get(kategori=kategori, id=id)
    curr_user = User.objects.get(id=request.user.id)
    rating = request.POST["rating"]
    notes = request.POST["notes"]
    review = ReviewModels.objects.create(furniture=furniture, user=curr_user, notes=notes, rating=rating)
    review.save()
    all_review = ReviewModels.objects.filter(furniture=furniture)
    return render(request, "user/furniture_detail.html", {"furniture": furniture, "reviews": all_review})


@login_required(login_url="/login")
def chat(request):
    curr_user = User.objects.get(id=request.user.id)
    try:
        topic = ChatTopicModels.objects.get(user=curr_user)
    except ObjectDoesNotExist:
        topic = ChatTopicModels.objects.create(user=curr_user)
        topic.save()
    if request.method == "POST":
        content = request.POST["content"]
        cahat_content = ChatContentModels.objects.create(user=curr_user, topic=topic, content=content)
        cahat_content.save()
    all_chat = ChatContentModels.objects.filter(topic=topic)
    return render(request, "user/chat.html", {"contents": all_chat})


@login_required(login_url="/login")
def call(request):
    return render(request, "user/call.html")


@login_required(login_url="/login")
def complain(request):
    return render(request, "user/complain.html")


@login_required(login_url="/login")
def preorder(request):
    return render(request, "user/preorder.html")


@login_required(login_url="/login")
def checkout_fast(request,id_furniture):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        jumlah = int(request.POST["jumlah"])
        furnitur = FurnitureModels.objects.get(id=id_furniture)
        if(int(jumlah) > furnitur.stock or int(jumlah) <=0 ):
            return redirect(request.META.get('HTTP_REFERER'))
        try :
            keranjang = ShoppingCartModels.objects.get(user=user)
        except ObjectDoesNotExist:
            keranjang = ShoppingCartModels.objects.create(user=user, total = 0) 
        current_total = furnitur.harga * jumlah           
        order = OrderModels.objects.create(furnitur = furnitur,user = user, jumlah= jumlah, keranjang = keranjang, total = current_total)
        keranjang.total += current_total
        keranjang.total_furnitur = jumlah
        order.save()
        keranjang.save()
    keranjang = ShoppingCartModels.objects.get(user=user)
    all_order = OrderModels.objects.filter(user=user , keranjang = keranjang)
    return render(request, "user/checkout.html" ,{"orders": all_order , "keranjang" : keranjang})

@login_required(login_url="/login")
def checkout_all(request):
    user = User.objects.get(id=request.user.id)
    try :
        keranjang = ShoppingCartModels.objects.get(user=user)
    except ObjectDoesNotExist:
        return redirect(request.META.get('HTTP_REFERER'))
    keranjang = ShoppingCartModels.objects.get(user=user)
    all_order = OrderModels.objects.filter(user=user , keranjang = keranjang)
    return render(request, "user/checkout.html" ,{"orders": all_order , "keranjang" : keranjang})    

@login_required(login_url="/login")
def payment(request):
    user = User.objects.get(id=request.user.id)
    keranjang = ShoppingCartModels.objects.get(user=user)
    return render(request, "user/payment.html",{"keranjang": keranjang})


def calculate_rating(furniture):
    reviews = ReviewModels.objects.filter(futniture=furniture)
    tmp_value = 0
    for review in reviews:
        tmp_value += review.rating
    final_value = "-"
    if reviews:
        final_value = str(tmp_value / reviews.count())
    return final_value
