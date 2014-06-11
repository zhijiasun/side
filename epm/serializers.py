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
    class Meta:
        model = Pioneer
        fields = ['pioneer_id','pioneer_title','pioneer_date','pioneer_author']
