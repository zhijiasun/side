from models import *
import xadmin

class EnterpriseAdmin(object):
	list_display = ('enter_name','register_time','enter_address')
	list_filter = ('enter_name','register_time','enter_address')


class PartyAdmin(object):
	list_display = ('party_name','member_number','contact_info')
	list_filter = ('party_name','member_number','contact_info')

xadmin.site.register(enterprise,EnterpriseAdmin)
xadmin.site.register(party,PartyAdmin)