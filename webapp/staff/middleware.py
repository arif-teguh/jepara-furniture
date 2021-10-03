from user.models import chairModels
from .models import IsStaffModel
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .forms import AddChairForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
home = '/'

def user_is_staff(func):
    def function_wrapper(*args, **kwargs):
        try :
            req = args[0]
            user = req.user.is_authenticated
            if not user:
                return redirect(home)
            else :
                staff = IsStaffModel.objects.get(user = req.user)
                if not staff :
                    return redirect(home)
            return func(*args, **kwargs)
        except ObjectDoesNotExist:
             return redirect(home)
    return function_wrapper