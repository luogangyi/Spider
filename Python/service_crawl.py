#! /usr/bin/env python
#coding=utf-8

from config import *

import math
import xlwt
from api import APIClient
from locations import CITIES

CALLBACK_URL = 'http://www.tbs-info.com/callback'

WEIBO_DESKTOP_APP_KEY = '140226478'
WEIBO_DESKTOP_APP_SECRET = '42fcc96d3e64d9e248649369d61632a6'
WEIBO_DESKTOP_ACCESS_TOKEN = '2.00lodWMD05_4UJ11d36e449cSW7NHB'
WEIBO_DESKTOP_EXPIRES_IN = '7807591'


client = APIClient(app_key=WEIBO_DESKTOP_APP_KEY, app_secret=WEIBO_DESKTOP_APP_SECRET, redirect_uri=CALLBACK_URL)
client.set_access_token(WEIBO_DESKTOP_ACCESS_TOKEN, WEIBO_DESKTOP_EXPIRES_IN)


def get_industry(idstr):
    url = "http://weibo.com/u/" + idstr
    headers = {
        'Host': 'e.weibo.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
    }
    
    req = urllib2.Request(url, headers = headers)  
    response = urllib2.urlopen(req)  

    
    for line in response.readlines():
        index = line.find(r'<dd class=\"W_texta\">')
        if index > 0:
            line = line[index:]
            start = line.find('<p>')
            end = line.find(r'<\/p>')
            return ustr2unicode(line[start+3:end])[3:]

    return u''


def ustr2unicode(input):
    end = len(input)
    pos = 0
    output = u""
    while pos < end:
        if pos <= end - 6 and input[pos] == '\\' and input[pos+1] == 'u':
            output += unichr(int(input[pos+2:pos+6], 16))
            pos = pos + 6
        else:
            output += unicode(input[pos])
            pos += 1    

    return output

def weiboDateStr2DateTime(dateStr):
    temp = datetime(*(time.strptime(dateStr, '%a %b %d %H:%M:%S +0800 %Y')[0:6]))
    return temp

def main():
    print client.users.show.get(uid=1899291080)
    e
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)
    
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'SimSun'    # 指定“宋体”
    style.font = font       

    current_row = 0

    KEYWORDS = [u'服务', u'客服']
    for keyword in KEYWORDS : 
        length = 1
        page = 1
        while length > 0:
            search_users = client.search.users.get(q=keyword, snick=1, sdomain=0,
                                               sintro=0, stag=0, sort=2,
                                                   count=50, page=page)
            length = len(search_users['users'])
            page = page + 1
            for user in search_users['users']:
                if user['name'].find(keyword) < 0:
                    continue

                if user['verified_type'] != 2 and user['verified_type'] != 5:
                    continue

                name = user['name']
                id = user['idstr']
                created_at = weiboDateStr2DateTime(user['created_at'])
                if user['gender'] == 'm':
                    gender = u'男'
                elif user['gender'] == 'f':
                    gender = u'女'
                else:
                    gender = u''

                location = user['location']
                statuses_count = user['statuses_count']
                friends_count = user['friends_count']
                followers_count = user['followers_count']
                industry = get_industry(id)
                
                status_per_day = round(statuses_count*1.0/((datetime.now() - created_at).days),1)

                sheet.write(current_row,0,"http://weibo.com/u/" + id)
                sheet.write(current_row,1,name,style)
                sheet.write(current_row,2,created_at)
                sheet.write(current_row,3,friends_count)
                sheet.write(current_row,4,followers_count)
                sheet.write(current_row,5,statuses_count)
                sheet.write(current_row,6,status_per_day)
                sheet.write(current_row,7,industry,style)
                sheet.write(current_row,8,location,style)
                sheet.write(current_row,9,gender,style)

                print name
                print industry
                print status_per_day
                print ""

                current_row = current_row + 1



            wbk.save('service.xls')


        print page
        


    
    wbk.save('service.xls')

if __name__ == '__main__':
    main()
