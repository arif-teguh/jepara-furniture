from telnetlib import STATUS
import user.models as userModel
from .models import IsStaffModel
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .middleware import user_is_staff
from django.contrib import messages

home_staff = '/staff/chat'
home = '/'
#from .models import ChairMode
@user_is_staff
def land_page(request):
    return render(request,'staff/chat.html')

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



def logout_staff(request):
    logout(request)
    return render(request,'staff/login.html')


@user_is_staff
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
    return render(request,'staff/chat.html',{"contents" : all_chat, "user_chat" : user_chat})

@user_is_staff
def reply_chat_reload(request,user_id):
    user_chat = User.objects.get(id = user_id)
    curr_user = User.objects.get(id = request.user.id)
    try :
        topic = userModel.ChatTopicModels.objects.get(user = user_chat)
    except ObjectDoesNotExist:
        topic = userModel.ChatTopicModels.objects.create(user = user_chat)
        topic.save()
    all_chat = userModel.ChatContentModels.objects.filter(topic = topic)
    return render(request,'staff/chat_content.html',{"contents" : all_chat, "user_chat" : user_chat})

@user_is_staff
def complain_list(request):
    complains = userModel.ComplainModels.objects.all()
    final_complains = []
    for each in complains:
        complain = {}
        complain["complain"] = each
        final_complains.append(complain)
    return render(request, 'staff/complain_list.html',{"complains": final_complains})


@user_is_staff
def accept_preorder(request,preorder_id):
    preorder = userModel.PreOrderModels.objects.get(id=preorder_id)
    preorder.status = 'accepted'
    preorder.save()
    messages.success(request, ("Preorder berhasil diterima !"))
    return redirect(request.META.get('HTTP_REFERER'))
    


@user_is_staff
def preorder_list(request):
    preorders = userModel.PreOrderModels.objects.all().exclude(status='deleted')
    # in case accepted ilang
    # preorders = userModel.PreOrderModels.objects.all().exclude(status__in=['deleted','accepted','viewed']) 
    final_preorders = []
    for each in preorders:
        preorder = {}
        preorder["preorder"] = each
        final_preorders.append(preorder)
    return render(request, 'staff/preorder_list.html',{"preorders": final_preorders})

    # furnitures = userModel.FurnitureModels.objects.all()
    # final_furnitures = []
    # for each in furnitures:
    #     furnitur = {}
    #     furnitur["furniture"] = each
    #     final_furnitures.append(furnitur)
    # return render(request, "admin/furniture_list.html", {"furnitures": final_furnitures})

    
@user_is_staff
def chat_list(request):
    chat_list = userModel.ChatTopicModels.objects.all()
    return render ( request, 'staff/chat_list.html',{"chat_list": chat_list})


@user_is_staff
def delete_complain(request,complain_id):
    try:
        complain = userModel.ComplainModels.objects.get(id = complain_id)
        messages.success(request, ("complain berhasil dihapus !"))
        complain.delete()
    except :
        messages.error(request , ("complain tidak ada!"))
    return redirect(request.META.get('HTTP_REFERER'))



@user_is_staff
def delete_preorder(request,preorder_id):
    try:
        preorder = userModel.PreOrderModels.objects.get(id = preorder_id)
        preorder.status = 'deleted'
        preorder.save()
        messages.success(request, ("Preorder berhasil dihapus !"))
    except :
        messages.error(request , ("Preorder tidak ada!"))
    return redirect(request.META.get('HTTP_REFERER'))