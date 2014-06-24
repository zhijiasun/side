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
    image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Pioneer
        fields = ['pioneer_title','pioneer_date','pioneer_author','pioneer_pic']


    def get_image_url(self,obj):
        return obj.pioneer_pic.path


class LifeTipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeTips
        fields = ['lifetips_title','lifetips_date','lifetips_author']


class PartyWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyWork
        fields = ['partywork_title', 'partywork_date', 'partywork_author']


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['notice_title','notice_date','notice_author']


class SpiritSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spirit
        fields = ['spirit_title','spirit_date','spirit_author']


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ['policy_title','policy_date','policy_author']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_title','question_date','question_author','question_content','question_answer','is_published']
