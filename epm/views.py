from django.shortcuts import render
from django.contrib.auth.models import User,Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from epm.serializers import *
from models import *
from django.views.decorators.csrf import csrf_exempt

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

@api_view(['POST'])
@csrf_exempt
def create_user(request):
    print 'aaaaaaaaaaaa'
    serialized = MyUserSerializer(data=request.DATA)
    if serialized.is_valid():
        print dir(serialized)
        print serialized.data

        username = serialized.init_data['username'],
        email = serialized.init_data['email'],
        password = serialized.init_data['password']

        u = User.objects.create_user(username,email,password)
        print u._meta.get_all_field_names()
        u.save()
        # u.set_password(serialized.init_data['password'])
        # try:
        #     u = User.objects.create(username=serialized.init_data['username'],password=serialized.init_data['password'],email=serialized.init_data['email'])
        # except Exception,e:
        #     print e
        # print type(u)
        print 'fadsfd'
        return Response(serialized.data,status = status.HTTP_201_CREATED)
        print serialized.data
    else:
        print 'else'
        print serialized.data
        return Response(serialized._errors,status = status.HTTP_400_BAD_REQUEST)


#method 1, use #api_view decoractor
@api_view(['GET','POST'])
def party_list(request):
    print("IP Address for debug-toolbar: " + request.META['REMOTE_ADDR'])
    p = party.objects.all()
    serilizer = PartySerializer(p,many=True)
    return Response(serilizer.data)


#method 2,inherit from the APIView class
class PartyList(APIView):
	def get(self,request):
		pass
	def delete(self,request,pk):
		pass	

from xadmin.sites import site
from xadmin.views import BaseAdminView,CommAdminView
from django.template.response import TemplateResponse

class MyAdminView(BaseAdminView):
    def get(self,request,*args,**kwargs):
        print 'aaaa'
        return TemplateResponse(request,'test.html')

# class MyCommView(CommAdminView):
#     site_title = 'me_comm'

# site.register_view(r'^me_test/$',MyAdminView,name='my_test')
# site.register_view(r'^me_comm/$',MyCommView,name='my_comm')
