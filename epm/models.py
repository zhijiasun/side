#coding:utf-8
import os
from django.db import models
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.storage import default_storage
from epm.utils import *

# Create your models here.
class party(models.Model):
    party_id = models.AutoField(primary_key=True,auto_created=True)
    party_name = models.CharField(u'党组织名称',max_length=100)
    secretary_name = models.CharField(u'书记姓名',max_length = 50)
    secretary_phone = models.CharField(u'书记电话',max_length = 30)
    member_number = models.IntegerField(u'党员人数')
    responsible_name = models.CharField(u'党务负责人姓名',max_length=50)
    responsible_phone = models.IntegerField(u'党务负责人电话')
    contact_info = models.CharField(u'联系方式',max_length=300)

    class Meta:
        verbose_name = u'党支部信息'
        verbose_name_plural = u'党支部信息'


    def __unicode__(self):
        return self.party_name

    # def related_enter(self):
    #     enters = enterprise.objects.filter(party_status=self)
    #     print enters
    #     return enters

class enterprise(models.Model):

    enter_id = models.AutoField(primary_key=True,auto_created=True)
    enter_name = models.CharField(u'企业名称',max_length=50)
    enter_address = models.CharField(u'企业地址',max_length=300)
    enter_nature = models.IntegerField(u'单位属性',default=1,choices=NATURE_CHOICES)
    industry_type = models.IntegerField(u'行业类别',default=1,choices=INDUSTRY_TYPE)
    industry_nature = models.IntegerField(u'企业类型',default=1,choices=INDUSTRY_NATURE)
    enter_scale = models.IntegerField(u'企业规模',default=1,choices=ENTER_SCALE)
    total_assets = models.IntegerField(u'资产总额',default=1,choices=TOTAL_ASSETS)
    # party_status = models.IntegerField(u'党组织情况',default=0,choices=PARTY_STATUS)
    party_name = models.ForeignKey(party,verbose_name=u'所属党组织')
    legal_person = models.CharField(u'法人姓名',max_length=50)
    legal_email = models.EmailField(u'法人邮箱',max_length=50)
    enter_email = models.EmailField(u'企业邮箱',max_length=50)
    legal_phone = models.CharField(u'负责人手机',max_length=50)
    fixed_phone = models.CharField(u'固定电话',max_length=50)

    class Meta:
        verbose_name = u'企业信息'
        verbose_name_plural = u'企业信息'


    def __unicode__(self):
        return self.enter_name


class member(models.Model):
    member_name = models.CharField(verbose_name=u'党员姓名',max_length=80)
    member_gender = models.IntegerField(u'性别',default=1,choices=((1,u'男'),(1,u'女')))
    member_nation = models.IntegerField(u'民族',default=1,choices=((1,u'汉族'),(2,u'藏族')))
    member_education = models.IntegerField(u'学历',default=1,choices=((1,u'本科'),(2,u'研究生')))
    member_birth = models.DateField(u'出生日期')
    member_worktime = models.DateField(u'参加工作时间')
    formal_member_time = models.DateField(u'转正时间')
    now_party_time = models.DateField(u'转入现组织时间')
    birth_address = models.CharField(u'出生地',max_length=100)
    home_address = models.CharField(u'家庭住址',max_length=100)
    living_address = models.CharField(u'现居住地址',max_length=100)
    member_phone = models.CharField(u'手机号',max_length=11)
    member_email = models.EmailField(u'电子邮箱',max_length=50)
    qq = models.CharField(u'QQ号',max_length=15)
    weixin = models.CharField(u'微信号',max_length=20)
    school = models.CharField(u'毕业院校',max_length=80)
    id_card = models.CharField(u'身份证号',max_length=30)
    member_enter = models.ForeignKey(enterprise,verbose_name=u'隶属企业')

    class Meta:
        verbose_name = u'党员信息'
        verbose_name_plural = u'党员信息'

    def __unicode__(self):
        return self.member_name


class Jason(models.Model):
    party_id = models.AutoField(primary_key=True,auto_created=True)
    party_name = models.CharField(u'党支部名称',max_length=100)
    member_number = models.IntegerField(u'党员人数')
    contact_info = models.CharField(u'联系方式',max_length=300)
    attachment = models.FileField(upload_to='upload/',blank=True)

    class Meta:
        verbose_name = u'Jason'
        verbose_name_plural = u'Jason'


    def __unicode__(self):
        return self.party_name



class Category(models.Model):
    name = models.CharField(u"名称", max_length=64)
    parent = models.ForeignKey('self', verbose_name=u'父类别', related_name='children', null=True, blank=True)

    class Meta:
        verbose_name=u'类别'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(u"标题", max_length=200)
    date = models.DateField(u"发布时间")
    content = models.TextField(u"内容", null=True, blank=True)
    attachment = models.FileField(u'附件',upload_to='/home/jasonsun/svn_repo/',blank=True)
    categories = models.ManyToManyField('Category', null=True, blank=True)

    class Meta:
        verbose_name=u'文章'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
