import math

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .forms import *
from .models import *

def index(req):
    return render(req, 'index.html')

def user_login(req):
    if req.user.is_authenticated:
        return HttpResponse(status = 404)
    if req.method == 'GET':
        return login_form(req)
    if req.method == 'POST':
        return login_post(req)
    return HttpResponse(status = 404)

def login_form(req):
    return render(req, 'auth/login.html', {'form': LoginForm(),})

def login_post(req):
    form = LoginForm(req.POST)
    if not form.is_valid():
        return HttpResponse(status = 400)

    user = authenticate(
        username = form.cleaned_data['username'],
        password = form.cleaned_data['password'],
    )

    if user:
        # login success
        login(req, user)
        return redirect('index')
    else:
        # login failed
        return HttpResponse(status = 401)

def register(req):
    if req.user.is_authenticated:
        return HttpResponse(status = 404)
    if req.method == 'GET':
        return register_form(req)
    if req.method == 'POST':
        return register_post(req)
    return HttpResponse(status = 404)

def register_form(req):
    return render(req, 'auth/register.html', {'form': RegisterForm(),})

def register_post(req):
    form = RegisterForm(req.POST)
    if not form.is_valid():
        return HttpResponse(status = 400)

    user = User.objects.create_user(
        username = form.cleaned_data['username'],
        password = form.cleaned_data['password'],
        first_name = form.cleaned_data['first_name'],
        last_name = form.cleaned_data['last_name'],
    )
    user.save()

    return redirect('login')

def user_logout(req):
    logout(req)
    return redirect('index')

def get_article_list(req, page_num):
    article_list = Article.objects.all().filter(is_deleted = False).order_by('-id')

    COUNT = 20
    start_index = (page_num - 1) * COUNT
    end_index = page_num * COUNT

    page_count = math.ceil(len(article_list) / COUNT)

    return render(req, 'articles/index.html', {
        'page': page_num,
        'articles': article_list[start_index:end_index],
        'has_prev': page_num > 1,
        'has_next': page_num < page_count,
    })

def get_article(req, article_id):
    article = get_object_or_404(Article, id = article_id, is_deleted = False)

    return render(req, 'articles/details.html', {
        'article': article,
    })

def compose_article(req):
    if not req.user.is_authenticated:
        return HttpResponse(status = 404)
    if req.method == 'GET':
        return compose_article_form(req)
    if req.method == 'POST':
        return compose_article_post(req)
    return HttpResponse(status = 404)

def compose_article_form(req):
    return render(req, 'articles/compose.html', {'form': ArticleForm(),})

def compose_article_post(req):
    pass

def edit_article(req):
    pass

def delete_article(req):
    pass