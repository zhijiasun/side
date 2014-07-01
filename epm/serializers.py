from django.contrib.auth.models import User,Group
from rest_framework import serializers
from models import *

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
    class Meta:
        model = member
        fields = ['member_name','member_gender','member_nation','member_education','member_birth',
                'member_worktime','join_party_time','formal_member_time','now_party_time','birth_address',
                'home_address','living_address','member_phone','member_email','qq','weixin','school','id_card',
                'member_party','member_enter']

class TestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Test
        fields = ['party_id','party_name','member_number','contact_info']

class PioneerSerializer(serializers.ModelSerializer):
    pictureurl = serializers.SerializerMethodField('construct_images2')
    # img_list = serializers.RelatedField(many=True)
    img_size = ['default','148*111','400*300','640*480']
    class Meta:
        model = Pioneer
        fields = ['title', 'date', 'author', 'pictureurl']

    def construct_images(self,obj):
        images = obj.img_list.all()
        result = {}
        i = 0
        for im in images:
            i+=1
            result['image'+str(i)]= im
        return result

    def construct_images2(self,obj):
        images = obj.img_list.all()
        result = {}
        result['dl']='http://115.28.79.151:8081'
        result['imageList'] = []
        tmp_list = []
        tmp_dict = {}
        for im in images:
            base, ext = os.path.splitext(os.path.basename(im.pic.url))
            base_url = os.path.dirname(im.pic.url)
            for i in self.img_size:
                if not cmp(i,'default'):
                    tmp_dict['objectId']= os.path.join(base_url+'/'+base+'_default'+ext)
                    tmp_dict['size']=i
                    tmp_dict['type']='original'
                else:
                    tmp_dict['objectId']=os.path.join(base_url+'/'+base+'_'+i+ext)
                    tmp_dict['size']=i
                    tmp_dict['type']='thumbnail'
                tmp_list.append(tmp_dict)
                tmp_dict = {}
            result['imageList'].append(tmp_list)
            tmp_list = []
            tmp_dict = {}

        return result


class LifeTipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeTips
        fields = ['title', 'date', 'author', 'content']


class PartyWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyWork
        fields = ['title', 'date', 'author', 'content']


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['title', 'date', 'author', 'content']


class SpiritSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spirit
        fields = ['title', 'date', 'author', 'content']


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['title', 'date', 'author', 'content']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_title','create_time','reply_time','question_author','question_content','question_answer','is_published']

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProcess
        fields = ['title', 'date', 'author', 'content']
