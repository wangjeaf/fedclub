#encoding=utf-8
from django.db import models
import datetime

# Create your models here.
class Salon(models.Model):
	#主键
	salon_id = models.AutoField(primary_key = True)

	#沙龙对应的编码（用于在url中显示沙龙相关信息）
	code = models.CharField(max_length = 40)
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

	def is_finished(self):
		return self.end_time < datetime.datetime.today()
	def is_not_start(self):
		return self.start_time > datetime.datetime.today()
	def is_active(self):
		return self.start_time < datetime.datetime.today() < self.end_time

	def get_status(self):
		if (self.is_finished()):
			return 'finished'
		elif (self.is_not_start()):
			return 'not-start'
		elif (self.is_active()):
			return 'active'
		else:
			return 'unknown'

	def __unicode__(self):
		return "%s" % (self.name)

class User(models.Model):
	#主键
	user_id = models.AutoField(primary_key = True)
	#外键，关联salon
	salon = models.ForeignKey(Salon)

	#报名人相关信息

	#姓名
	name = models.CharField(max_length = 40) 
	#手机号
	mobile = models.CharField(null=True, max_length = 11)
	#邮件
	email = models.EmailField()	
	#公司名
	company = models.CharField(null=True, max_length = 100) 
	#自我介绍
	introduction = models.CharField(null=True, max_length = 200) 

	# 注册时间
	register_time = models.DateTimeField()

	#处理状态
	# 1、未处理 00
	# 2、已同意未发邮件 10
	# 3、已同意已发邮件 11
	# 4、已同意已发邮件已签到   12
	# 5、已拒绝未发邮件 20
	# 6、已拒绝已发邮件 21
	status = models.SmallIntegerField(default = 00)
	
	#二维码
	barcode = models.CharField(null = True, max_length = 40) 
	
	def get_status(self):
		if (self.not_handled()):
			return 'not-handle'
		elif (self.accepted()):
			if (self.emailed()):
				if (self.checkined()):
					return 'checkin'
				else:
					return 'accept&email'
			elif (self.not_emailed()):
				return 'accept&not-email'
		elif (self.rejected()):
			if (self.emailed()):
				return 'reject&email'
			elif (self.not_emailed()):
				return 'reject&not-email'

	def not_handled(self):
		return self.status == 0
	def accepted(self):
		return self.status / 10 == 1
	def rejected(self):
		return self.status / 10 == 2
	def emailed(self):
		return self.status % 10 > 0
	def not_emailed(self):
		return self.status % 10 == 0
	def checkined(self):
		return self.status % 10 == 2

	def __unicode__(self):
		return "%s(from %s), %s, %s, %s" % (self.name, self.company, self.mobile, self.email, self.introduction)

	@classmethod
	def get_untreated(cls, salon_id):
		return cls.objects.filter(salon = salon_id, status = 0)

	@classmethod
	def get_accepted(cls, salon_id):
		return cls.objects.filter(salon = salon_id, status__gt = 9, status__lt = 20).order_by('status')

	@classmethod
	def get_rejected(cls, salon_id):
		return cls.objects.filter(salon = salon_id, status__gt = 19).order_by('status')

	#接受user_id指定用户的申请	
	@classmethod
	def accept(cls,user_id):
		cls.__set_accept_flag__(user_id,10)
		
	#拒绝user_id指定用户的申请	
	@classmethod
	def reject(cls,user_id):
		cls.__set_accept_flag__(user_id,20)

	#设置user_id指定用户状态为已发送邮件	
	@classmethod
	def mailed(cls,user_id):
		cls.__set_mail_flag__(user_id,1)

	#设置user_id指定用户状态为未发送邮件	
	@classmethod
	def unmailed(cls,user_id):
		cls.__set_mail_flag__(user_id,0)

	#设置user_id指定用户状态为已签到
	@classmethod
	def checkined(cls,user_id):
		cls.__set_mail_flag__(user_id,2)

	@classmethod
	def __set_mail_flag__(cls,user_id,flag_num):
		user = cls.objects.get(user_id=user_id)
		flag = user.status
	        flag = flag / 10 * 10 + flag_num 
		user.status = flag
		user.save()

	@classmethod
        def __set_accept_flag__(cls,user_id,flag_num):
		user = cls.objects.get(user_id=user_id)
		flag = user.status
	        flag = flag % 10 + flag_num 
		user.status = flag
                user.save()

                	
