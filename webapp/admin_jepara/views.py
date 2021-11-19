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
import user.models as userModel
from .forms import AddFurnitureForm
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
    staffs = IsStaffModel.objects.all()
    user_in_staff = []
    for staff in staffs :
        user_in_staff.append(staff.user.id)
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
def base(request):
    return render(request, 'base_admin.html')