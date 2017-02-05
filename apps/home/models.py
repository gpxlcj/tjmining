#! -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_markdown.models import MarkdownField
from project_lib.generate_id import generate_id
from settings.origin import MEDIA_ROOT
from django.utils.encoding import force_unicode



class ImageModel(models.Model):

    image = models.ImageField(
        verbose_name=u'封面图片',
        upload_to=MEDIA_ROOT+'/img/',
        height_field= 'height',
        width_field= 'width',
    )
    height = models.PositiveIntegerField(default=400, verbose_name=u'图片高度')
    width = models.PositiveIntegerField(default=700, verbose_name=u'图片宽度')


    class Meta:
        verbose_name = u''
        verbose_name_plural = u'图片类'


    def __unicode__(self):
        return '%d_%s' % (self.id, force_unicode(self.image))


class BlogModel(models.Model):
    '''
    type: Model
    name: Blog Class
    '''

    title = models.CharField(verbose_name=u'标题', max_length=200, blank=False, default=u'Nothing')
    content = MarkdownField(verbose_name=u'正文', blank=True, max_length=30000)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now=True)
    author = models.CharField(verbose_name=u'作者', max_length=50, default=u'无名氏')
    blog_id = models.CharField(verbose_name=u'博客id', max_length=100, unique=True, default=generate_id())
    cover = models.OneToOneField(ImageModel, verbose_name=u'封面图片', blank=True)
    subtitle = models.CharField(verbose_name=u'副标题', max_length=100, blank=True)

    class Meta:
        verbose_name = u'博客'
        verbose_name_plural = u'博客类'

    def __unicode__(self):
        return '%s_%s' %(self.title, self.author)




class CommentModel(models.Model):

    content = models.TextField(verbose_name=u'內容', max_length=400, blank=True)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now=True)
    author = models.CharField(verbose_name=u'评论者名称', max_length=200)
    comment_id = models.CharField(verbose_name=u'评论id', max_length=100, unique=True, default=generate_id())
    blog = models.ForeignKey(BlogModel, verbose_name=u'所属博客id', related_query_name=u'blog_comment')
    target_id = models.CharField(verbose_name=u'目标评论id', max_length=100, blank=True)

    class Meta:
        verbose_name = u'评论'
        verbose_name_plural = u'评论类'

    def __unicode__(self):
        return '%s_%s' %(self.author, str(self.create_time))

class BoardCommentModel(models.Model):

    content = models.TextField(verbose_name=u'內容', max_length=400, blank=True)
    comment_id = models.CharField(verbose_name=u'评论', max_length=100, unique=True, default=generate_id())
    target_id = models.CharField(verbose_name=u'目标评论id', max_length=100, blank=True)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now=True)
    author = models.CharField(verbose_name=u'评论者名称', max_length=200)


    class Meta:
        verbose_name = u'留言板'
        verbose_name_plural = u'留言板类'
