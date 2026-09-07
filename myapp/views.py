from django.shortcuts import render, get_object_or_404,redirect
from .models import Categories, Article,About,Comment
from .form import RegisterForm,LoginForm,CategoryForm,ArticleForm,AddUserForm,EditUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate ,login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect


def home(request):
    search = request.GET.get('search')

    posts = Article.objects.filter(
        is_feature=True
    ).order_by('-created_at')

    if search:
        posts = posts.filter(
            Q(title__icontains=search) | Q(short_description__icontains=search)
        )
        print(posts)

    paginator=Paginator(posts,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    return render(request, 'home.html', {
        'page_obj':page_obj,
        'posts': page_obj,
    })

def category_posts(request, id):

    category = get_object_or_404(
        Categories,
        id=id
    )

    posts = category.articles.all()

    context = {
        'category': category,
        'posts': posts
    }

    return render(request, 'category_post.html', context)


def post_detail(request, slug):

    post = get_object_or_404(
        Article,
        slug=slug,
        status='Published'
    )

    if request.method=='POST':
        comment=Comment()
        comment.user = request.user
        comment.article =post
        comment.comment=request.POST['comment']
        comment.save()
        return HttpResponseRedirect (request.path_info)
    comments=Comment.objects.filter(article=post)
    comment_count=comments.count()
    print(comments)

    context = {
        'post': post,
        'comments':comments,
        'comment_count':comment_count
    }

    return render(request, 'post_detail.html', context)


def about(request):
    detail = About.objects.latest('created_at')

    return render(request, 'about.html', {'detail': detail})


def search(request):
    return render(request,'search.html')

def register(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User Successfully Registered")
            return redirect('login_page')
    else:
        form=RegisterForm()
    return render(request,'register.html',{'form':form})


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages

def login_page(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            messages.success(
                request,
                "You have logged in successfully!"
            )

            return redirect('dashboard')

        messages.error(
            request,
            "Invalid username or password"
        )

    else:
        form = AuthenticationForm()

    return render(
        request,
        'login.html',
        {'form': form}
    )
# def login_page(request):
#     if request.method=='POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username=form.cleaned_data['username']
#             password=form.cleaned_data['password']
#             user =authenticate(request,username=username,password=password)
#             if user is not None:
#                 login(request,user)
#                 messages.success(request,'You have logged in successfully!')
#                 return redirect('home')
#             else:
#                 messages.error(request, "Invalid username or password")
#     else:
#         form = LoginForm()
#     return render(request,'login.html',{'form':form})


def logout_page(request):

    if request.user.is_authenticated:
        logout(request)
        messages.success(
            request,
            "Logged out successfully!"
        )

    return redirect('home')

@login_required(login_url=login_page)
def dashboard(request):
    article_count=Article.objects.count()
    category_count=Categories.objects.count()
    context={
        'article_counts':article_count,'category_counts':category_count
    }
    return render(request,'dashboard/dashboard.html',context)


def categories(request):

    return render(request,'dashboard/categories.html')

def add_category(request):
    if request.method=="POST":
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form =CategoryForm()
  
    return render(request,'dashboard/add_category.html',{'form':form})


def edit_category(request, pk):

    category = get_object_or_404(Categories, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(
            request.POST,
            instance=category
        )

        if form.is_valid():
            form.save()
            return redirect('categories')

    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category
    }

    return render(
        request,
        'dashboard/edit_category.html',
        context
    )


def delete_category(request,pk):
    category=get_object_or_404(Categories,pk=pk)
    category.delete()
    return redirect('categories')

def articles(request):

    if request.user.has_perm('myapp.change_article'):
        articles = Article.objects.all()
    else:
        articles = Article.objects.filter(author=request.user)

    return render(
        request,
        'dashboard/articles.html',
        {'articles': articles}
    )

def add_articles(request):
    if request.method=="POST":
        form=ArticleForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect('articles')
        else:
            print(form.errors) 
    else:
        form =ArticleForm()
  
    return render(request,'dashboard/add_article.html',{'form':form})

def edit_articles(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if not (
        request.user.has_perm('myapp.change_article')
        or article.author == request.user
    ):
        return redirect('articles')

    if request.method == "POST":
        form = ArticleForm(
            request.POST,
            request.FILES,
            instance=article
        )
        if form.is_valid():
            form.save()
            return redirect('articles')
    else:
        form = ArticleForm(instance=article)

    context = {
        'form': form,
        'articles': article
    }

    return render(
        request,
        'dashboard/edit_article.html',
        context
    )
def delete_articles(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if not (request.user.has_perm('myapp.delete_article') or article.author == request.user):
        return redirect('articles')

    article.delete()
    return redirect('articles')
def users(request):
    users=User.objects.all()
    context = {
        'users':users
    }
    return render(request,'dashboard/users.html',context)
def add_user(request):
    if request.method=="POST":
        form=AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            print(form.errors)
    else:
        form = AddUserForm()
    context={
        'form':form
    }
    return render(request,'dashboard/add_user.html',context)


def edit_user(request,pk):
    user=get_object_or_404(User,pk=pk)
    if request.method == "POST":
        form = EditUserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = EditUserForm(instance=user)
    
    context={
        'form':form,
        'user':user    }
        
    return render(request,'dashboard/edit_user.html',context)

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user.is_superuser:
        return redirect('users')

    if user == request.user:
        return redirect('users')

    user.delete()
    return redirect('users')

