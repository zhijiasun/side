from django.conf.urls import patterns,url,include
from epm import views

urlpatterns = patterns('',
	url(r'^party/$',views.party_list),
    url(r'^users/register',views.create_user),
)
