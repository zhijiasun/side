from django.conf.urls import patterns,url,include
from epm import views

urlpatterns = patterns('',
	url(r'^party/$',views.party_list),
	url(r'^process/$',views.process_import),
    url(r'^users/register',views.create_user),
    url(r'^pioneer$',views.pioneer_list),
    url(r'^lifetips$',views.lifetips_list),
)
