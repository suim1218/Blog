"""blogsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from blog import views,views_if

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index', views.index),
    url(r'^$', views.index),
    url(r'^login_action/$', views.login_action),
    url(r'^articles/$', views.articles),
    url(r'^articles/(?P<article_id>[0-9]+)$', views.article_details, name="article_details"),
    url(r'^search_name/$', views.search_name),
    url(r'^logout/$', views.logout),
    url(r'^edit_page/$', views.edit_page),
    url(r'^edit/action/$', views.edit_action),
    url(r'^delete/(?P<article_id>[0-9]+)/$', views.article_delete, name="delete"),
    url(r'^modify_page/(?P<article_id>[0-9]+)/$', views.modify_page,name="modify_page"),
    url(r'^modify/action/(?P<article_id>[0-9]+)/$', views.modify_action, name="modify_action"),
    url(r'^api/', include('blog.urls', namespace="blog")),
    # url(r'^api/add_article', views_if.add_article)
    url(r'^accounts/login/$', views.index),
]
