from django.test import TestCase
from .models import Article
from datetime import datetime

from django.contrib.auth.models import User


# Create your tests here.

class ModelTest(TestCase):
    '''模型测试'''

    def setUp(self):
        Article.objects.create(id=1, title='title', description='description', content='content')
        pass

    def test_article_models(self):
        '''文章表'''
        pass
        result = Article.objects.get(id=1)
        self.assertEqual(result.title, "title")


class IndexPageTest(TestCase):
    '''测试index登录首页'''

    def test_index_page_renders_index_template(self):
        ''' 断言是否用给定的index.html模版响应'''
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class LogoutTest(TestCase):
    '''测试index登录首页'''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_logout(self):
        ''' 断言是否用给定的index.html模版响应'''
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)


class LoginActionTest(TestCase):
    ''' 测试登录动作'''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_add_user(self):
        ''' 测试添加用户 '''
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        ''' 用户名密码为空 '''
        response = self.client.post('/login_action/', {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password null!", response.content)

    def test_login_action_username_password_error(self):
        ''' 用户名密码错误 '''
        response = self.client.post('/login_action/', {'username': 'abc', 'password': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        ''' 登录成功 '''
        response = self.client.post('/login_action/', data={'username': 'admin', 'password': 'admin123456'})
        self.assertEqual(response.status_code, 302)


class AddArticleTest(TestCase):
    ''' 添加文章 '''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_add_article_success(self):
        ''' 测试添加文章 '''
        response = self.client.post('/edit/action/',
                                    data={'title': "this is title", "description": "this is description",
                                          "content": "this is conten"})
        self.assertEqual(response.status_code, 302)

    def test_article_title_null(self):
        ''' 测试添加文章标题为空 '''
        response = self.client.post('/edit/action/', data={'title': "", "description": "this is description",
                                                           "content": "this is conten"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"title or description or content null!", response.content)


class ModifyArticleTest(TestCase):
    ''' 修改文章 '''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        login_user = {'username': 'admin', 'password': 'admin123456'}
        Article.objects.create(id=1, title='this is title', description='this is description',
                               content='this is content')
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_modify_article_success(self):
        ''' 测试修改文章 '''
        response = self.client.post('/modify/action/1/',
                                    data={'title': "title is change", "description": "description is change",
                                          "content": "conten is change"})
        self.assertEqual(response.status_code, 302)


class DeleteArticleTest(TestCase):
    ''' 删除文章 '''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        login_user = {'username': 'admin', 'password': 'admin123456'}
        Article.objects.create(id=1, title='this is title', description='this is description',
                               content='this is content')
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_delete_article_success(self):
        ''' 测试修改文章 '''
        response = self.client.get('/delete/1/')
        self.assertEqual(response.status_code, 302)


class GetArticleTest(TestCase):
    ''' 查询文章 '''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        login_user = {'username': 'admin', 'password': 'admin123456'}
        Article.objects.create(id=1, title='wangyang', description='this is description', content='this is content')
        # Article.objects.create(id=2, title='second title', description='second description2', content='second content2')

        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_search_article_success(self):
        ''' 测试搜索文章 '''
        response = self.client.get('/search_name/?name=wangyang')
        # print(response.content)
        self.assertIn(b"wangyang", response.content)
        # self.assertEqual(response.status_code, 302)
