#encoding=utf-8
from django.db import models

# Create your models here.
class Salon(models.Model):
	#主键
	salon_id = models.AutoField(primary_key = True)
	#活动名称
	name = models.CharField(max_length = 100)
	#开始时间
	start_time = models.DateTimeField()
	#结束时间
	end_time = models.DateTimeField()
	#活动创建人
	creator = models.CharField(max_length = 40)
	#活动描述
	description = models.CharField(max_length = 200)
	#活动地址
	address = models.CharField(max_length = 200)

class User(models.Model):
	#主键
	user_id = models.AutoField(primary_key = True)
	#外键，关联salon
	salon = models.ForeignKey(Salon)

	#报名人相关信息

	#姓名
	name = models.CharField(max_length = 40) 
	#手机号
	mobile = models.PositiveIntegerField(null=True)
	#邮件
	email = models.EmailField()	
	#公司名
	company = models.CharField(null=True, max_length = 100) 
	#自我介绍
	introduction = models.CharField(null=True, max_length = 200) 

	#处理状态
	# 1、未处理 00
	# 2、已同意未发邮件 10
	# 3、已同意已发邮件 11
	# 4、已拒绝未发邮件 20
	# 5、已拒绝已发邮件 21
	status = models.SmallIntegerField()
