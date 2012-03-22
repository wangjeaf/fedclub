#python
#encoding=utf-8

import urllib

def get_bar_code(content):
	urllib.urlretrieve('http://chart.apis.google.com/chart?cht=qr&chs=150x150&chl=' + str(content), 
			str(content) + '.jpg')

if __name__ == '__main__':
	get_bar_code(1234)
	get_bar_code('wangjeaf')
