from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$',                                                 'fedclub.salon.views.home', name='home'),

	# salon
    url(r'^salon/$',                                           'fedclub.salon.views.salon_list'),
    url(r'^salon/add/$',                                       'fedclub.salon.views.salon_add'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/$',                     'fedclub.salon.views.salon_get'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/update/$',              'fedclub.salon.views.salon_update'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/delete/$',              'fedclub.salon.views.salon_delete'),

	# many users
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/$',              'fedclub.salon.views.users_list'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/delete$',        'fedclub.salon.views.users_delete'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/accept$',        'fedclub.salon.views.users_accept'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/reject$',        'fedclub.salon.views.users_reject'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/email$',         'fedclub.salon.views.users_email'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/accept_email$',  'fedclub.salon.views.users_accept_email'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/reject_email$',  'fedclub.salon.views.users_reject_email'),

	# single user
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/$',           'fedclub.salon.views.user_get'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/delete$',     'fedclub.salon.views.user_delete'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/update$',     'fedclub.salon.views.user_update'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/accept$',     'fedclub.salon.views.user_accept'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/reject$',     'fedclub.salon.views.user_reject'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/email$',      'fedclub.salon.views.user_email'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/accept_email$','fedclub.salon.views.user_accept_email'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/(?P<user_id>[\w\d]+)/reject_email$','fedclub.salon.views.user_reject_email'),

	# check in, by barcode
    url(r'^salon/(?P<salon_id>[\w\d]+)/checkin_manual/home$',       'fedclub.salon.views.checkin_manual_home'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/checkin_manual$',            'fedclub.salon.views.checkin_manual'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/checkin$',                   'fedclub.salon.views.checkin'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
