from django.shortcuts import render
from django.contrib.auth.models import User,Group
from rest_framework import viewsets
from epm.serializers import UserSerializer,GroupSerializer,EnterpriseSerializer,PartySerializer
from models import *

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer


class EnterpriseViewSet(viewsets.ModelViewSet):
	queryset = enterprise.objects.all()
	serializer_class = EnterpriseSerializer

class PartyViewSet(viewsets.ModelViewSet):
	queryset = party.objects.all()
	serializer_class = PartySerializer