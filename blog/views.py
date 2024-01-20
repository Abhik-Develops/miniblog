from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post, FeedBack
from django.contrib.auth.models import Group

# Create your views here.

#home
def home(request):
    posts = Post.objects.all()
    return render(request,'blog/home.html',{'posts':posts, 'home': 'active'})

#about
def about(request):
    return render(request, 'blog/about.html', {'about': 'active'})

#contact
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email'] 
        address = request.POST['address'] 
        msg = request.POST['name'] 
        obj = FeedBack(name=name, email=email, address=address, msg=msg)
        obj.save()
        return redirect("/thankyou")

    return render(request, 'blog/contact.html', {'contact': 'active'})

#dashboard 
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts':posts, 'fullname':full_name, 'groups':gps, 'dashboard': 'active'})
    return redirect('/login/')

#signup
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Congratulations! You have become an Author')
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()    
    return render(request, 'blog/signup.html', {'form':form, 'signup': 'active'})

#login
def user_login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in sucessfully')
                return redirect('/dashboard/')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form':form, 'login': 'active'})
        

#logout 
def user_logout(request):
    logout(request)
    return redirect('/')

#Add new post
def add_post(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            desc = form.cleaned_data['desc']
            post = Post(title=title, desc=desc)
            post.save()
            return redirect('/dashboard/')
    else:
        form = PostForm()
    return render(request, 'blog/addpost.html', {'form':form})

#Update post
def update_post(request, id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.method == 'POST':
        pi = Post.objects.get(pk=id)
        form = PostForm(request.POST, instance=pi)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/')
    else:
        pi = Post.objects.get(pk=id)
        form = PostForm(instance=pi)
    return render(request, 'blog/updatepost.html', {'form':form})

#delete post
def delete_post(request, id):
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.method == 'POST':
        pi = Post.objects.get(pk=id)
        pi.delete()
        return redirect('/dashboard/')


def thankyou(request):
    return render(request, 'blog/thankyou.html')