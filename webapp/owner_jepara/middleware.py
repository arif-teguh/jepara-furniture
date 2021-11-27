from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

home = '/'

def user_is_owner(func):
    def function_wrapper(*args, **kwargs):
        try :
            req = args[0]
            user = req.user
            if (user.username).lower() == "owner":
                return func(*args, **kwargs)
            return redirect(home)
        except ObjectDoesNotExist:
             return redirect(home)
    return function_wrapper