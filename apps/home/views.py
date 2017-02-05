#! -*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseForbidden
from models import BlogModel, CommentModel
from datetime import datetime
from project_lib.build_json import render_to_json, return_status
import pymongo


def blog(request, blog_id):
    if request.method == 'GET':
        blog = get_object_or_404(BlogModel, blog_id=blog_id)
        title_name = blog.title
        current_time = datetime.now()
        content = str(blog.content)
        cover_url = blog.cover.image.url
        print(cover_url)
        cover_url = '/media/img/' + str(cover_url).split('/')[-1]

        temp_content = str()
        last_num = 0
        for i in range(0, len(content)):
            if content[i] == '\n':
                temp_content += content[last_num:i-1]
                temp_content += '\\n'
                last_num = i+1
        else:
            temp_content += content[last_num:len(content)]
        content = temp_content
        page_title = blog.title.title()

        return render_to_response('blog/blog.html', locals())
    else:
        return Http404("the blog does not exist")


def about(request):
    if request.method == 'GET':
        cover_url = '/static/img/home-bg.png'
        current_time = datetime.now()
        title_name = u'about me'
        page_title = u'About Me'

        return render_to_response('blog/about.html', locals())
    else:
        return Http404

def contact(request):
    if request.method == 'GET':
        return render_to_response('blog/contact.html', locals())
    else:
        return Http404



def index(request):
    if request.method == 'GET':
        cover_url = '/static/img/home-bg.png'
        blog_list = BlogModel.objects.all().order_by('create_time')
        blog_list = blog_list[0:10]
        current_time = datetime.now()
        title_name = u'台灣橘子洲賣很貴的橘子'
        page_title = u'台灣橘子洲賣橘子'
        return render_to_response('blog/index.html', locals())
    else:
        return Http404
