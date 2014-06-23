from django.conf.urls import patterns,url,include
from epm import views

urlpatterns = patterns('',
	# url(r'^party/$',views.party_list),
	# url(r'^process/$',views.process_import),
    # url(r'^users/register',views.create_user),
    url(r'^pioneer$',views.pioneer_list),
    url(r'^lifetips$',views.lifetips_list),
    url(r'^policy$',views.policy_list),
    url(r'^spirit$',views.spirit_list),
    url(r'^notice$',views.notice_list),
    url(r'^member/verify/$',views.member_verify),
    url(r'^member/$',views.member_list),
)
