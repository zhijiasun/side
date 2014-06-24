#coding:utf-8
from models import *
from xadmin.plugins.actions import BaseActionView
from import_export.admin import ImportExportModelAdmin
from plugin import *
from xadmin.sites import site
from xadmin import views
import xadmin
from xadmin.views import ListAdminView,ModelFormAdminView,CreateAdminView
from xadmin.layout import Fieldset, Field
from xadmin.views.base import CommAdminView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django import forms

# class JasonForm(forms.ModelForm):
#     class Meta:
#         model = Jason

class TestAdmin(CommAdminView):
    list_display = ('party_name','member_number','contact_info','attachment','pic','thumb')
    list_filter = ('party_name','member_number','contact_info')

    # def save_models(self):
    #     print 'In Jason Admin'
    #     print self.request.FILES
    #     # f = self.request.FILES['attachment']
    #     # pa = default_storage.save('abc',ContentFile(f.read()))
    #     super(JasonAdmin,self).save_models()
    #     print 'ok'

xadmin.site.register(Test,TestAdmin)


class MyAction(BaseActionView):
    action_name = "my_action"
    description = 'descripe the action'
    model_perm = 'change'

    def do_action(self,queryset):
        pass
class EnterpriseAdmin(object):
    list_display = ('enter_name','enter_address','enter_attribute',
            'industry_type','industry_nature','enter_scale','total_assets','related_party_status',
            'legal_person','legal_email','enter_email','legal_phone','fixed_phone')
    list_filter = ('enter_name','enter_address')
    resource_class = EnterpriseResource


class PartyAdmin(object):
    list_display = ('party_name','secretary_name','secretary_phone','member_number','responsible_name','related_enter','responsible_phone')
    list_filter = ('party_name','member_number')
    actions = [MyAction,]
    # reversion_enable = True


class MemberAdmin(object):

    list_display = ('member_name','member_gender','member_worktime','member_enter_name','member_party_name')
    list_filter = ('member_name','member_gender','member_worktime')
    # reversion_enable = True

class UserProfileAdmin(object):
    list_display = ('user','is_verified')

class PioneerImageAdmin(object):
    model = PioneerImage
    extra = 1

class PioneerAdmin(object):
    list_display = ('pioneer_id','pioneer_title','pioneer_date','pioneer_author','pioneer_content')
    list_filter = ('pioneer_title','pioneer_date','pioneer_author','pioneer_content')
    inlines = [PioneerImageAdmin]
    # reversion_enable = True


class LifeTipsAdmin(object):
    list_display = ('lifetips_id','lifetips_title','lifetips_date','lifetips_author','lifetips_content')
    list_filter = ('lifetips_id','lifetips_title','lifetips_date','lifetips_author','lifetips_content')
    # reversion_enable = True

class PartyWorkAdmin(object):
    list_display = ('partywork_id','partywork_title','partywork_date','partywork_author','partywork_content')
    list_filter = ('partywork_id','partywork_title','partywork_date','partywork_author','partywork_content')

    # reversion_enable = True


class NoticeAdmin(object):
    list_display = ('notice_id','notice_title','notice_date','notice_author','notice_content')
    list_filter = ('notice_id','notice_title','notice_date','notice_author','notice_content')

    # reversion_enable = True


class SpiritAdmin(object):
    list_display = ('spirit_id','spirit_title','spirit_date','spirit_author','spirit_content')
    list_filter = ('spirit_id','spirit_title','spirit_date','spirit_author','spirit_content')

    # reversion_enable = True

class PolicyAdmin(object):
    list_display = ('policy_id','policy_title','policy_date','policy_author','policy_content')
    list_filter = ('policy_id','policy_title','policy_date','policy_author','policy_content')

    # reversion_enable = True
    
class BusinessProcessAdmin(object):
    list_display = ('process_id','process_title','process_date','process_author','process_content','process_type')
    list_filter = ('process_id','process_title','process_date','process_author','process_content','process_type')

    # reversion_enable = True

class QuestionAdmin(object):
    list_display = ('question_id','question_title','question_date','question_author','question_content')
    list_filter = ('question_id','question_title','question_date','question_author','question_content')

    # reversion_enable = True

class ListSetting(object):
    object_list_template = 'new.html'

class GolbeSetting(object):
    globe_search_models = [Article, ]
    # menu_template = 'test.html'
    site_title = (u'崂山党建管理系统')
    site_footer = (u'www.centling.com')
    globe_models_icon = {
        Article: 'file', Category: 'cloud'
    }
xadmin.site.register(CommAdminView, GolbeSetting)
# xadmin.site.register(ListAdminView,ListSetting)

class ArticleAdmin(object):
    list_display = ('title', 'categories', 'date')
    list_display_links = ('title',)

    search_fields = ('title', 'content')
    list_editable = ('date',)
    list_filter = ('categories', 'date')

    form_layout = (
        Fieldset(u'基本信息',
            'title', 'date'
        ),
        Fieldset(u'文章内容',
            Field('content', template="xcms/content_field.html")
        ),
    )
    style_fields = {'content': 'wysi_ck', 'categories':'m2m_tree'}

class CategoryAdmin(object):
    list_display = ('name', 'parent')
    list_display_links = ('id', 'name',)

    search_fields = ('name', )
    list_editable = ('name', )
    list_filter = ('parent', )

xadmin.site.register(enterprise,EnterpriseAdmin)
xadmin.site.register(party,PartyAdmin)
xadmin.site.register(member,MemberAdmin)
xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(Pioneer,PioneerAdmin)
xadmin.site.register(LifeTips,LifeTipsAdmin)
xadmin.site.register(PartyWork,PartyWorkAdmin)
xadmin.site.register(Notice,NoticeAdmin)
xadmin.site.register(Spirit,SpiritAdmin)
xadmin.site.register(Policy,PolicyAdmin)
xadmin.site.register(BusinessProcess,BusinessProcessAdmin)
xadmin.site.register(Question,QuestionAdmin)
site.register_plugin(MyPlugin,ListAdminView)
# site.register_plugin(ImportPlugin,ListAdminView)
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Category, CategoryAdmin)
