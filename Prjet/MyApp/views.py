from django.shortcuts import render
from django.urls import reverse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse,HttpResponseRedirect
from .models import ToDoList,Profile
from .forms import CreateUserForm
from .decorators import unauthenticated_user,admin_only

# Create your views here.

# HOME PAGE
def index(request):
    group = None
    template = loader.get_template('index.html')
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    context = {
        'group':group,
    }
    return HttpResponse(template.render(context,request))

# ALL TO DO LISTS PAGE
@login_required(login_url='login')
def to_do(request):
    group = None
    todo = ToDoList.objects.all()
    cu = request.user
    template = loader.get_template('to_do.html')
    if cu.groups.exists():
        group = cu.groups.all()[0].name
        if group == 'customer':
            list = cu.profile.todolist_set.all()
            context = {
                'list':list,
                'todo':todo,
                'group':group,
            }
            return HttpResponse(template.render(context,request))
        elif group == 'admin':
            list = ToDoList.objects.all()
            context = {
                'list':list,
                'group':group,
            }    
            return HttpResponse(template.render(context,request))
    return HttpResponse(template.render(context,request))

def todo_completed(request):
    group = request.user.groups.all()[0].name
    list = request.user.profile.todolist_set.filter(iscompleted=True)
    template = loader.get_template('todo_completed.html')
    context = {
          'list':list,
          'group': group,
    }
    return HttpResponse(template.render(context,request))

def todo_notcompleted(request):
    list = request.user.profile.todolist_set.filter(iscompleted=False)
    template = loader.get_template('todo_notcompleted.html')
    context = {
          'list':list,
    }
    return HttpResponse(template.render(context,request))
# ADD A TO DO LIST PAGE
@login_required(login_url='login')
def add_to_do(request):
    user = request.user
    group = user.groups.all()[0].name
    template = loader.get_template('add_to_do.html')
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        post_by = request.user.profile
        save_list = ToDoList(title=title,desc=desc,post_by=post_by)
        save_list.save()
        return HttpResponseRedirect(reverse('todo'))
    context = {
        'group': group,
    }
    return HttpResponse(template.render(context,request))

# EDIT A TO DO LIST PAGE
@login_required(login_url='login')
def edit_to_do(request,id):
    group = request.user.groups.all()[0].name
    list = ToDoList.objects.get(id=id)
    template = loader.get_template('edit_to_do.html')
    if request.method == 'POST':
        list.title = request.POST['title']
        list.desc = request.POST['desc']
        isCompleted = request.POST.get('iscompleted',False)
        if isCompleted == 'iscompleted':
            isCompleted = True
        print(isCompleted)
        list.iscompleted = isCompleted
        list.save()
        return HttpResponseRedirect(reverse('todo'))
    context = {
        'list':list,
        'group': group,
    }    
    return HttpResponse(template.render(context,request))

# DELETE A TO DO LIST PAGE
@login_required(login_url='login')
def delete_to_do(request,id):
    list = ToDoList.objects.get(id=id)
    list.delete()
    return HttpResponseRedirect(reverse('todo'))

# REGISTER A USER PAGE
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    group = Group.objects.get(name='customer')
    template = loader.get_template('register.html')
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        phone = request.POST['phone']
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user.groups.add(group)
            Profile.objects.create(
                user=user,
                username=username,
                email=email,
                phone=phone, 
                )
            messages.success(request,'Account was created for ' + username)
            return HttpResponseRedirect(reverse('login'))
    context = {
        'form':form
    }
    return HttpResponse(template.render(context,request))

# LOGIN A USER PAGE
@unauthenticated_user
def login_User(request):
    template = loader.get_template('login.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        print(user)
        if user is not None:
            if user.profile.image == None:
                user.profile.image = 'profile_picture.png'
                user.profile.save()
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.info(request,"Username or Password is Incorrect")    
    context = {}
    return HttpResponse(template.render(context,request))

# LOGOUT A USER
def logout_User(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

# USER PAGE
@login_required(login_url='login')
def user_page(request):
    profiles = Profile.objects.all()
    cus = request.user
    group = cus.groups.all()[0].name
    user = request.user.profile 
    notes = cus.profile.todolist_set.all()
    completed_notes = cus.profile.todolist_set.filter(iscompleted=True)
    notcompleted_notes = cus.profile.todolist_set.filter(iscompleted=False)
    total_completed = completed_notes.count()
    total_notcompleted = notcompleted_notes.count()
    total_notes = notes.count()
    template = loader.get_template('user_page.html')
    context = {
        'user':user,
        'cus': cus,
        'total_notes': total_notes,
        'profiles': profiles,
        'group': group,
        'total_completed': total_completed,
        'total_notcompleted': total_notcompleted,
    }
    return HttpResponse(template.render(context,request))

# USER SETTINGS PAGE
@login_required(login_url='login')
def acc_settings(request):
    user = request.user
    profile = Profile.objects.all()
    group = user.groups.all()[0].name
    template = loader.get_template('acc_settings.html')
    if request.method == 'POST':
        user.profile.username = request.POST['username']
        user.username = request.POST['username']
        user.profile.email = request.POST['email']
        user.email = request.POST['email']
        user.profile.phone = request.POST['phone']
        user.profile.image = request.FILES['image']
        user.profile.save()
        user.save()
        return HttpResponseRedirect(reverse('user_page'))
    context = {
        'user':user,
        'profile': profile,
        'group': group,
    }
    return HttpResponse(template.render(context,request))

@login_required(login_url='login')
@admin_only
def all_customers(request):
    group = request.user.groups.all()[0].name
    profiles = Profile.objects.all()
    template = loader.get_template('all_customers.html')
    context = {
        'profiles': profiles,
        'group': group,
    }
    return HttpResponse(template.render(context,request))

@login_required(login_url='login')
@admin_only
def customer(request,name):
    group = request.user.groups.all()[0].name
    profiles = Profile.objects.get(username=name)
    notes = profiles.todolist_set.all()
    total_notes = notes.count()
    template = loader.get_template('customer.html')
    context = {
        'profiles':profiles,
        'total_notes':total_notes,
        'notes': notes,
        'group': group,
    }
    return HttpResponse(template.render(context,request))
