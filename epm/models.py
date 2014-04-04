#coding:utf-8
from django.db import models

# Create your models here.

class enterprise(models.Model):

	STATE_OWNED_ENTER = 1
	COOPERATIVE_ENTER = 2
	JOIN_VENTURE = 3
	NATURE_CHOICES = (
		(STATE_OWNED_ENTER,u'国有企业'),
		(COOPERATIVE_ENTER,'合作企业'),
		(JOIN_VENTURE,u'合资企业'),
	)
	enter_id = models.AutoField(primary_key=True,auto_created=True)
	enter_name = models.CharField(u'企业名称',max_length=50)
	register_time = models.DateField(u'注册时间')
	enter_address = models.CharField(u'注册地址',max_length=50)
	enter_nature = models.IntegerField(u'企业性质',default=STATE_OWNED_ENTER,choices=NATURE_CHOICES)

	class Meta:
		verbose_name = u'企业信息'
		verbose_name_plural = u'企业信息'


	def __unicode__(self):
		return self.enter_name


class party(models.Model):
	party_id = models.AutoField(primary_key=True,auto_created=True)
	party_name = models.CharField(u'党支部名称',max_length=100)
	member_number = models.IntegerField(u'党员人数')
	contact_info = models.CharField(u'联系方式',max_length=300)

	class Meta:
		verbose_name = u'党支部信息'
		verbose_name_plural = u'党支部信息'


	def __unicode__(self):
		return self.party_name


