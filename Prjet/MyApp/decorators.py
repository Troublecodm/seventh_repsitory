from django.shortcuts import redirect
from django.contrib.auth.models import Group

def unauthenticated_user(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
          return redirect('index')
        else:
          return view_func(request,*args, **kwargs)
    return wrapper_func

def admin_only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('index')
        if group == 'admin':
            return view_func(request,*args, **kwargs)        
    return wrapper_func