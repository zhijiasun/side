#coding:utf-8
from xadmin.sites import site
from ams.models import AppComment, VersionManager


class AppCommentAdmin(object):
    list_display = ('app_version','phone_info','comment')


class VersionManagerAdmin(object):
    list_display = ('version_code','version_name','description','apk')
    list_filter = ('version_code','version_name','description','apk')

site.register(AppComment, AppCommentAdmin)
site.register(VersionManager, VersionManagerAdmin)
