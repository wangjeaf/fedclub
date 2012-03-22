#encoding=utf-8
from django.db import models

# Create your models here.
class Salon(models.Model):
	salon_id = models.AutoField(primary_key = True) 	#主键
	name = models.CharField(max_length = 100) 			#活动名称
	start_time = models.DateTimeField()					#开始时间
	end_time = models.DateTimeField()   				#结束时间
	creator = models.CharField(max_length = 40)         #活动创建人
	description = models.CharField(max_length = 200)    #活动描述
	address = models.CharField(max_length = 200)        #地址

class User(models.Model):
	user_id = models.AutoField(primary_key = True)		#主键
	salon = models.ForeignKey(Salon)					#外键，关联salon

	name = models.CharField(max_length = 40) 			#报名人姓名
	mobile = models.PositiveIntegerField(null=True) 	#手机号
	email = models.EmailField()							#邮件
	company = models.CharField(null=True, max_length = 100) #公司名
	introduction = models.CharField(null=True, max_length = 200) #自我介绍

	#状态
	# 1、未处理 00
	# 2、已同意未发邮件 10
	# 3、已同意已发邮件 11
	# 4、已拒绝未发邮件 20
	# 5、已拒绝已发邮件 21
	status = models.SmallIntegerField()
