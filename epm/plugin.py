#coding:utf-8
from import_export import resources
from models import *
from django.template import loader
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin
from xadmin.views.base import CommAdminView

class EnterpriseResource(resources.ModelResource):
    class Meta:
        model = enterprise

class MyPlugin(BaseAdminPlugin):
    flag = True
    def init_request(self,*args,**kwargs):
        return bool(self.flag)

    def block_top_toolbar(self,context,nodes):
        c = {}
        nodes.append(loader.render_to_string('import.html',context_instance=c))
