#coding:utf-8
from django.db import models

# Create your models here.


class AppComment(models.Model):
    app_content = models.TextField(u'意见')

    class Meta:
        verbose_name = u'意见反馈'
        verbose_name_plural = u'意见反馈'


class VersionManager(models.Model):
    version_id = models.AutoField(primary_key=True, auto_created=True)
    version_code = models.CharField(u'版本号',max_length=30)
    version_name = models.CharField(u'版本名称',max_length=30)
    description = models.TextField(u'描述')
    download_url = models.URLField(u'apk下载地址')

    class Meta:
        verbose_name = u'版本管理'
        verbose_name_plural = u'版本管理'
