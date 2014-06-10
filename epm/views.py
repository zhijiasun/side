#coding:utf-8
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from epm.serializers import *
from models import *
from django.views.decorators.csrf import csrf_exempt
from xadmin.views.edit import ModelFormAdminView,CreateAdminView
from django import forms
from django.utils.encoding import force_unicode
from import_export.admin import ImportMixin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = member.objects.all()
    serializer_class = MemberSerializer


class EnterpriseViewSet(viewsets.ModelViewSet):
	queryset = enterprise.objects.all()
	serializer_class = EnterpriseSerializer

class PartyViewSet(viewsets.ModelViewSet):
	queryset = party.objects.all()
	serializer_class = PartySerializer

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

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
        return TemplateResponse(request,'test.html')

# class MyCommView(CommAdminView):
#     site_title = 'me_comm'

site.register_view(r'^me_test/$',MyAdminView,name='my_test')
# site.register_view(r'^me_comm/$',MyCommView,name='my_comm')
class ImportForm(forms.Form):
    import_file = forms.FileField(label = u'选择输入的文件')

    def __init__(self,*args,**kwargs):
        super(ImportForm,self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit','Submit'))
    

class ImportAdminView(ImportMixin,CreateAdminView):
    add_form_template = 'model_form.html'
    import_template_name = 'model_form.html'

    def get_context(self):
        '''
        re-implement import_action()
        '''
        resource = self.get_import_resource_class()()
        icontext = {}
        print resource
        fileform = ImportForm
        fileform.helper = self.get_form_helper()
        if fileform.helper:
            print 'add input'
            fileform.helper.add_input(Submit('submit', 'Submit'))
        new_context = {'import_title':('从文件导入 %s') % force_unicode(self.opts.verbose_name),'fileform':fileform}
        context = super(CreateAdminView, self).get_context()
        context.update(new_context)
        return context

site.register_modelview(r'^import/$',ImportAdminView,name='%s_%s_import')

def process_import(request):
    print request.FILES
    return HttpResponseRedirect('/xadmin/')
