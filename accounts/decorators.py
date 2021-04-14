from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(func):
    def inner_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return func(request, *args, **kwargs)
    return inner_func

def allowed_users(allowed=[]):
    def decorator(func):
        def inner_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed:
                return func(request, *args, **kwargs)
            else:
                return HttpResponse("you are not allowed")
        
        return inner_func
    return decorator


def admin_only(func):
        def inner_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group == "customer":
                  return redirect("user")
            if group == "admin":
                  return func(request, *args, **kwargs)
        return inner_func
