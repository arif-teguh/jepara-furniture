from typing import overload
from unicodedata import category
from django.core import exceptions
from datetime import datetime
from django.http.response import HttpResponseNotAllowed
from .models import (
    FurnitureModels, OrderModels, ReviewModels, ChatTopicModels,
    ChatContentModels, OrderModels,ShoppingCartModels, ProfileModels,ComplainModels, PreOrderModels, PaymentModels, KategoriModels
)
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .forms import RegisterUserForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
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
        else :
            messages.error(request, 'Username atau password salah')
    return render(request, "user/login.html")


def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        print(username)
        if request.POST.get('region',"-") != "jabodetabek":
            messages.error(request, 'Layanan hanya bisa untuk daerah Jabodetabek saja!')
            return redirect(request.META.get('HTTP_REFERER'))
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            email = request.POST["email"]
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            alamat = "-"
            gender = request.POST.get('gender',"-")
            phone = request.POST.get('phone',"-")
            full_name = request.POST.get('full_name',"-")
            profile = ProfileModels.objects.create(
                alamat = alamat,
                gender = gender,
                phone = phone,
                full_name = full_name,
                user = user
            )
            profile.save()
            return redirect("/login")
        else :
            messages.error(request, 'Ada yang salah dengan user mu')
    return render(request, "user/register.html")


@login_required(login_url="/login")
def logout_user(request):
    logout(request)
    return render(request, "user/home.html")


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
def review_furniture(request, id):
    if request.method == "POST":
        furniture = FurnitureModels.objects.get(id=id)
        user_has_review = ReviewModels.objects.filter(user = request.user ,futniture=furniture)
        if user_has_review.count():
            messages.error(request, 'Kamu sudah menulis review pada furniture ini!')
            return redirect(request.META.get('HTTP_REFERER'))
        curr_user = request.user
        user_has_order_complete = OrderModels.objects.filter(user=curr_user,furnitur = furniture)
        payment_complete = False
        for order in user_has_order_complete:
            payment = PaymentModels.objects.filter(user = curr_user, keranjang_deleted_id = order.keranjang_deleted_id, status = "Completed")
            if payment.count() > 0:
                payment_complete = True
                break
        if not payment_complete:
            messages.error(request, 'Kamu belum pernah membeli furniture ini , Kamu tidak bisa menreview furnitur ini!')
            return redirect(request.META.get('HTTP_REFERER'))
        rating = request.POST["star"]
        notes = request.POST["notes"]
        review = ReviewModels.objects.create(futniture=furniture, user=curr_user, notes=notes, rating=rating)
        review.save()
    return redirect(request.META.get('HTTP_REFERER'))
    


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
def chat_reload(request):
    curr_user = User.objects.get(id=request.user.id)
    try:
        topic = ChatTopicModels.objects.get(user=curr_user)    
    except ObjectDoesNotExist:
        topic = ChatTopicModels.objects.create(user=curr_user)
        topic.save()
    all_chat = ChatContentModels.objects.filter(topic=topic)
    return render(request, "user/chat_content.html", {"contents": all_chat})

# @login_required(login_url="/login")
# def call(request):
#     return render(request, "user/call.html")


@login_required(login_url="/login")
def complain(request):
    payment = PaymentModels.objects.filter(user=request.user, status__in = ["Completed","Delivered"])
    if payment.count() == 0 :
        messages.error(request, 'Tidak dapat melakukan komplain dikarenakan anda tidak memiliki pesanan')
        return redirect(request.META.get('HTTP_REFERER'))
    if request.method == "POST":
        try :
            alamat = request.POST['alamat']
            nama = request.POST['nama']
            email = request.POST['email']
            deskripsi = request.POST['deskripsi']
            pic =request.FILES.get('file')
            complain = ComplainModels.objects.create(
                user = request.user,
                alamat = alamat,
                nama = nama,
                email = email,
                deskripsi = deskripsi,
            )
            if pic :
                complain.picture = pic
            complain.save()
            messages.success(request, 'Komplain berhasil dikirimkan !')
        except exceptions as e: 
            print(e)
            messages.error(request, 'Ada data yang salah !')
    return render(request, "user/complain.html")


@login_required(login_url="/login")
def preorder(request):
    if request.method == "POST":
        try :
            alamat = request.POST['alamat']
            nama = request.POST['nama']
            email = request.POST['email']
            jenis_furniture = request.POST['jenis_furniture']
            pic =request.FILES.get('file')
            preorder = PreOrderModels.objects.create(
                user = request.user,
                alamat = alamat,
                nama = nama,
                email = email,
                jenis_furniture = jenis_furniture,
            )
            if pic :
                preorder.picture = pic
            preorder.save()
            messages.success(request, 'Preorder berhasil dikirimkan !')
        except : 
            messages.error(request, 'Ada data yang salah atau kurang!')
    return render(request, "user/preorder.html")


@login_required(login_url="/login")
def checkout_fast(request,id_furniture):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        jumlah = int(request.POST["jumlah"])
        furnitur = FurnitureModels.objects.get(id=id_furniture)
        if(int(jumlah) > furnitur.stock or int(jumlah) <=0 ):
            messages.error(request, 'Form submission fail')
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
        messages.success(request, (f"Berhasil menambahkan {jumlah} {furnitur.nama} kedalam keranjang"))
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
    try :
        keranjang = ShoppingCartModels.objects.get(user=user)
    except :
        messages.info(request, 'Keranjang anda masih kosong isi terlebih  dahulu!')
        return redirect("/")
    if request.method == "POST":
        try:
            payment = PaymentModels.objects.filter(user=request.user).exclude(status = "Completed")
            if payment.count() > 0 :
                messages.error(request, 'Tidak dapat melakukan pembayaran dikarenakan Karena pembayaran sebelumnya belum selesai')
                return redirect(request.META.get('HTTP_REFERER'))
            profile = ProfileModels.objects.get(user = request.user)
            picture =request.FILES['bukti_pembayaran']
            if not picture :
                raise
            if profile.alamat == "alamat" or not bool(profile.alamat):
                messages.error(request, 'Ganti alamat terlebih dahulu di halaman profile sebelum melakukan pembayaran')
                return redirect(request.META.get('HTTP_REFERER'))
            payment = PaymentModels.objects.create(
                user = request.user,
                alamat = profile.alamat,
                total = keranjang.total,
                status = "Pending",
                bukti_pembayaran = picture,
                total_furnitur = keranjang.total_furnitur,
                keranjang_deleted_id = keranjang.id
            )
            payment.save()
            orders = OrderModels.objects.filter(keranjang = keranjang)
            for order in orders :
                furniture = order.furnitur
                furniture.stock -= order.jumlah
                furniture.save()
                order.keranjang_deleted_id = keranjang.id
                order.save()
            keranjang.delete()
            return redirect("/")
        except :
            messages.error(request, 'Foto bukti pembayaran harus ada!')
    return render(request, "user/payment.html",{"keranjang": keranjang})


def calculate_rating(furniture):
    reviews = ReviewModels.objects.filter(futniture=furniture)
    tmp_value = 0
    for review in reviews:
        tmp_value += review.rating
    final_value = "-"
    if reviews:
        final_value = tmp_value / reviews.count()
        if len(str(final_value)) > 3:
            final_value =  "{:.2f}".format(final_value)
    return final_value

def profile(request):
    try:
        profile = ProfileModels.objects.get(user = request.user)
    except:
        profile = ProfileModels.objects.create(
                alamat = "alamat",
                gender = "M",
                phone = "phone",
                full_name = "full_name",
                user = request.user
            )
    return render(request, "profile.html",{"profile": profile})



def edit_profile(request):
    profile = ProfileModels.objects.get(user = request.user)
    if request.method == "POST":
        profile.alamat = request.POST['alamat']
        profile.gender = request.POST['gender']
        profile.full_name = request.POST['full_name']
        profile.phone = request.POST['phone']
        profile.birth_date = str(request.POST['birth_date'])
        profile_pic =request.FILES.get('file')
        if profile_pic :
            profile.profile_pic = profile_pic
        profile.save()
    profile.birth_date = str(profile.birth_date)
    return render(request, "profile-edit.html",{"profile": profile})


@login_required(login_url="/login")
def confirmation(request):
    try:
        payment = PaymentModels.objects.get(user=request.user , status = "Delivered")
    except:
        messages.error(request, 'Tidak ada pesanan yang butuh konfirmasi !')
        return redirect("/")
    keranjang_deleted_id = payment.keranjang_deleted_id
    all_order = OrderModels.objects.filter(user=request.user , keranjang_deleted_id = keranjang_deleted_id)
    if request.method == "POST":
        payment.status = "Completed"
        payment.tanggal_bayar =  datetime.now()
        payment.save()
        messages.success(request, 'Pesanan berhasil diselesaikan !')
        return redirect("/")
    #return render(request, "user/checkout.html" ,{"orders": all_order , "keranjang" : keranjang})
    return render(request, "user/confirmation.html",{"orders": all_order, "keranjang": payment})


@login_required(login_url="/login")
def detele_some_order(request, id):
    try:
        
        order = OrderModels.objects.get(id = id , user= request.user)
        harga = order.total
        keranjang = ShoppingCartModels.objects.get(user= request.user)
        keranjang.total -= harga
        keranjang.save()
        order.delete()
        messages.success(request , 'Sukses mendelete orderan !')
    except:
        messages.error(request, 'Gagal Mendelte order!')
    return redirect(request.META.get('HTTP_REFERER'))


# def get_category(request):
#     category = FurnitureModels.objects.all().values('kategori').annotate(dcount=Count('kategori'))
#     categories = []
#     for a in category:
#         dict = {}
#         kategori = a.get("kategori")
#         exclude = ["chair","wardobe","table","bedroom"]
#         if kategori not in exclude:
#             dict = {}
#             dict["name"] = kategori
#             dict["name2"] = kategori.capitalize()
#             categories.append(dict)
#     return render(request, "user/category.html",{"categories":categories,})

def get_category(request):
    kategori = KategoriModels.objects.all()
    categories = []
    for a in kategori:
        dict = {}
        kategori = a.nama
        exclude = ["chair","wardobe","table","bedroom"]
        if kategori not in exclude:
            dict = {}
            dict["name"] = kategori
            dict["name2"] = kategori.capitalize()
            categories.append(dict)
    return render(request, "user/category.html",{"categories":categories,})


def get_notif(request):
    try:
        preorder_deleted = PreOrderModels.objects.filter(user= request.user, status = 'deleted')
        preorder_accepeted = PreOrderModels.objects.filter(user= request.user, status = 'accepted')
        accepeted = len(preorder_accepeted)
        deleted = len(preorder_deleted)
        print('aaaaaa')
        if accepeted == 0 and deleted == 0:
            print('aaaaaa2')
            return HttpResponse('')
        else:
            print('aaaaaa3')
            # return HttpResponse('ada notif')
            return render(request, "user/notif.html",{"accepted":accepeted, "deleted":deleted})
    except:
        return HttpResponse('')

@login_required
def dismiss_notif(request):
    try:
        preorders = PreOrderModels.objects.filter(user = request.user)
        for preorder in preorders:
            if preorder.status == 'deleted':
                preorder.delete()
            else:
                preorder.status = 'viewed'
                preorder.save()
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        return redirect(request.META.get('HTTP_REFERER'))