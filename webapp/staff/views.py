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