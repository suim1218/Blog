from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.contrib import auth
from blog.models import Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

# 首页
def index(request):
    return render(request, 'index.html')


# 登录页
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == '' or password == '':
            return render(request, "index.html", {"error": "username or password null!"})
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 登录
            request.session['user'] = username  # 将 session 信息记录到浏览器
            response = HttpResponseRedirect('/articles/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


# 文章列表页
@login_required
def articles(request):
    article_list = Article.objects.all()
    username = request.session.get('user', '')
    paginator = Paginator(article_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "articles.html", {"user": username, "articles": contacts})


# 文章详情页
@login_required
def article_details(request, article_id):
    article = Article.objects.get(pk=article_id)
    article_title = article.title
    article_description = article.description
    article_content = article.content
    article_publish = article.date_publish
    return render(request, "article_details.html",
                  {"article_title": article_title, "article_description": article_description,
                   "article_content": article_content, "article_publish": article_publish, "article_id": article_id})


# 搜索文章标题
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    article_list = Article.objects.filter(title__contains=search_name)
    # return render(request, "articles.html", {"user": username, "articles": article_list})
    paginator = Paginator(article_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "articles.html", {"user": username, "articles": contacts})


# 退出
@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponseRedirect('/index/')
    return response


# 文章编辑页
@login_required
def edit_page(request):
    return render(request, 'edit_page.html')


# 新增文章
@login_required
def edit_action(request):
    title = request.POST.get('title', 'title')
    description = request.POST.get('description', 'title')
    content = request.POST.get('content', 'content')
    if title == '' or description == '' or content == '':
        return render(request, "edit_page.html", {"error": "title or description or content null!"})
    else:
        Article.objects.create(title=title, description=description, content=content)
        response = HttpResponseRedirect('/articles/')
        return response


# 删除文章
@login_required
def article_delete(request, article_id):
    Article.objects.filter(id=article_id).delete()
    response = HttpResponseRedirect('/articles/')
    return response


# 获取到修改页面内容
@login_required
def modify_page(request, article_id):
    article = Article.objects.get(pk=article_id)
    article_title = article.title
    article_description = article.description
    article_content = article.content
    article_id = article.id
    # if article_title == '' or article_content == '':
    #     return render(request, "edit_page.html", {"error": "title or content null!"})
    return render(request, 'modify_page.html',
                  {"article_title": article_title, "article_description": article_description,
                   "article_content": article_content, "article_id": article_id})


# 修改成功
@login_required
def modify_action(request, article_id):
    article = Article.objects.get(pk=article_id)
    title = request.POST.get('title', '')
    description = request.POST.get('description', '')
    content = request.POST.get('content', '')
    # print(title, description, content)
    article.title = title
    article.description = description
    article.content = content
    article.save()
    response = HttpResponseRedirect('/articles/')
    return response
