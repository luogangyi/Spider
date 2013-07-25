# -*-coding: utf8 -*-

import urllib
import urllib2
from apibus_handler import APIBusHandler

ACCESSKEY = 'my43y3xm31'
SECRETKEY = '42km5w43xij545515h3zlhlylyly3x5lhj1kx2mx'

apibus_handler = APIBusHandler(ACCESSKEY, SECRETKEY)
opener = urllib2.build_opener(apibus_handler)

'''
print 'call sae segment api:'
chinese_text = '中文文本'
url = 'http://segment.sae.sina.com.cn/urlclient.php?word_tag=1&encoding=UTF-8'
payload = urllib.urlencode([('context', chinese_text),])
print opener.open(url, payload).read()
'''

# sending sms
print 'call sae sms api:'
url = 'http://inno.smsinter.sina.com.cn/sae_sms_service/sendsms.php'
msg = '短信网关测试'
msg = msg.encode("GBK")
payload = urllib.urlencode({'mobile': '18651899924', 'msg': msg, 'encoding': 'GBK'})
print payload
print opener.open(url, payload).read()
