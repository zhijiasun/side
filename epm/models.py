#coding:utf-8
import os
import sys
print sys.getdefaultencoding()
from django.db import models
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.storage import default_storage
from epm.utils import *
from django.core.exceptions import ValidationError

# Create your models here.
class party(models.Model):
    party_id = models.AutoField(primary_key=True,auto_created=True)
    party_name = models.CharField(u'党组织名称',max_length=100)
    party_attribute = models.IntegerField(u'党组织属性',default=1,choices=PARTY_ATTRIBUTE)
    member_number = models.IntegerField(u'党员人数')
    secretary_name = models.CharField(u'书记姓名',max_length = 50)
    secretary_phone = models.CharField(u'书记电话',max_length = 30)
    responsible_name = models.CharField(u'党务负责人姓名',max_length=50)
    responsible_phone = models.IntegerField(u'党务负责人电话')
    qq = models.CharField(u'QQ号',max_length=20)
    weixin = models.CharField(u'微信号',max_length=20)
    party_email = models.EmailField(u'党组织邮箱')

    class Meta:
        verbose_name = u'党支部信息'
        verbose_name_plural = u'党支部信息'


    def __unicode__(self):
        return self.party_name

    def related_enter(self):
        # enters = enterprise.objects.filter(party_status=self)
        enters = self.enters.all() # use the realted_name in enterprise
        results = ''
        for enter in enters:
            print type(enter.enter_name)
            print enter.enter_name
            if results:
                results  = results + ';' + enter.enter_name
            else:
                results = results + enter.enter_name
        # enters = [ enter.enter_name for enter in enters ] # !! so strange, can't return chinese correctly

        return results

    related_enter.short_description = u'关联企业'

    def related_members(self):
        members = self.membersAtParty.all()
        return members


class enterprise(models.Model):

    def validate_notnull(obj):
        if not obj:
            print 'aaaa'
            raise ValidationError('related party is NULL')

    enter_id = models.AutoField(primary_key=True,auto_created=True)
    enter_name = models.CharField(u'企业名称',max_length=50)
    enter_address = models.CharField(u'企业地址',max_length=300)
    enter_attribute = models.IntegerField(u'单位属性',default=1,choices=NATURE_CHOICES)
    industry_type = models.IntegerField(u'行业类别',default=1,choices=INDUSTRY_TYPE)
    industry_nature = models.IntegerField(u'企业类型',default=1,choices=INDUSTRY_NATURE)
    enter_scale = models.IntegerField(u'企业规模',default=1,choices=ENTER_SCALE)
    total_assets = models.IntegerField(u'资产总额',default=1,choices=TOTAL_ASSETS)
    legal_person = models.CharField(u'法人姓名',max_length=50)
    legal_email = models.EmailField(u'法人邮箱')
    enter_email = models.EmailField(u'企业邮箱',max_length=50)
    legal_phone = models.CharField(u'负责人手机',max_length=50)
    fixed_phone = models.CharField(u'固定电话',max_length=50)
    """
    blank=True, null=True can make ForeignKey is optional.
    1.
    we also can create an default party which means NULL and the id is 1 at DB, and do as follows:

    def get_default_party():
        return party.objects.get(id=1) 
    related_party = models.ForeignKey(party,verbose_name = u'党组织情况',default=get_default_party())

    2. chagne the behaviour when delete the ForeignKey:
       set the on_delete can change the behaviour
    """
    related_party = models.ForeignKey(party,verbose_name = u'党组织情况',blank=True,null=True,on_delete=models.SET_NULL,related_name='enters')

    class Meta:
        verbose_name = u'企业信息'
        verbose_name_plural = u'企业信息'


    def __unicode__(self):
        return self.enter_name

    def related_party_status(self):
        return PARTY_ATTRIBUTE[self.related_party.party_attribute - 1][1]

    related_party_status.short_description = u'党组织属性'


class member(models.Model):
    member_name = models.CharField(verbose_name=u'党员姓名',max_length=80)
    member_gender = models.IntegerField(u'性别',default=1,choices=((1,u'男'),(2,u'女')))
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
    member_party = models.ForeignKey(party,verbose_name=u'隶属党组织',blank=True,null=True,on_delete=models.SET_NULL,related_name='membersAtParty')
    member_enter = models.ForeignKey(enterprise,verbose_name=u'隶属企业',blank=True,null=True,on_delete=models.SET_NULL,related_name='membersAtEnter')

    class Meta:
        verbose_name = u'党员信息'
        verbose_name_plural = u'党员信息'

    def __unicode__(self):
        return self.member_name

    def member_enter_name(self):
        return self.member_enter.enter_name

    member_enter_name.short_description = u'隶属企业'

    def member_party_name(self):
        return self.member_party.party_name
    member_party_name.short_description = u'隶属党组织'

class Pioneer(models.Model):
    pioneer_id = models.AutoField(primary_key=True,auto_created=True)
    pioneer_title = models.CharField(u'标题',max_length=10)
    pioneer_date = models.DateTimeField(u'创建日期',auto_now_add=True)
    pioneer_author = models.CharField(u'作者',max_length=30)
    pioneer_content = models.TextField(u'内容')

    class Meta:
        verbose_name = u'党务先锋'
        verbose_name_plural = u'党务先锋'

    def __unicode__(self):
        return self.pioneer_title

class LifeTips(models.Model):
    lifetips_id = models.AutoField(primary_key=True,auto_created=True)
    lifetips_title = models.CharField(u'标题',max_length=10)
    lifetips_date = models.DateTimeField(u'创建日期',auto_now_add=True)
    lifetips_author = models.CharField(u'作者',max_length=30)
    lifetips_content = models.TextField(u'内容')

    class Meta:
        verbose_name = u'生活小贴士'
        verbose_name_plural = u'生活小贴士'

    def __unicode__(self):
        return self.lifetips_title

class PartyWork(models.Model):
    partywork_id = models.AutoField(primary_key=True,auto_created=True)
    partywork_title = models.CharField(u'标题',max_length=10)
    partywork_date = models.DateTimeField(u'创建日期',auto_now_add=True)
    partywork_author = models.CharField(u'作者',max_length=30)
    partywork_content = models.TextField(u'内容',)

    class Meta:
        verbose_name = u'党务提醒信息'
        verbose_name_plural = u'党务提醒信息'

    def __unicode__(self):
        return self.partywork_title

class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True,auto_created=True)
    notice_title = models.CharField(u'标题',max_length=10)
    notice_date = models.DateTimeField(u'创建日期',auto_now_add=True)
    notice_author = models.CharField(u'作者',max_length=30)
    notice_content = models.TextField(u'内容')

    class Meta:
        verbose_name = u'公告活动信息'
        verbose_name_plural = u'公告活动信息'

    def __unicode__(self):
        return self.notice_title

class Spirit(models.Model):
    spirit_id = models.AutoField(primary_key=True,auto_created=True)
    spirit_title = models.CharField(u'标题',max_length=10)
    spirit_date = models.DateTimeField(u'创建日期',auto_now_add=True)
    spirit_author = models.CharField(u'作者',max_length=30)
    spirit_content = models.TextField(u'内容')

    class Meta:
        verbose_name = u'上级精神'
        verbose_name_plural = u'上级精神'

    def __unicode__(self):
        return self.spirit_title

class Policy(models.Model):
    policy_id = models.AutoField(primary_key=True,auto_created=True)
    policy_title = models.CharField(u'标题',max_length=10)
    policy_date = models.DateTimeField(u'创建日期',auto_now_add=True)
    policy_author = models.CharField(u'作者',max_length=30)
    policy_content = models.TextField(u'内容')

    class Meta:
        verbose_name = u'惠企政策'
        verbose_name_plural = u'惠企政策'

    def __unicode__(self):
        return self.policy_title

class Test(models.Model):
    party_id = models.AutoField(primary_key=True,auto_created=True)
    party_name = models.CharField(u'党支部名称',max_length=100)
    member_number = models.IntegerField(u'党员人数')
    contact_info = models.CharField(u'联系方式',max_length=300)
    attachment = models.FileField(upload_to='upload/',blank=True)
    pic = models.ImageField(upload_to='upload/',blank=True)

    class Meta:
        verbose_name = u'测试'
        verbose_name_plural = u'测试'


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
