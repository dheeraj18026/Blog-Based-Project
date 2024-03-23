from django.shortcuts import render,HttpResponseRedirect
from blog.forms import SignUpForm,LoginForm,PostForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login,logout,authenticate
from blog.models import Post
from django.contrib.auth.models import Group
from django.core.cache import cache


# Home
def home(request):
    posts = Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts})

# About 
def about(request):
    return render(request,'blog/about.html')

# Contact
def contact(request):
    return render(request,'blog/contact.html')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        ip = request.session.get("ip")
        ct = cache.get('count', version=user.pk)
        return render(request,'blog/dashboard.html',{'posts':posts, 'full_name':full_name,
        'groups':gps, 'ct':ct,'ip':ip})     
    else:
        return HttpResponseRedirect('/login/')

# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Sign_Up
def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
            messages.success(request,'Congratulation !!!  You have become an Author.')
    else:
        form = SignUpForm()
    return render(request,'blog/signup.html',{'form':form})

# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    auth_login(request,user)
                    messages.success(request,' Hello... this is your Dashboard !!!')
                    return HttpResponseRedirect('/dashboard/')
        else :
            fm = LoginForm()
        return render(request, 'blog/login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/dashboard/')  

def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                post = Post(title=title,desc=desc)
                post.save()
                form = PostForm()
                messages.success(request,' Blog added successfully !!!')
                return HttpResponseRedirect('/add_post/')
        else:
            form = PostForm()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def update_post(request,id):
    if request.user.is_authenticated: 
        if request.method=="POST":
            data = Post.objects.get(pk=id)
            form =  PostForm(request.POST, instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,'Blog saved successfully !!!')
                return HttpResponseRedirect('/dashboard/')
        else:
            data = Post.objects.get(pk=id)
            form = PostForm(instance=data)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = Post.objects.get(pk=id)
            data.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')