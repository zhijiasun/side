from django.test import TestCase
from django.test.client import Client
from epm.models import Pioneer, member, UserProfile
from datetime import datetime
from django.contrib.auth.models import User
from django_dynamic_fixture import G
import json

# Create your tests here.


class PioneerTestCase(TestCase):
    
    def test_pioneer_create(self):
        p = Pioneer.objects.create(title='first pioneer title',date=datetime.now(),author='first author',content='content')
        self.assertEquals(p.title, 'first pioneer title')


class PioneerListTestCase(TestCase):

    def test_get_pioneer(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/pioneer')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10000)


class LifeTipsListTestCase(TestCase):

    def test_get_lifetips(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/lifetips')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10000)
        

class NoticeListTestCase(TestCase):

    def test_get_notice(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/notice')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10000)
        

class SpiritListTestCase(TestCase):

    def test_get_spirit(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/spirit')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10000)


class PolicyListTestCase(TestCase):

    def test_get_plicy(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/policy')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10000)


class PorcessListTestCase(TestCase):

    def test_get_null_process(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/process')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10011)

    def test_get_join_process_without_data(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/process?type=join')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10010)

    def test_get_invalid_type_process(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/process?type=invliad')
        result = json.loads(response.content)
        
        self.assertEquals(result['errCode'],10015)


class UserRegisterTestCase(TestCase):

    def test_user_register_successfully(self):
        c= Client()
        data = {'username':'test', 'email':'test@test.com','password':'123456'}
        response = c.post('/dangjian/laoshanparty/v1/register/', data)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10000)

    def test_user_register_without_username(self):
        c = Client()
        data = {'email':'test@test.com','password':'123456'}
        response = c.post('/dangjian/laoshanparty/v1/register/', data)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10016)

    def test_user_register_without_email(self):
        c = Client()
        data = {'username':'test','password':'123456'}
        response = c.post('/dangjian/laoshanparty/v1/register/', data)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'], 10000)

    def test_user_register_without_password(self):
        c = Client()
        data = {'usename':'test','email':'test@test.com'}
        response = c.post('/dangjian/laoshanparty/v1/register/', data)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10016)

    def create_existed_user(self):
        u = User.objects.create_user('username=test','password=123456')
        u.save()
        
    def test_user_register_with_existed_username(self):
        pass

class GetUserInfoTestCase(TestCase):

    fixtures = ['admin.json','epm.json']

    def test_get_valid_user_info(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/test/info/')
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10000)
        self.assertTrue('is_verified' in result['data'].keys())
        self.assertTrue('real_organization' in result['data'].keys())
        self.assertTrue('real_idcard' in result['data'].keys())
        self.assertTrue('is_manager' in result['data'].keys())
        self.assertTrue('real_name' in result['data'].keys())

    def test_get_invalid_user_info(self):
        c = Client()
        response = c.get('/dangjian/laoshanparty/v1/invalid/info/')
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10006)
        self.assertTrue('data' not in result.keys())


class MemberVerifyTestCase(TestCase):

    def test_member_verify_with_valid_info(self):
        #initialize the needed data
        m = G(member,member_name='test_name',id_card='123456789012345678')
        user = G(User,username='testMember',password='123456')
        up = G(UserProfile, user=user)

        data = {'real_name':'test_name','real_idcard':'123456789012345678'}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/testMember/member/verify/', data)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10000)

    def test_member_verify_with_invliad_info(self):
        m = G(member,member_name='test_name',id_card='123456789012345678')
        user = G(User,username='testMember',password='123456')
        up = G(UserProfile, user=user)

        #with invliad real_name
        data = {'real_name':'test_invliad_name','real_idcard':'123456789012345678'}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/testMember/member/verify/', data)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10005)

        #with invliad real_idcard
        data1 = {'real_name':'test_name','real_idcard':'223456789012345678'}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/testMember/member/verify/', data1)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10005)


        #with invliad username in api
        data2 = {'real_name':'test_name','real_idcard':'123456789012345678'}
        c = Client()
        response = c.post('/dangjian/laoshanparty/v1/invalid_name/member/verify/', data)
        result = json.loads(response.content)

        self.assertEquals(response.status_code,200)
        self.assertEquals(result['errCode'],10006)
