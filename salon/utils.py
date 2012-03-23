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

google_chart_api_url = 'http://chart.apis.google.com/chart?cht=qr&chs=150x150&chl='
check_in_url = 'http://fed.d.xiaonei.com/salon/%s/users/checkin?barcode=%s'

# 生成text对应的md5编码的前六位
# text是由沙龙名称、用户名称、用户邮箱组合确定的
def gen_barcode_md5(text):
	m = hashlib.md5()
	m.update(text)
	result = m.hexdigest()
	# 加密以后取前六位 
	return result[:6]

# 确保content是一个带唯一身份认证的url信息，扫描后可直接点击
def get_bar_code(salon_id, barcode):
	checkin_url = check_in_url % (str(salon_id), str(barcode))
	urllib.urlretrieve(google_chart_api_url + str(checkin_url), 
			'barcode_images/' + str(salon_id) + '_' + str(barcode) + '.png')


# send mail to developers according to task info
def send_mail(salon_name, user_name, barcode):

	# email, with attachment
	msg_root = MIMEMultipart()

	# encoding 
	msg_root["Accept-Language"] = "zh-CN"
	msg_root["Accept-Charset"]="ISO-8859-1,utf-8"

	# email message
	file_content = '''
		<p>%s，您好：<p>
		<p style='margin-left:2em'>欢迎来到人人FED技术沙龙</p>
		<p style='margin-left:2em'>您的二维码是 %s </p>
		<hr><img src="cid:bar_code_image">
		''' % (user_name, str(barcode))
	text_msg = MIMEText(file_content, 'html', 'utf-8')
	msg_root.attach(text_msg)

 	# append barcode image file as attachment
	image_file = get_png_file_path(salon_name, user_name, barcode)
	image_content = open(image_file, 'rb').read();
	image_att = MIMEImage(image_content, 'png')
	image_att.add_header('Content-Disposition', 'attachment', filename='barcode.png')
	image_att.add_header('Content-ID', '<bar_code_image>')    
	msg_root.attach(image_att)

	# to
	to_list = ('zhifu.wang@renren-inc.com', 'wentao.zhang@renren-inc.com;')
	# to_list = 'zhifu.wang@renren-inc.com'

	# from
	me = 'no-reply.fed' + "<no-reply.fed@renren-inc.com>"

	# other 
	msg_root['subject'] = Header('欢迎来到人人FED技术沙龙-标题', 'utf-8')  
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

def get_png_file_path(salon_name, user_name, barcode):
	return 'barcode_images/' + str(salon_name) + '_' + str(barcode) + '.png'

if __name__ == '__main__':
	get_bar_code('RENREN', 'F32321D')
	get_bar_code('FED', 'FDKJ32123')

	send_mail('RENREN', 'test', 'F32321D')
	send_mail('FED', 'test', 'FDKJ32123')

	print gen_barcode_md5('FED_Salon_wangjeaf_wangjeaf@gmail.com')

