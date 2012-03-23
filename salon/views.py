# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader
from salon.models import Salon, User

from salon.utils import get_bar_code, send_mail
# ^$
def home(request):
	get_bar_code('RENREN', 'F32321D')
	get_bar_code('FED', 'FDKJ32123')

	send_mail('RENREN', 'test', 'F32321D')
	send_mail('FED', 'test', 'FDKJ32123')

	salons = Salon.objects.all()
	t = loader.get_template('index.html')
	c = Context({
		'salons' : salons
	})
	return HttpResponse(t.render(c))

# ^salon/$
def salon_list(request):
	return HttpResponse('salon_list')
# ^salon/add/
def salon_add(request):
	return HttpResponse('salon_add')
# ^salon/(?P<salon_id>[\w\d]+)/$
def salon_get(request, salon_id):
	return HttpResponse('salon_get')
# ^salon/(?P<salon_id>[\w\d]+)/update/$
def salon_update(request, salon_id):
	return HttpResponse('salon_update')
# ^salon/(?P<salon_id>[\w\d]+)/delete/$
def salon_delete(request, salon_id):
	return HttpResponse('salon_delete')

# many users
# ^salon/(?P<salon_id>[\w\d]+)/users/$
def users_list(request, salon_id):
	return HttpResponse('users_list')

#^salon/(?P<salon_id>[\w\d]+)/users/delete$
def users_delete(request, salon_id):
	return HttpResponse('users_delete')

# ^salon/(?P<salon_id>[\w\d]+)/users/accept$
def users_accept(request, salon_id):
	return HttpResponse('users_accept')

# ^salon/(?P<salon_id>[\w\d]+)/users/reject$
def users_reject(request, salon_id):
	return HttpResponse('users_reject')

# ^salon/(?P<salon_id>[\w\d]+)/users/email$
def users_email(request, salon_id):
	return HttpResponse('users_email')

# ^salon/(?P<salon_id>[\w\d]+)/users/accept_email$
def users_accept_email(request, salon_id):
	return HttpResponse('users_accept_email')

# ^salon/(?P<salon_id>[\w\d]+)/users/reject_email$
def users_reject_email(request, salon_id):
	return HttpResponse('users_reject_email')

# single user
# ^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/$
def user_get(request, salon_id, user_id):
	return HttpResponse('user_get')

# ^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/delete$
def user_delete(request, salon_id, user_id):
	return HttpResponse('user_delete')

# ^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/update$
def user_update(request, salon_id, user_id):
	return HttpResponse('user_update')

# ^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/accept$
def user_accept(request, salon_id, user_id):
	return HttpResponse('user_accept')

# ^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/reject$
def user_reject(request, salon_id, user_id):
	return HttpResponse('user_reject')

# ^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/email$
def user_email(request, salon_id, user_id):
	return HttpResponse('user_email')

# ^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/accept_email$
def user_accept_email(request, salon_id, user_id):
	return HttpResponse('user_accept_email')

# ^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/reject_email$
def user_reject_email(request, salon_id, user_id):
	return HttpResponse('user_reject_email')

# check in, by barcode
# ^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/checkin$
def checkin(request, salon_id, user_id):
	return HttpResponse('checkin')

def checkin_manual(request, salon_id):
	return HttpResponse('checkin')
