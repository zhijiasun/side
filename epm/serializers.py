from django.contrib.auth.models import User,Group
from rest_framework import serializers
from models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url','username','email','groups')

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
