#! -*- coding:utf-8 -*-
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'blog/(?P<blog_id>[0-9]*)/$', views.blog, name='blog_view'),
    url(r'index/$', views.index),
    url(r'about/$', views.about),
    url(r'contact/$', views.contact),

]


