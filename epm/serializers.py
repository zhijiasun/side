from django.contrib.auth.models import User,Group
from rest_framework import serializers
from models import *
from epm.utils import *
from side import settings
import time

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url','username','email')#,'groups')

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url','name')


class EnterpriseSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = enterprise
		fields = ['enter_name','enter_address']


class PartySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = party
		fields = ['party_name','contact_info','member_number']


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    member_gender = serializers.SerializerMethodField('str_gender')
    member_nation = serializers.SerializerMethodField('str_nation')
    member_education = serializers.SerializerMethodField('str_education')
    member_party = serializers.SerializerMethodField('str_member_party')
    member_enter = serializers.SerializerMethodField('str_member_enter')
    member_birth = serializers.SerializerMethodField('str_member_birth')
    member_worktime = serializers.SerializerMethodField('str_member_worktime')
    join_party_time = serializers.SerializerMethodField('str_member_jointime')
    formal_member_time = serializers.SerializerMethodField('str_member_formaltime')
    now_party_time = serializers.SerializerMethodField('str_now_party_time')

    class Meta:
        model = member
        fields = ['member_name','member_gender','member_nation','member_education','member_birth',
                'member_worktime','join_party_time','formal_member_time','now_party_time','birth_address',
                'home_address','living_address','member_phone','member_email','qq','weixin','school','id_card',
                'member_party','member_enter']

    def str_member_birth(self, obj):
        if not obj.member_birth:
            return ''
        else:
            return obj.member_birth

    def str_member_worktime(self, obj):
        if obj.member_worktime:
            return obj.member_worktime
        else:
            return ''

    def str_member_jointime(self, obj):
        if obj.join_party_time:
            return obj.join_party_time
        else:
            return ''

    def str_member_formaltime(self, obj):
        if obj.formal_member_time:
            return obj.formal_member_time
        else:
            return ''

    def str_now_party_time(self, obj):
        if obj.now_party_time:
            return obj.now_party_time
        else:
            return ''

    def str_gender(self,obj):
        return GENDER[obj.member_gender][1] 

    def str_nation(self,obj):
        return NATION[obj.member_nation][1]

    def str_education(self,obj):
        return EDUCATION[obj.member_education][1]

    def str_member_party(self,obj):
        if obj.member_party:
            return obj.member_party.party_name
        else:
            return ''

    def str_member_enter(self,obj):
        if obj.member_enter:
            return obj.member_enter.enter_name
        else:
            return ''

class TestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Test
        fields = ['party_id','party_name','member_number','contact_info']


img_size = ['default',(148,111),(400,300),(640,480)]
BASE_DL = 'http://115.28.79.151:8081/media/upload'

def return_images(obj):
    images = obj.img_list.all()
    result = {}
    result['dl'] = BASE_DL
    result['imageList'] = []
    tmp_list = []
    tmp_dict = {}
    for im in images:
        base, ext = os.path.splitext(os.path.basename(im.pic.url))
        base_url = os.path.dirname(im.pic.url)
        base_name = os.path.basename(base_url)
        for i in img_size:
            if not cmp(i,'default'):
                tmp_dict['objectId']= os.path.join('/'+base_name+'/'+base+'_default'+ext)
                tmp_dict['size']=i
                tmp_dict['type']='original'
            else:
                #should have a judge whether the file existed
                tmp_dict['objectId']=os.path.join('/'+base_name+'/'+base+'_thumb_'+str(i[0])+'_'+str(i[1])+ext)
                # print settings.BASE_DIR + tmp_dict['objectId']
                # if os.path.exist(settings.BASE_DIR + tmp_dict['objectId']):
                #     print 'ok'
                tmp_dict['size']=str(i[0])+'*'+str(i[1])
                tmp_dict['type']='thumbnail'
            tmp_list.append(tmp_dict)
            tmp_dict = {}
        result['imageList'].append(tmp_list)
        tmp_list = []
        tmp_dict = {}
    return result


class PioneerSerializer(serializers.ModelSerializer):
    pictureurl = serializers.SerializerMethodField('construct_images')
    date = serializers.SerializerMethodField('date_to_timestamp')
    img_size = ['default',(148,111),(400,300),(640,480)]

    class Meta:
        model = Pioneer
        fields = ['title', 'date', 'author', 'content', 'pictureurl']

    def date_to_timestamp(self, obj):
        if obj.date:
            return time.mktime(obj.date.timetuple())

    def construct_images(self,obj):
        return return_images(obj)
        # images = obj.img_list.all()
        # result = {}
        # result['dl'] = BASE_DL
        # result['imageList'] = []
        # tmp_list = []
        # tmp_dict = {}
        # for im in images:
        #     base, ext = os.path.splitext(os.path.basename(im.pic.url))
        #     base_url = os.path.dirname(im.pic.url)
        #     base_name = os.path.basename(base_url)
        #     for i in self.img_size:
        #         if not cmp(i,'default'):
        #             tmp_dict['objectId']= os.path.join('/'+base_name+'/'+base+'_default'+ext)
        #             tmp_dict['size']=i
        #             tmp_dict['type']='original'
        #         else:
        #             #should have a judge whether the file existed
        #             tmp_dict['objectId']=os.path.join('/'+base_name+'/'+base+'_thumb_'+str(i[0])+'_'+str(i[1])+ext)
        #             tmp_dict['size']=str(i[0])+'*'+str(i[1])
        #             tmp_dict['type']='thumbnail'
        #         tmp_list.append(tmp_dict)
        #         tmp_dict = {}
        #     result['imageList'].append(tmp_list)
        #     tmp_list = []
        #     tmp_dict = {}

        # return result


class LifeTipsSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField('date_to_timestamp')

    class Meta:
        model = LifeTips
        fields = ['title', 'date', 'author', 'content']

    def date_to_timestamp(self, obj):
        if obj.date:
            return time.mktime(obj.date.timetuple())


class PartyWorkSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField('date_to_timestamp')

    class Meta:
        model = PartyWork
        fields = ['title', 'date', 'author', 'content']

    def date_to_timestamp(self, obj):
        if obj.date:
            return time.mktime(obj.date.timetuple())


class NoticeSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField('date_to_timestamp')

    class Meta:
        model = Notice
        fields = ['title', 'date', 'author', 'content']

    def date_to_timestamp(self, obj):
        if obj.date:
            return time.mktime(obj.date.timetuple())

class SpiritSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField('date_to_timestamp')

    class Meta:
        model = Spirit
        fields = ['title', 'date', 'author', 'content']

    def date_to_timestamp(self, obj):
        if obj.date:
            return time.mktime(obj.date.timetuple())

class PolicySerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField('date_to_timestamp')

    class Meta:
        model = Policy
        fields = ['title', 'date', 'author', 'content']

    def date_to_timestamp(self, obj):
        if obj.date:
            return time.mktime(obj.date.timetuple())

class QuestionSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField('create_to_timestamp')
    reply_time = serializers.SerializerMethodField('reply_to_timestamp')

    class Meta:
        model = Question
        fields = ['question_id','question_title','create_time','reply_time','question_author','question_content','question_answer']

    def create_to_timestamp(self, obj):
        if obj.create_time:
            return time.mktime(obj.create_time.timetuple())

    def reply_to_timestamp(self, obj):
        if obj.reply_time:
            return time.mktime(obj.reply_time.timetuple())

class ProcessSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField('date_to_timestamp')

    class Meta:
        model = BusinessProcess
        fields = ['title', 'date', 'author', 'content']

    def date_to_timestamp(self, obj):
        if obj.date:
            return time.mktime(obj.date.timetuple())
