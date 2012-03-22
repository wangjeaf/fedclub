#python
#encoding=utf-8
import smtplib
import email
from email.Utils import formatdate
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.Header import Header  

# send mail to developers according to task info
def send_mail():

	# email, with attachment
	msg_root = MIMEMultipart()

	# encoding 
	msg_root["Accept-Language"] = "zh-CN"
	msg_root["Accept-Charset"]="ISO-8859-1,utf-8"

	# email message
	file_content = '欢迎来到人人FED技术沙龙-内容 \n <hr><img src="cid:bar_code_image">\n'
	text_msg = MIMEText(file_content, 'html', 'utf-8')
	msg_root.attach(text_msg)

 	# append barcode image file as attachment
	image_file = 'wangjeaf.jpg'
	image_content = open(image_file, 'rb').read();
	image_att = MIMEImage(image_content, 'jpg')
	image_att.add_header('Content-Disposition', 'attachment', filename='barcode.jpg')
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

if __name__ == '__main__':
	send_mail();
