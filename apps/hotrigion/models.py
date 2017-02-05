#! -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from project_lib.generate_id import generate_id


class GeoMongoDBModel(models.Model):

    collection_name = models.CharField(verbose_name=u'集合名稱', max_length=100)
    db_id = models.CharField(verbose_name=u'資料庫id', max_length=100, unique=True, default=generate_id())
    max_latitude = models.FloatField(verbose_name=u'最大緯度', default=0)
    min_latitude = models.FloatField(verbose_name=u'最小緯度', default=0)
    max_longitude = models.FloatField(verbose_name=u'最大經度', default=0)
    min_longitude = models.FloatField(verbose_name=u'最小經度', default=0)
    is_modified = models.BooleanField(verbose_name=u'范围已知', default=False)

    class Meta:
        verbose_name = u'資料庫'
        verbose_name_plural = u'資料庫類'

    def __unicode__(self):
        return '%s' %self.collection_name