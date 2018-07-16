from django.conf.urls import url
from . import views_if

urlpatterns = [
    # ex : /api/add_article/
    url(r'^add_article', views_if.add_article, name='add_article'),
    url(r'^modify_article/$', views_if.modify_article, name='modify_article'),
    url(r'^delete_article/$', views_if.delete_article, name='delete_article'),
    url(r'^get_article/$', views_if.get_article, name='get_article'),
    url(r'^login_action/$', views_if.login_action, name='login_action'),

]