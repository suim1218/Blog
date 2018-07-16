from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from blog.models import Article
from django.contrib import auth
import base64
from django.contrib import auth as django_auth


# 用户认证
def user_auth(request):
    get_http_auth = request.META.get('HTTP_AUTHORIZATION', b'')
    auth = get_http_auth.split()
    try:
        auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(':')
    except IndexError:
        return "null"
    userid, password = auth_parts[0], auth_parts[2]
    user = django_auth.authenticate(username=userid, password=password)
    if user is not None and user.is_active:
        django_auth.login(request, user)
        return "success"
    else:
        return "fail"


# 登录接口
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == '' or password == '':
            return JsonResponse({'status': 10021, 'message': 'parameter null'})
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            return JsonResponse({'status': 200, 'message': 'login success'})
        else:
            return JsonResponse({'status': 10023, 'message': 'username or password error'})
    else:
        return JsonResponse({'status': 10024, 'message': 'Request error'})


# 添加文章接口
def add_article(request):
    if request.method == 'POST':
        auth_result = user_auth(request)
        if auth_result == "null":
            return JsonResponse({'status': 10011, 'message': 'user auth null'})

        if auth_result == "fail":
            return JsonResponse({'status': 10012, 'message': 'user auth fail'})
        id = request.POST.get('id', '')
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        content = request.POST.get('content', '')
        print(id, title, description, content)

        if id == '' or title == '' or description == '' or content == '':
            return JsonResponse({'status': 10021, 'message': 'parameter null'})
        # if len(title) > 10:
        #     return JsonResponse({'status': 10023, 'message': 'title too long'})
        # if len(description) > 20:
        #     return JsonResponse({'status': 10023, 'message': 'description too long'})
        # if len(content) > 30:
        #     return JsonResponse({'status': 10023, 'message': 'content too long'})
        result = Article.objects.filter(id=id)
        if result:
            return JsonResponse({'status': 10023, 'message': 'Article id already exists'})
        try:
            Article.objects.create(id=id, title=title, description=description, content=content)
        except BaseException:
            return JsonResponse({'status': 10025, 'message': '添加文章失败'})

        return JsonResponse({'status': 200, 'message': 'add article success'})
    else:
        return JsonResponse({'status': 10024, 'message': 'Request error'})


# 修改文章接口
def modify_article(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        content = request.POST.get('content', '')

        if id == '' or title == '' or description == '' or content == '':
            return JsonResponse({'status': 10021, 'message': 'parameter null'})
        # if len(title) > 10:
        #     return JsonResponse({'status': 10023, 'message': 'title too long'})
        # if len(description) > 20:
        #     return JsonResponse({'status': 10023, 'message': 'description too long'})
        # if len(content) > 30:
        #     return JsonResponse({'status': 10023, 'message': 'content too long'})
        result = Article.objects.filter(id=id)
        if not result:
            return JsonResponse({'status': 10023, 'message': 'Article not exist'})
        try:
            Article.objects.filter(id=id).update(id=id, title=title, description=description, content=content)
        except BaseException:
            return JsonResponse({'status': 10025, 'message': '修改文章失败'})

        return JsonResponse({'status': 200, 'message': 'modify article success'})
    else:
        return JsonResponse({'status': 10024, 'message': 'Request error'})


# 删除文章接口
def delete_article(request):
    if request.method == 'POST':
        id = request.POST.get('id', '')
        result = Article.objects.filter(id=id)
        if not result:
            return JsonResponse({'status': 10023, 'message': 'Article not exist'})
        try:
            Article.objects.filter(id=id).delete()
        except BaseException:
            return JsonResponse({'status': 10025, 'message': '删除文章失败'})

        return JsonResponse({'status': 200, 'message': 'delete article success'})
    else:
        return JsonResponse({'status': 10024, 'message': 'Request error'})


# 查询文章接口
def get_article(request):
    title = request.GET.get("name", "")  #
    if title == '':
        return JsonResponse({'status': 10021, 'message': 'parameter null'})

    if title != '':
        datas = []
        articles = Article.objects.filter(title__contains=title)
        if articles:
            for r in articles:
                article = {}
                article['title'] = r.title
                article['description'] = r.description
                article['content'] = r.content
                # article['title'] = r.title
                datas.append(article)
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
