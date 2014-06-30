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
        fields = ['member_name','member_gender','member_nation','member_worktime']

class TestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Test
        fields = ['party_id','party_name','member_number','contact_info']

class PioneerSerializer(serializers.ModelSerializer):
    img_list = serializers.SerializerMethodField('construct_images')
    # img_list = serializers.RelatedField(many=True)
    class Meta:
        model = Pioneer
<<<<<<< HEAD
        fields = ['title', 'date', 'author', 'content']
=======
        fields = ['pioneer_title','pioneer_date','pioneer_author','img_list']
>>>>>>> 1f2af3e8d80f39e973780000a0cfa35bbaaecf8c


    def construct_images(self,obj):
        images = obj.img_list.all()
        result = {}
        i = 0
        for im in images:
            i+=1
            result['image'+str(i)]= im
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
