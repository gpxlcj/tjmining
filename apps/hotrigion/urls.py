#! -*- coding:utf-8 -*-
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'heatmap/$', views.heatmap),
    url(r'get_hot_region/$', views.get_hot_region),
    url(r'heatmapbygrid/$', views.heatmap_by_grid),
    url(r'show_hot_region/$', views.show_hot_region),
    url(r'sample_show/$', views.sample_show),

]


