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
from ..user.models import ChatTopicModels,ChatContentModels
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
            user = User.objects.create_user(username = username, email = email, password = password)
            user.save()
            staff = IsStaffModel.objects.create(user = user)
            staff.save()
            return redirect('/admin/staff')
    return render(request,'admin/register_staff.html')

@user_is_admin
def staff_list(request):
    staffs = IsStaffModel.objects.all()

    return render(request,'admin/staff_list.html',{'staffs':staffs})


@user_is_admin
def reply_chat(request,user_id):
    user_chat = User.objects.get(id = user_id)
    curr_user = User.objects.get(id = request.user.id)
    try :
        topic = ChatTopicModels.objects.get(user = user_chat)
    except ObjectDoesNotExist:
        topic = ChatTopicModels.objects.create(user = user_chat)
        topic.save()
    if (request.method == "POST"):
        content = request.POST['content']
        cahat_content = ChatContentModels.objects.create(user = curr_user,topic = topic, content = content)
        cahat_content.save()
    all_chat = ChatContentModels.objects.filter(topic = topic)
    return render(request,'admin/chat_board.html',{"contents" : all_chat})