from django.conf.urls import patterns, include, url
from rest_framework import routers
from epm import views

"""
from django.contrib import admin
admin.autodiscover()
"""
import xadmin
xadmin.autodiscover()

from xadmin.plugins import xversion
xversion.register_models()


router = routers.DefaultRouter()
router.register(r'users',views.UserViewSet)
router.register(r'groups',views.GroupViewSet)
router.register(r'enterprise',views.EnterpriseViewSet)
router.register(r'party',views.PartyViewSet)
router.register(r'member',views.MemberViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'side.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^xadmin/', include(xadmin.site.urls)),
    url(r'^',include(router.urls)),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    url(r'^epm/',include('epm.urls'))
)
