#python
#encoding=utf-8
import smtplib
import email
from email.Utils import formatdate
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.Header import Header  
import urllib
import os
import hashlib
from salon.models import Salon, User
from django.template import Context, loader

google_chart_api_url = 'http://chart.apis.google.com/chart?cht=qr&chs=150x150&chl='
check_in_url = 'http://fed.d.xiaonei.com/salon/%s/users/checkin?barcode=%s'

# 生成text对应的md5编码的前六位
# text是由沙龙名称、用户名称、用户邮箱组合确定的
def gen_barcode_md5(salon, user):
	text = salon.code + '_' + user.email
	m = hashlib.md5()
	m.update(text)
	result = m.hexdigest()
	# 加密以后取前六位 
	return result[:6]

# 确保content是一个带唯一身份认证的url信息，扫描后可直接点击
def get_bar_code(salon_code, barcode):
	checkin_url = check_in_url % (str(salon_code), str(barcode))
	file_path = 'barcode_images/' + str(salon_code) + '_' + str(barcode) + '.png'
	if not os.path.exists(file_path):
		urllib.urlretrieve(google_chart_api_url + str(checkin_url), file_path)
	return file_path

# send mail to developers according to task info
def send_mail(salon, user):
	
	# email, with attachment
	msg_root = MIMEMultipart()

	# encoding 
	msg_root["Accept-Language"] = "zh-CN"
	msg_root["Accept-Charset"]="ISO-8859-1,utf-8"

	if (user.accepted()):
		t = loader.get_template('email/accept.html')
	else:
		t = loader.get_template('email/reject.html')
	# email message
	c = Context({
        'user': user, 
		'salon': salon
    })
	email_content = t.render(c)
	text_msg = MIMEText(email_content, 'html', 'utf-8')
	msg_root.attach(text_msg)

 	# append barcode image file as attachment
	image_file = get_bar_code(salon.code, user.barcode);
	image_content = open(image_file, 'rb').read();
	image_att = MIMEImage(image_content, 'png')
	image_att.add_header('Content-Disposition', 'attachment', filename='barcode.png')
	image_att.add_header('Content-ID', '<bar_code_image>')    
	msg_root.attach(image_att)

	# to
	# to_list = ('zhifu.wang@renren-inc.com', 'wentao.zhang@renren-inc.com;')
	to_list = user.email

	# from
	me = 'no-reply.fed' + "<no-reply.fed@renren-inc.com>"

	# other 
	msg_root['subject'] = Header('第一届人人前端技术沙龙邀请函', 'utf-8')  
	msg_root['from'] = me
	msg_root['date'] = formatdate()

	if (isinstance(to_list, tuple)):
		msg_root['to'] = ';'.join(to_list)
	else:
		msg_root['to'] = to_list

	try:
		s = smtplib.SMTP("smtp.renren-inc.com")
		s.sendmail(me, to_list, msg_root.as_string())
		s.close()
		return True
	except Exception, e:
		print str(e)
		return False

if __name__ == '__main__':
	get_bar_code('RENREN', 'F32321D')
	get_bar_code('FED', 'FDKJ32123')

	#send_mail('RENREN', 'test', 'F32321D')
	#send_mail('FED', 'test', 'FDKJ32123')

	# print gen_barcode_md5('FED_Salon_wangjeaf_wangjeaf@gmail.com')
