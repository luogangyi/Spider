#!/usr/bin/env python
# encoding: utf-8

import urllib
import urllib2
import httplib2
import time
from BeautifulSoup import BeautifulSoup

def hot(): 
    http = httplib2.Http()
         
    baseurl = 'http://data.weibo.com/top/ajax/influence'
    
    headers = {
        'Origin': 'http://data.weibo.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://data.weibo.com/top/influence/'
    }
    
    
    url = baseurl
    data = {'page': '1', 'class': '29', 'type': 'day', 'depart': '0001',
                'level': '0', 'open': '', '_t': 0}      
    data = urllib.urlencode(data)  
    req = urllib2.Request(url, data, headers)  
    response = urllib2.urlopen(req)  
    content = response.read() 

    #print content
    content = content.replace(r'\"',r'"') 
    content = content.replace(r'\/',r'/') 
    soup = BeautifulSoup(content)

    imgs = soup.findAll('img', attrs={'class' : "photo_zw"}) 
    for img in imgs:
        url = img['src']
        start = url.find('cn/')
        end = url.find('/50/')
        print url
        print url[start+3:end]




def main():
    hot()


if __name__ == '__main__':
    main()


