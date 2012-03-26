from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('fedclub.salon.views',
    # Examples:
    url(r'^$',                                                 'home', name='home'),

	# salon
    url(r'^salon/$',                                           'salon_list'),
    url(r'^salon/add/$',                                       'salon_add'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/$',                     'salon_get'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/update/$',              'salon_update'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/delete/$',              'salon_delete'),

	# many users
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/$',              'users_list'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/add/$',           'users_add'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/delete/$',        'users_delete'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/accept/$',        'users_accept'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/reject/$',        'users_reject'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/reset/$',         'users_reset'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/email/$',         'users_email'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/accept_email/$',  'users_accept_email'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/users/reject_email/$',  'users_reject_email'),

	# single user
    url(r'^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/$',           'user_get'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/delete/$',     'user_delete'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/update/$',     'user_update'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/accept/$',     'user_accept'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/reset/$',      'user_reset'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/reject/$',     'user_reject'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/email/$',      'user_email'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/accept_email/$','user_accept_email'),
    url(r'^salon/(?P<salon_id>[\w\d]+)/user/(?P<user_id>[\w\d]+)/reject_email/$','user_reject_email'),

	# check in, by barcode
    url(r'^salon/(?P<salon_id>[\w\d]+)/checkin_manual$',            'checkin_manual'),
    url(r'^salon/(?P<salon_code>[\w\d]+)/checkin$',                   'checkin'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
