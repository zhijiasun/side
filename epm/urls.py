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
    url(r'^process$',views.process_list),
    url(r'^(?P<username>.*)/questions$',views.question_list),
    url(r'^(?P<username>.*)/question/$',views.submit_question),
    url(r'^(?P<username>.*)/member/$',views.member_info),
    url(r'^(?P<username>.*)/partywork$',views.partywork_list),
    url(r'^(?P<username>.*)/member/verify/$',views.member_verify),
    url(r'^(?P<username>.*)/party/verify/$',views.party_verify),
    # url(r'^(?P<username>.*)/party/$',views.party_verify),//To-do get all the members info
    url(r'^(?P<username>.*)/info/$',views.user_info),
    # url(r'^member/$',views.member_list),
    # url(r'^question/$',views.raise_question),
    # url(r'^questions$',views.question_list),
)
