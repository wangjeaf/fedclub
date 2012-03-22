from salon.models import Salon
from salon.models import User

from django.contrib import admin

class SalonAdmin(admin.ModelAdmin):
	fields = ['name', 'start_time', 'end_time', 'creator', 'description', 'address']
	list_display = ['name', 'start_time', 'end_time', 'creator', 'description', 'address', 'get_status']
	list_filter = ['creator']

class UserAdmin(admin.ModelAdmin):
	fields = ['salon', 'name', 'mobile', 'email', 'company', 'introduction']
	list_display = ['salon', 'name', 'mobile', 'email', 'company', 'introduction', 'get_status']

admin.site.register(User, UserAdmin)
admin.site.register(Salon, SalonAdmin)
