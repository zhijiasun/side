#coding:utf-8
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.http import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view,link,authentication_classes,permission_classes
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
import time,datetime
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from registration.views import RegistrationView as BaseRegistrationView
from registration import signals
from rest_framework.serializers import _resolve_model
from django.contrib.auth import authenticate,login
from django.core.exceptions import ObjectDoesNotExist
import csv

# Create your views here.


class RegistrationView(BaseRegistrationView):
    def register(self,request,**cleaned_data):
        print cleaned_data
        username,email,password = cleaned_data['username'],cleaned_data['email'],cleaned_data['password1']
        u = User.objects.create_user(username, email, password)
        # u.is_staff = True
        # u.save()
        # new_user = authenticate(username=username, password=password)
        # login(request, new_user)

        signals.user_registered.send(sender=self.__class__,
            user=u, request=request)
        
        # user_profile_model = _resolve_model
        # new_user.is_staff=True
        UserProfile.objects.create(user=u)
        return u


class IsVerified(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print 'obj is:',type(obj)
        print obj.app_user
        print request.user

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

    @link()
    def get_bynumber(self,request,pk=None):
        print pk
        tests = Test.objects.filter(member_number=pk)
        tserializer = TestSerializer(tests,many=True)
        return Response(tserializer.data)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def member_verify(request):
    if request.method == 'POST':
        result = {"result":"0001", "message": "invalid request","is_verified":"False"}
        name = request.DATA.get('real_name','')
        idcard = request.DATA.get('real_idcard','')
        print request.DATA
        if name and idcard:
            print name,idcard
            m = member.objects.filter(id_card=idcard)
            print m
            if len(m) is 1:
                u = UserProfile.objects.get(user=request.user)
                u.is_verified = True
                u.save()
                result['is_verified']="True"
                result['result']='0000'
                result['message']='OK'
                return Response(result,status = status.HTTP_200_OK)
        return Response(result,status=status.HTTP_400_BAD_REQUEST)


def party_list(request):
    pass


def enter_list(request):
    pass


@api_view(['GET','POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def member_list(request):
    if request.method == 'GET':
        print request.user
        appuser = request.user.app_user.all()
        print type(appuser)
        print dir(appuser)
        if appuser[0].is_verified:
            try:
                m = member.objects.get(id_card = appuser[0].real_idcard)
            except ObjectDoesNotExist:
                print 'object does not exist'
            ms = MemberSerializer(m)
            result = {"result":"0000","message":"","data":ms.data}
            return Response(result,status = status.HTTP_200_OK)


def get_result(model, modelSerializer,kwargs):

    print model,modelSerializer,kwargs
    startTime = time.localtime(float(kwargs.get('startTime',0)))
    startTime = datetime.datetime.fromtimestamp(time.mktime(startTime))

    if 'endTime' in kwargs.keys():
        endTime = time.localtime(float(kwargs.get('endTime')))
        endTime = datetime.datetime.fromtimestamp(time.mktime(endTime))
    else:
        endTime = datetime.datetime.now()

    ###???? shoud change this line
    obj = model.objects.filter(pioneer_date__gte=startTime).filter(pioneer_date__lte=endTime)
    print obj
    maxCount = int(kwargs.get('maxCount',10))
    offset = int(kwargs.get('offset',0))
    print obj

    obj = obj[offset:offset+maxCount]
    print obj
    objs = modelSerializer(obj,many=True)
    print objs.data
    result = {"result":"0000","message":"Successfully get content","data":objs.data}
    # if objs.is_valid():
    #     result = {"result":"0000","message":"Successfully get content","data":objs.data}
    #     print result
    # else:
    #     result = {"result":"0001","message":"Get content error!","data":objs.errors}
    #     print result
    return result




@api_view(['GET','POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def pioneer_list(request):
    """
    support four parameters in request.GET
    startTime -- the start time of the record
    endTime -- the end time of the record
    maxCount -- the max number of the results
    offset -- offset of the results
    """
    if request.method == 'GET':
        startTime = time.localtime(float(request.GET.get('startTime',0)))
        # endTime = time.localtime(float(request.GET.get('endTime',datetime.datetime.now().microsecond)))
        startTime = datetime.datetime.fromtimestamp(time.mktime(startTime))
        if 'endTime' in request.GET.keys():
            endTime = time.localtime(float(request.GET.get('endTime')))
            endTime = datetime.datetime.fromtimestamp(time.mktime(endTime))
        else:
            endTime = datetime.datetime.now()
        p = Pioneer.objects.filter(pioneer_date__gte=startTime).filter(pioneer_date__lte=endTime)

        maxCount = int(request.GET.get('maxCount',10))
        offset = int(request.GET.get('offset',0))

        p = p[offset:offset+maxCount]
        pa = PioneerSerializer(p,many=True)
        result = {"result":"0000","message":"xxxx","data":pa.data}
    elif request.method == 'POST':
        print 'Method is POST'
    return Response(result,status = status.HTTP_200_OK)

@api_view(['GET','POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def lifetips_list(request):
    """
    support four parameters in request.GET
    startTime -- the start time of the record
    endTime -- the end time of the record
    maxCount -- the max number of the results
    offset -- offset of the results
    """
    if request.method == 'GET':
        startTime = time.localtime(float(request.GET.get('startTime',0)))
        # endTime = time.localtime(float(request.GET.get('endTime',datetime.datetime.now().microsecond)))
        startTime = datetime.datetime.fromtimestamp(time.mktime(startTime))
        if 'endTime' in request.GET.keys():
            endTime = time.localtime(float(request.GET.get('endTime')))
            endTime = datetime.datetime.fromtimestamp(time.mktime(endTime))
        else:
            endTime = datetime.datetime.now()
        p = LifeTips.objects.filter(lifetips_date__gte=startTime).filter(lifetips_date__lte=endTime)

        maxCount = int(request.GET.get('maxCount',10))
        offset = int(request.GET.get('offset',0))

        p = p[offset:offset+maxCount]
        pa = LifeTipsSerializer(p,many=True)
        result = {"result":"0000","message":"xxxx","data":pa.data}
    elif request.method == 'POST':
        print 'Method is POST'
    return Response(result,status = status.HTTP_200_OK)


@api_view(['GET','POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def notice_list(request):
    """
    support four parameters in request.GET
    startTime -- the start time of the record
    endTime -- the end time of the record
    maxCount -- the max number of the results
    offset -- offset of the results
    """
    if request.method == 'GET':
        startTime = time.localtime(float(request.GET.get('startTime',0)))
        # endTime = time.localtime(float(request.GET.get('endTime',datetime.datetime.now().microsecond)))
        startTime = datetime.datetime.fromtimestamp(time.mktime(startTime))
        if 'endTime' in request.GET.keys():
            endTime = time.localtime(float(request.GET.get('endTime')))
            endTime = datetime.datetime.fromtimestamp(time.mktime(endTime))
        else:
            endTime = datetime.datetime.now()
        p = Notice.objects.filter(notice_date__gte=startTime).filter(notice_date__lte=endTime)

        maxCount = int(request.GET.get('maxCount',10))
        offset = int(request.GET.get('offset',0))

        p = p[offset:offset+maxCount]
        pa = NoticeSerializer(p,many=True)
        result = {"result":"0000","message":"xxxx","data":pa.data}
    elif request.method == 'POST':
        print 'Method is POST'
    return Response(result,status = status.HTTP_200_OK)


@api_view(['GET','POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def spirit_list(request):
    """
    support four parameters in request.GET
    startTime -- the start time of the record
    endTime -- the end time of the record
    maxCount -- the max number of the results
    offset -- offset of the results
    """
    if request.method == 'GET':
        startTime = time.localtime(float(request.GET.get('startTime',0)))
        # endTime = time.localtime(float(request.GET.get('endTime',datetime.datetime.now().microsecond)))
        startTime = datetime.datetime.fromtimestamp(time.mktime(startTime))
        if 'endTime' in request.GET.keys():
            endTime = time.localtime(float(request.GET.get('endTime')))
            endTime = datetime.datetime.fromtimestamp(time.mktime(endTime))
        else:
            endTime = datetime.datetime.now()
        p = Spirit.objects.filter(spirit_date__gte=startTime).filter(spirit_date__lte=endTime)

        maxCount = int(request.GET.get('maxCount',10))
        offset = int(request.GET.get('offset',0))

        p = p[offset:offset+maxCount]
        pa = SpiritSerializer(p,many=True)
        result = {"result":"0000","message":"xxxx","data":pa.data}
    elif request.method == 'POST':
        print 'Method is POST'
    return Response(result,status = status.HTTP_200_OK)


@api_view(['GET','POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def policy_list(request):
    """
    support four parameters in request.GET
    startTime -- the start time of the record
    endTime -- the end time of the record
    maxCount -- the max number of the results
    offset -- offset of the results
    """
    if request.method == 'GET':
        startTime = time.localtime(float(request.GET.get('startTime',0)))
        # endTime = time.localtime(float(request.GET.get('endTime',datetime.datetime.now().microsecond)))
        startTime = datetime.datetime.fromtimestamp(time.mktime(startTime))
        if 'endTime' in request.GET.keys():
            endTime = time.localtime(float(request.GET.get('endTime')))
            endTime = datetime.datetime.fromtimestamp(time.mktime(endTime))
        else:
            endTime = datetime.datetime.now()
        p = Policy.objects.filter(policy_date__gte=startTime).filter(policy_date__lte=endTime)

        maxCount = int(request.GET.get('maxCount',10))
        offset = int(request.GET.get('offset',0))

        p = p[offset:offset+maxCount]
        pa = PolicySerializer(p,many=True)
        result = {"result":"0000","message":"xxxx","data":pa.data}
    elif request.method == 'POST':
        print 'Method is POST'
    return Response(result,status = status.HTTP_200_OK)


@api_view(['GET','POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def question_list(request):
    """
    support four parameters in request.GET
    startTime -- the start time of the record
    endTime -- the end time of the record
    maxCount -- the max number of the results
    offset -- offset of the results
    """
    if request.method == 'GET':
        startTime = time.localtime(float(request.GET.get('startTime',0)))
        # endTime = time.localtime(float(request.GET.get('endTime',datetime.datetime.now().microsecond)))
        startTime = datetime.datetime.fromtimestamp(time.mktime(startTime))
        if 'endTime' in request.GET.keys():
            endTime = time.localtime(float(request.GET.get('endTime')))
            endTime = datetime.datetime.fromtimestamp(time.mktime(endTime))
        else:
            endTime = datetime.datetime.now()
        p = Question.objects.filter(question_date__gte=startTime).filter(question_date__lte=endTime)

        maxCount = int(request.GET.get('maxCount',10))
        offset = int(request.GET.get('offset',0))

        p = p[offset:offset+maxCount]
        pa = QuestionSerializer(p,many=True)
        result = {"result":"0000","message":"xxxx","data":pa.data}
    elif request.method == 'POST':
        print 'Method is POST'
    return Response(result,status = status.HTTP_200_OK)

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

    def post(self,request,*args,**kwargs):
        """
        here we can process the imported file,we can easily get the related model
        """
        print '############'
        print self.model
        print '############'
        print request.FILES
        f = request.FILES['import_file']
        datareader = csv.reader(f)
        print datareader
        line = f.readline()
        print line
        for row in datareader:
            print row
        return HttpResponseRedirect('/xadmin/')


site.register_modelview(r'^import/$',ImportAdminView,name='%s_%s_import')

def process_import(request):
    print request.FILES
    if request.POST:
        f = request.FILES['file']
        datareader = csv.reader(f)
        print datareader
        line = f.readline()
        print line
        for row in datareader:
            print row
    return HttpResponseRedirect('/xadmin/')
