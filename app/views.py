from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def index(request):
    blog = Blog.objects.all().order_by('-id')
    news = News.objects.all().order_by('-id')
    context = {
        'blogs': blog,
        'news': news,
    }
    return render(request,'index.html',context)

def blog_details(request,blog_id):
    blog = Blog.objects.get(id= blog_id)
    
    context = {
        'blog':blog,
        
    }
    return render(request,'blog_details.html',context)



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'username already exists')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'email already exists')
            else:
                user = User.objects.create(username=username, email=email, is_staff=True)
                user.set_password(password)  
                user.save()

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request=request, user=user)
                    messages.success(request, "Congrats! You are successfully logged in.")
                    return redirect('dashboard')
        else:
            messages.warning(request, 'Password does not match')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user  = authenticate(username = username, password = password)
        if user is not None:
            login(request = request, user=user)
            return redirect('dashboard')
        else:
            messages.warning(request, message='username or password are incorrect')

    return render(request,'login_view.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard(request):
    blogs = Blog.objects.filter(user = request.user)
    news = News.objects.filter(user = request.user)
    user_profile = UserProfile.objects.get(user = request.user)
    context = {
        'blogs':blogs,
        'news':news,
        'user_profile':user_profile,
        'blogs_counts':Blog.objects.filter(user= request.user).count(),
        'news_counts':News.objects.filter(user= request.user).count(),

    }
    return render(request,'dashboard.html',context)

def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')  
        content = request.POST.get('content')
        image = request.FILES.get('image')  

        if Blog.objects.filter(title=title).exists():
            messages.warning(request, 'Blog with this title already exists')
        else:
            blog = Blog.objects.create(
                user=request.user,
                title=title,
                content=content,
                image=image,
            )
            blog.save()
            messages.success(request, 'Blog is created successfully')
            return redirect('index')
    
    return render(request, 'add_post.html')
# this is  for the blog to edit 
def edit_blog(request,blog_id):
    blog = Blog.objects.get(id = blog_id)
    if request.method == 'POST':
        blog.title = request.POST['title']
        blog.content = request.POST['content']
        blog.image = request.FILES['image']
        blog.save()
        messages.success(request,'Blog updated successfully')
        return redirect('dashboard')
    context = {
        'blog':blog
    }
    return render(request,'edit_blog.html',context)


def delete_blog(request,blog_id):
    blog = Blog.objects.get(id = blog_id)
    if request.method == 'POST':
        blog.delete()
        messages.success(request,'Your blog deleted successfully')
        return redirect('dashboard')
    return render(request,'delete_blog.html',{'blog':blog})

def add_news(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES['image']

        if News.objects.filter(title = title).exists():
            messages.warning(request,message='News is already uploaded')
        else:
            news = News.objects.create(
                user = request.user,
                title = title,
                content = content,
                image = image
            )
            news.save()
            messages.success(request,message='news is successfully created')
            return redirect('index')
    return render(request,'add_news.html')

def news_details(request,news_id):
    news = News.objects.get(id = news_id)

    return render(request,'news_details.html',{'news':news})

def edit_news(request,news_id):
    news = News.objects.get(id = news_id)
    if request.method == 'POST':
        news.title = request.POST['title']
        news.content = request.POST['content']
        news.image = request.FILES['image']
        news.save()
        messages.success(request,'Blog updated successfully')
        return redirect('dashboard')
    context = {
        'blog':news
    }
    return render(request,'edit_blog.html',context)

def delete_news(request,news_id):
    news = News.objects.get(id = news_id)
    if request.method == 'POST':
        news.delete()
        messages.success(request,'Your blog deleted successfully')
        return redirect('dashboard')
    return render(request,'delete_blog.html',{'news':news})

def user_profile(request,user_profile_id):
    user_profile = UserProfile.objects.get(id = user_profile_id)
    context = {
        'user_profile':user_profile
    }
    return render(request,'user_profile.html',context)

def edit_profile(request):
    user_profile = UserProfile.objects.get(user = request.user)
    if request.method == 'POST':
        user_profile.username = request.POST['name']
        user_profile.bio = request.POST['bio']
        user_profile.address = request.POST['address']
        user_profile.profile_image = request.FILES.get('profile_image','')
        if user_profile.profile_image:
            user_profile.save()
        messages.success(request,message='user is successfully updated')
        return redirect('dashboard')
    
    context = {
        'user_profile':user_profile,
       
    }
    return render(request,'edit_profile.html',context)


from django.db.models import Q
def filter_view(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        blogs = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)) # Filter blogs by title containing the search query
    else:
        blogs = Blog.objects.all()  # If no query, return all blogs
    return render(request, 'filter.html', {'blogs': blogs, 'query': query})


def search_result(request):
    query = request.GET.get('q', '')
    if query:
        blogs = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        news = News.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        blogs = Blog.objects.all()
        news = News.objects.all()
    
    # Render the 'index' template with the context
    return render(request, 'index.html', {'blogs': blogs, 'news':news, 'query': query})
