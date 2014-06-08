#coding:utf-8
from import_export import resources
from models import *
from django.template import loader
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin
from xadmin.views.base import CommAdminView
import pdb

class EnterpriseResource(resources.ModelResource):
    class Meta:
        model = enterprise

class MyPlugin(BaseAdminPlugin):
    flag = True

    def init_request(self,*args,**kwargs):
        print dir(self)
        print '#########'
        print self.admin_view,self.admin_site
        print type(self.model._meta)
        print 'aaa'
        return bool(self.flag)

    def get_form_datas(*args,**kwargs):
        print 'aaa'
        super(MyPlugin,self).get_form_datas(*args,**kwargs)



    def block_top_toolbar(self,context,nodes):
        context.update({'import_url':'import/'})
        # c = {'import_url':'/import/'}
        nodes.append(loader.render_to_string('import.html',context_instance=context))


class ImportPlugin(BaseAdminPlugin):

    f = True
    def init_request(self,*args,**kwargs):
        print 'ImportPlugin9999999999'
        return bool(self.f)

    def block_nav_btns(self,context,nodes):
        print 'CCCCCCCCCCCCCCCC'
        c = {}
        nodes.append(loader.render_to_string('button.html',context_instance=c))
