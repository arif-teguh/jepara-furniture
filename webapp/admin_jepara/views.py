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


from .middleware import user_is_admin
from django.contrib import messages
import user.models as userModel
from .forms import AddFurnitureForm
from django.contrib import messages
# Create your views here.

home_admin = '/admin/order'

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
            alamat = request.POST.get('alamat')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            full_name = request.POST.get('full_name')
            birth_date = request.POST.get('birth_date')
            user = User.objects.create_user(username = username, email = email, password = password, is_staff = True)
            user.save()
            profile = userModel.ProfileModels.objects.create(
                alamat = alamat,
                gender = gender,
                phone = phone,
                full_name = full_name,
                birth_date = birth_date,
                user = user
            )
            profile.save()
            messages.success(request, (f"{user.username} berhasil ditambahkan !"))
        else :
            messages.error(request, 'Ada data yang kurang atau belum diisi!')
    return render(request,'admin/register_staff.html')

@user_is_admin
def staff_list(request):
    user_in_staff = User.objects.filter(is_staff=True)
    staffs_profile = userModel.ProfileModels.objects.filter(user__in = user_in_staff )
    return render(request,'admin/staff_list.html',{'staffs':staffs_profile})

@user_is_admin
def user_list(request):
    staffs = User.objects.filter(is_staff = True)
    user_in_staff = []
    for staff in staffs :
        user_in_staff.append(staff.id)
    staffs_profile = userModel.ProfileModels.objects.all().exclude(user__id__in = user_in_staff )
    return render(request,'admin/user_list.html',{'staffs':staffs_profile})
    
@user_is_admin
def furniture_list(request):
    furnitures = userModel.FurnitureModels.objects.all()
    final_furnitures = []
    for each in furnitures:
        furnitur = {}
        furnitur["furniture"] = each
        final_furnitures.append(furnitur)
    return render(request, "admin/furniture_list.html", {"furnitures": final_furnitures})

@user_is_admin
def reply_chat(request,user_id):
    user_chat = User.objects.get(id = user_id)
    curr_user = User.objects.get(id = request.user.id)
    try :
        topic = userModel.ChatTopicModels.objects.get(user = user_chat)
    except ObjectDoesNotExist:
        topic = userModel.ChatTopicModels.objects.create(user = user_chat)
        topic.save()
    if (request.method == "POST"):
        content = request.POST['content']
        cahat_content = userModel.ChatContentModels.objects.create(user = curr_user,topic = topic, content = content)
        cahat_content.save()
    all_chat = userModel.ChatContentModels.objects.filter(topic = topic)
    return render(request,'admin/chat.html',{"contents" : all_chat})



@user_is_admin
def addNewFurniture(request):
    form = AddFurnitureForm(request.POST)
    if (request.method == "POST"):
        name = request.POST['nama']
        harga = request.POST['harga']
        info = request.POST['info']
        stock = request.POST['stok']
        kategori = request.POST['kategori'].lower()
        gambar =request.FILES.get('file')
        #form = AddFurnitureForm(request.POST)
        if(form.is_valid()):
            furniture = userModel.FurnitureModels.objects.create(nama =  name , harga = harga, gambar = gambar, kategori = kategori, info = info , stock = stock)
            furniture.save()
            messages.success(request, (f"{furniture.nama} berhasil ditambahkan !"))
        else :
            messages.error(request, 'Ada data yang kurang atau belum diisi!')
    return render(request, 'admin/addfurniture.html',{'form': form})

@user_is_admin
def delete_furniture(request, furtniture_id):
    furniture = userModel.FurnitureModels.objects.get(id = furtniture_id)
    messages.success(request, (f"{furniture.nama} berhasil dihapus !"))
    furniture.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@user_is_admin
def edit_furniture(request, furtniture_id):
    try:
        furniture = userModel.FurnitureModels.objects.get(id = furtniture_id)
        if (request.method == "POST"):
            furniture.name = request.POST['nama']
            furniture.harga = request.POST['harga']
            furniture.info = request.POST['info']
            furniture.stock = request.POST['stok']
            furniture.kategori = request.POST['kategori'].lower()
            gambar =request.FILES.get('file',"tidak ada")
            if gambar != "tidak ada":
                furniture.gambar =gambar
            furniture.save()
            messages.success(request, (f"{furniture.nama} berhasil diedit !"))
        return render(request, 'admin/editfurniture.html',{'furniture': furniture})
    except:
        messages.error(request, ("Terjadi kesalahan furniture tidak ada atau ada value yang slaah !"))
        return redirect(request.META.get('HTTP_REFERER'))        

@user_is_admin
def base(request):
    return render(request, 'admin/order.html')

def login_admin(request):
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request, user)
            return redirect(home_admin)
    return render(request,'admin/login.html')

def logout_admin(request):
    logout(request)
    return render(request,'admin/login.html')


@user_is_admin
def view_profile(request, id_user):
    user = User.objects.get(id = id_user)
    profile = userModel.ProfileModels.objects.get(user = user)
    return render( request, 'admin/profile-viewonly.html',{'profile':profile})


@user_is_admin
def order_list(request):
    payment = userModel.PaymentModels.objects.all().exclude(status = "Completed")
    return render( request, 'admin/order_list.html',{'payment':payment})

@user_is_admin
def confirm_order(request, order_id):
    try :
        payment = userModel.PaymentModels.objects.get(id=order_id, status = "Pending")
        payment.status = "Delivered"
        payment.save()
        messages.success(request, ("Status pembayaran berhasil diubah menjadi dikirm !"))
    except :
        messages.error(request, ("Status pembayaran gagal diubah!"))
        return redirect(request.META.get('HTTP_REFERER'))    
    return redirect(request.META.get('HTTP_REFERER'))

@user_is_admin
def order_detail(request, order_id):
    try:
        payment = userModel.PaymentModels.objects.get(id = order_id)
    except:
        messages.error(request, 'Tidak ada pesanan yang butuh konfirmasi !')
        return redirect("/")
    keranjang_deleted_id = payment.keranjang_deleted_id
    all_order = userModel.OrderModels.objects.filter(user=payment.user , keranjang_deleted_id = keranjang_deleted_id)
    #return render(request, "user/checkout.html" ,{"orders": all_order , "keranjang" : keranjang})
    return render(request, "admin/order_detail.html",{"orders": all_order, "keranjang": payment})