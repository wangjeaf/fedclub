# Create your views here.

from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader
from salon.models import Salon, User
from salon.utils import send_mail, gen_barcode_md5
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
import datetime

# ^$
def home(request):
	salons = Salon.objects.all()
	return render_to_response('index.html', {'salons': salons})

# ^salon/$
def salon_list(request):
	return HttpResponse('salon_list')

# ^salon/add/
def salon_add(request):
	try:
		edit_type = request.POST['edit_type']
	except(KeyError):
		return render_to_response('salon/add.html', {}, context_instance=RequestContext(request))
	else:
		salon = Salon()
		salon.code = request.POST['code']
		salon.name = request.POST['name']
		salon.start_time = request.POST['start_time']
		salon.end_time = request.POST['end_time']
		salon.creator = request.POST['creator']
		salon.description = request.POST['description']
		salon.address = request.POST['address']
		salon.save()
		return HttpResponseRedirect(reverse('home'))

# ^salon/(?P<salon_id>[\w\d]+)/$
def salon_get(request, salon_id):
	salon = Salon.objects.get(code = salon_id)
	users = User.objects.filter(salon = salon.salon_id)
	untreated_users = User.get_untreated()
	accepted_users = User.get_accepted()
	rejected_users = User.get_rejected()
	print 'untreat:'+ str(len(untreated_users))
	return render_to_response('salon/view.html', {'salon':salon, 'users':users,'untreated_users':untreated_users,'accepted_users':accepted_users,'rejected_users':rejected_users}, context_instance=RequestContext(request))

# ^salon/(?P<salon_id>[\w\d]+)/update/$
def salon_update(request, salon_id):
	return HttpResponse('salon_update')
# ^salon/(?P<salon_id>[\w\d]+)/delete/$
def salon_delete(request, salon_id):
	salon = Salon.objects.get(code = salon_id)
	salon_name = salon.name
	salon.delete()
	return render_to_response('salon/delete_success.html', {'salon_name':salon_name})

# many users
# ^salon/(?P<salon_id>[\w\d]+)/users/$
def users_list(request, salon_id):
	return HttpResponse('users_list')

# ^salon/(?P<salon_id>[\w\d]+)/users/add/$
def users_add(request, salon_id):
	try:
		edit_type = request.POST['edit_type']
	except(KeyError):
		return render_to_response('user/add.html', {'salon_id':salon_id}, context_instance=RequestContext(request))
	else:
		salon = Salon.objects.get(code = salon_id)
		user = User()
		user.salon = salon
		user.name = request.POST['name']
		user.company = request.POST['company']
		user.mobile = request.POST['mobile']
		user.email = request.POST['email']
		user.introduction = request.POST['introduction']
		user.barcode = gen_barcode_md5(salon, user)
		user.register_time = datetime.datetime.today()
		user.status = 0
		user.save()
		return HttpResponseRedirect('/salon/' + user.salon.code + '/')

#^salon/(?P<salon_id>[\w\d]+)/users/delete$
def users_delete(request, salon_id):
	return HttpResponse('users_delete')

#^salon/(?P<salon_id>[\w\d]+)/users/reset$
def users_reset(request, salon_id):
	if request.POST.has_key('select_rejected_users'):
		user_ids = request.POST.getlist('select_rejected_users')
		for user_id in user_ids:
			user = User.objects.get(user_id = user_id)
			if (user.status != 21):
				user.status = 0
				user.save()

	if request.POST.has_key('select_accepted_users'):
		user_ids = request.POST.getlist('select_accepted_users')
		for user_id in user_ids:
			user = User.objects.get(user_id = user_id)
			if (user.status != 11 and user.status != 12):
				user.status = 0
				user.save()

	return HttpResponseRedirect('/salon/' + salon_id + '/')

# ^salon/(?P<salon_id>[\w\d]+)/users/accept$
def users_accept(request, salon_id):
	if request.POST.has_key('select_untreated_users'):
		user_ids = request.POST.getlist('select_untreated_users')
		for user_id in user_ids:
			user = User.objects.get(user_id = user_id)
			if (user.status != 10):
				user.status = 10
				user.save()

	return HttpResponseRedirect('/salon/' + salon_id + '/')

# ^salon/(?P<salon_id>[\w\d]+)/users/reject$
def users_reject(request, salon_id):
	if request.POST.has_key('select_untreated_users'):
		user_ids = request.POST.getlist('select_untreated_users')
		for user_id in user_ids:
			user = User.objects.get(user_id = user_id)
			if (user.status != 20):
				user.status = 20
				user.save()

	return HttpResponseRedirect('/salon/' + salon_id + '/')

# ^salon/(?P<salon_id>[\w\d]+)/users/email$
def users_email(request, salon_id):
	return HttpResponse('users_email')

# ^salon/(?P<salon_id>[\w\d]+)/users/accept_email$
def users_accept_email(request, salon_id):
	if request.POST.has_key('select_accepted_users'):
		salon = Salon.objects.get(code = salon_id)
		user_ids = request.POST.getlist('select_accepted_users')
		for user_id in user_ids:
			user = User.objects.get(user_id = user_id)
			if (user.status == 10):
				send_mail(salon, user)
				user.status = 11
				user.save()

	return HttpResponseRedirect('/salon/' + salon_id + '/')

# ^salon/(?P<salon_id>[\w\d]+)/users/reject_email$
def users_reject_email(request, salon_id):
	if request.POST['select_rejected_users']:
		salon = Salon.objects.get(code = salon_id)
		user_ids = request.POST.getlist('select_rejected_users')
		for user_id in user_ids:
			user = User.objects.get(user_id = user_id)
			if (user.status == 20):
				send_mail(salon, user)
				user.status = 21
				user.save()

	return HttpResponseRedirect('/salon/' + salon_id + '/')

# single user

# ^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/$
def user_get(request, salon_id, user_id):
	return HttpResponse('user_get')

# ^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/delete$
def user_delete(request, salon_id, user_id):
	user = User.objects.get(user_id = user_id)
	user.delete()
	return HttpResponseRedirect('/salon/' + salon_id + '/')

# ^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/update$
def user_update(request, salon_id, user_id):
	return HttpResponse('user_update')

# ^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/reset$
def user_reset(request, salon_id, user_id):
	user = User.objects.get(user_id = user_id)
	user.status = 0;
	user.save()
	return HttpResponseRedirect('/salon/'+salon_id+'/');
	#return HttpResponse('user_accept')

# ^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/accept$
def user_accept(request, salon_id, user_id):
	User.accept(user_id);
	return HttpResponseRedirect('/salon/'+salon_id+'/');
	#return HttpResponse('user_accept')

# ^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/reject$
def user_reject(request, salon_id, user_id):
	User.reject(user_id);
	return HttpResponseRedirect('/salon/'+salon_id+'/');
	#return HttpResponse('user_reject')

# ^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/email$
def user_email(request, salon_id, user_id):
	return HttpResponse('user_email')

# ^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/accept_email$
def user_accept_email(request, salon_id, user_id):
	user = User.objects.get(user_id = user_id)
	salon = Salon.objects.get(code = salon_id)
	send_mail(salon, user)
	if (user.status != 11):
		user.status = 11
		user.save()

	return HttpResponseRedirect('/salon/' + salon_id + '/')

# ^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/reject_email$
def user_reject_email(request, salon_id, user_id):
	user = User.objects.get(user_id = user_id)
	salon = Salon.objects.get(code = salon_id)
	send_mail(salon, user)
	if (user.status != 21):
		user.status = 21
		user.save()
	return HttpResponseRedirect('/salon/' + salon_id + '/')

# check in, by barcode
# ^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/checkin$
def checkin(request, salon_id):
	return HttpResponse('checkin')

def checkin_manual(request, salon_id):
	return HttpResponse('checkin')
