# -*-coding: utf8 -*-
import urllib
import urllib2

data = {'mobile': '18651899924',
        'msg': '测试python'
}
        
url = "http://fudafirm.sinaapp.com/sms.php?" + urllib.urlencode(data)

headers = {
            'Host': 'fudafirm.sinaapp.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
}
    
req = urllib2.Request(url, headers = headers)  
response = urllib2.urlopen(req)  
content = response.read() 
print content
