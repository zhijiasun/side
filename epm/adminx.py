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

class JasonAdmin(CommAdminView):
    list_display = ('party_name','member_number','contact_info','attachment')
    list_filter = ('party_name','member_number','contact_info')

    # def save_models(self):
    #     print 'In Jason Admin'
    #     print self.request.FILES
    #     # f = self.request.FILES['attachment']
    #     # pa = default_storage.save('abc',ContentFile(f.read()))
    #     super(JasonAdmin,self).save_models()
    #     print 'ok'

xadmin.site.register(Jason,JasonAdmin)


class MyAction(BaseActionView):
    action_name = "my_action"
    description = 'descripe the action'
    model_perm = 'change'

    def do_action(self,queryset):
        pass
class EnterpriseAdmin(object):
    list_display = ('enter_name','enter_address')
    list_filter = ('enter_name','enter_address')
    resource_class = EnterpriseResource


class PartyAdmin(object):
    list_display = ('party_name','member_number','contact_info')
    list_filter = ('party_name','member_number','contact_info')
    actions = [MyAction,]

class MemberAdmin(object):
    list_display = ('member_name','member_gender','member_worktime')
    list_filter = ('member_name','member_gender','member_worktime')

class GolbeSetting(object):
    globe_search_models = [Article, ]
    site_title = (u'崂山党建管理系统')
    site_footer = (u'www.centling.com')
    globe_models_icon = {
        Article: 'file', Category: 'cloud'
    }
xadmin.site.register(CommAdminView, GolbeSetting)

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
site.register_plugin(MyPlugin,ListAdminView)
xadmin.site.register(Article, ArticleAdmin)
xadmin.site.register(Category, CategoryAdmin)
