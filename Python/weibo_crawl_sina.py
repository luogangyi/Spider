#! /usr/bin/env python
#coding=utf-8
# update by lgy 2014.3.11

from config import *

import math
from utils import *
from sina_api import APIClient
from locations import CITIES


ACCOUNT = 'yoyoworms@gmail.com'
PASSWORD = '880924'
CODE = '8d77cabdd56bc7034447518881bbe34c'
ACCESS_TOKEN = '2.00lodWMD0cbl_xbb19ae8b5aeb8JiD'
EXPIRES_IN = '1354647601'

APP_KEY = '876515056'
APP_SECRET = '6c5ac8344a1b092e025bbce912acfe52'
AUTH_URL = 'https://api.weibo.com/oauth2/authorize'
TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'
CALLBACK_URL = 'http://www.tbs-info.com/callback'

APPLE_APP_KEY = '31024382'
APPLE_APP_SECRET = '25c3e6b5763653d1e5b280884b45c51f'
APPLE_ACCESS_TOKEN = '2.00lodWMD0QrKGC75955e2cddR4KXVB'
APPLE_EXPIRES_IN = '7788166'
    

WEIBO_DESKTOP_APP_KEY = '140226478'
WEIBO_DESKTOP_APP_SECRET = '42fcc96d3e64d9e248649369d61632a6'

WEIBO_DESKTOP_ACCESS_TOKEN = '2.00lodWMD05_4UJa09171967eVCaRgB'
WEIBO_DESKTOP_EXPIRES_IN = '7202005'

client = APIClient(app_key=WEIBO_DESKTOP_APP_KEY, app_secret=WEIBO_DESKTOP_APP_SECRET, redirect_uri=CALLBACK_URL)
client.set_access_token(WEIBO_DESKTOP_ACCESS_TOKEN, WEIBO_DESKTOP_EXPIRES_IN)

SEARCH_INFO_SOURCE_ID = 1
HOT_INFO_SOURCE_ID = 5
BAIDU_INFO_SOURCE_ID = 6


def get_code():
    conn = httplib.HTTPSConnection('api.weibo.com')
    postdata = urllib.urlencode({'client_id':APP_KEY,
                                 'response_type':'code',
                                 'redirect_uri':CALLBACK_URL,
                                 'action':'submit',
                                 'userId':ACCOUNT,
                                 'passwd':PASSWORD,
                                 'isLoginSina':0,
                                 'from':'',
                                 'regCallback':'',
                                 'state':'',
                                 'ticket':'',
                                 'withOfficalFlag':0})
    
    conn.request('POST','/oauth2/authorize', postdata,{'Referer':'api.weibo.com','Content-Type': 'application/x-www-form-urlencoded'})    
    res = conn.getresponse()

    print res.read()
    print 'headers===========',res.getheaders()
    print 'msg===========',res.msg
    print 'status===========',res.status
    print 'reason===========',res.reason
    print 'version===========',res.version
    
    location = res.getheader('location')
    print location
    code = location#.split('=')[1]
    conn.close()
    
    print code
    
    return code

def get_code2():
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    referer_url = client.get_authorize_url()
    print "referer url is : %s" % referer_url
 
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    urllib2.install_opener(opener)
 
    postdata = {"client_id": APP_KEY,
                "redirect_uri": CALLBACK_URL,
                "userId": ACCOUNT,
                "passwd": PASSWORD,
                "isLoginSina": "0",
                "action": "submit",
                "response_type": "code",
               }
 
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
               "Host": "api.weibo.com",
               "Referer": referer_url
              }
 
    req = urllib2.Request(
                           url = AUTH_URL,
                           data = urllib.urlencode(postdata),
                           headers = headers
                           )
    try:
        resp = urllib2.urlopen(req)
        print resp.read()
        print "callback url is : %s" % resp.geturl()
        print "code is : %s" % resp.geturl()[-32:]
    except Exception, e:
        print e


def hackApp():
    postdata = {"client_id": WEIBO_DESKTOP_APP_KEY,
                "client_secret": WEIBO_DESKTOP_APP_SECRET,
                "grant_type": "password",
                "username": ACCOUNT,
                "password": PASSWORD,
               }
 
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
               "Host": "api.weibo.com",
               "Referer": CALLBACK_URL,
              }

    req = urllib2.Request(
                           url = TOKEN_URL,
                           data = urllib.urlencode(postdata),
                           headers = headers
                           )
    try:
        resp = urllib2.urlopen(req)
        print resp.read()
        print "callback url is : %s" % resp.geturl()
    except Exception, e:
        print e
 


'''
API Search Part

'''
    
def search_for_new_statuses():
    previous_real_count = session.query(Status).filter(Status.info_source_id==SEARCH_INFO_SOURCE_ID).count()

    lasttime = session.query(Job).filter(Job.info_source_id==SEARCH_INFO_SOURCE_ID).order_by(Job.id.desc()).first()
    deltatime = lasttime.previous_executed - timedelta(hours=2)
    starttime = time.mktime(deltatime.timetuple())
    #print lasttime
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = SEARCH_INFO_SOURCE_ID

    for keyword in KEYWORDS : 
        search_statuses = client.search.statuses.get(q=keyword.str, count=50, starttime=starttime)
        statuses = search_statuses['statuses']

        count = count + len(statuses)
        #print count

        for status in statuses:
            add_status_and_user_to_session(status, keyword.id)


        time.sleep(5)
    
    
    current_real_count = session.query(Status).filter(Status.info_source_id==SEARCH_INFO_SOURCE_ID).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()




'''
Scrawl Hot Part

'''
def get_hots():
    previous_real_count = session.query(Status).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = HOT_INFO_SOURCE_ID

    URL_ID_LIST = ['1099', '1199', '1299', '1399', '1499', '1599', '1699',
                   '1799','1899', '1999', '2099', '2199']

    for url_id in URL_ID_LIST:
        for page_id in range(1,11): 
            url = 'http://hot.weibo.com/?v=%s&page=%d'%(url_id, page_id)


            headers = {
                'Host': 'hot.weibo.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
                'Referer': 'http://hot.weibo.com/'
            }
        
            req = urllib2.Request(url, headers = headers)  
            response = urllib2.urlopen(req)  
            content = response.read() 
        
            soup = BeautifulSoup(content)
        
            
            weibos = soup.findAll('div', attrs={'class': "WB_text"})
            for weibo in weibos:
                keyword_id = keyword_match(weibo.text)

                if keyword_id > 0:
                    weibo_id = weibo.parent.parent.parent['mid']
                    store_by_weibo_id(weibo_id, keyword_id)
                    count = count + 1
                    

    current_real_count = session.query(Status).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit() 


'''
Scrawl Baidu Search Part

'''

def get_baidu_search_result():
    try:
        previous_real_count = session.query(Status).count()
        count = 0
        sql_job = Job()
        sql_job.previous_executed = datetime.now()
        sql_job.info_source_id = BAIDU_INFO_SOURCE_ID

        for keyword in KEYWORDS :
            data = {'wd': keyword.str.encode('utf8'),
                    'pn': 0,
                    'cl': 2,
                    'tn': 'baiduwb',
                    'ie': 'utf-8',
                    'rtt': 2,
                    'wb': 4
                   }
            
            url = "http://www.baidu.com/s?" + urllib.urlencode(data)
            
            headers = {
                'Host': 'www.baidu.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
                'Referer': 'http://www.baidu.com/'
            }
        
            req = urllib2.Request(url, headers = headers)  
            response = urllib2.urlopen(req)  
            content = response.read() 
        
            soup = BeautifulSoup(content)
        
            weibos = soup.findAll('p', attrs={'class': "info m"})
            count = count + len(weibos)

            for weibo in weibos:
                address = weibo.a['href'][20:]
                start = address.find('/')
                end = address.find('?t=')
                mid = address[start+1:end]

                store_by_weibo_mid(mid, keyword.id)


        current_real_count = session.query(Status).count()

        sql_job.fetched_info_count = count
        sql_job.real_fetched_info_count = current_real_count - previous_real_count

        session.add(sql_job)
        session.flush()
        session.commit()    
    except Exception, e:
        print e

'''
Refresh Following Part
'''

def refresh_monitoring_status():
    #monitoring_statuses = session.query(MonitoringStatus)
    monitoring_statuses = session.query(MonitoringStatus,Status).join(Status).filter(Status.info_source_id == SEARCH_INFO_SOURCE_ID)

    for row in monitoring_statuses:
        if row.MonitoringStatus.expiring_at >= datetime.now(): #expired
            update_by_weibo_id(row.MonitoringStatus.weibo_status_id,
                               row.Status.weibo_origin_id)
            time.sleep(1)

'''
Common Usage

'''

def add_status_and_user_to_session(status, keyword_id):
    user = status['user']
    if user is None or status['text'] is None: #Exception
        return

    sql_user = session.query(User).filter(User.user_origin_id==str(user['id']), User.info_source_id==SEARCH_INFO_SOURCE_ID).first()
    if not sql_user:
        sql_user = User()

    sql_user.user_origin_id = str(user['id'])
    sql_user.info_source_id = SEARCH_INFO_SOURCE_ID
    sql_user.screen_name = user['screen_name']
    sql_user.profile_image_url = user['profile_image_url']
    sql_user.status_count = user['statuses_count']
    sql_user.follower_count = user['followers_count']
    sql_user.following_count = user['friends_count']
    sql_user.verified = user['verified']
    sql_user.gender = user['gender']
    location = locationId2Str(user['province'], user['city'])
    sql_user.geo_info_province = location['province']
    sql_user.geo_info_city = location['city']

    
    sql_status = session.query(Status).filter(Status.weibo_origin_id==status['id'], Status.info_source_id==SEARCH_INFO_SOURCE_ID).first()
    if not sql_status:
        sql_status = Status()

    sql_status.weibo_origin_id = status['id'] 
    sql_status.url = "http://weibo.com/" + str(user['id']) + "/" + id2mid(status['idstr'])
    sql_status.weibo_user_screen_name = user['screen_name']
    sql_status.keyword_id = keyword_id
    sql_status.info_source_id = SEARCH_INFO_SOURCE_ID
    sql_status.text = status['text']
    sql_status.created_at = weibo_date_str_to_datetime(status['created_at'])
    sql_status.repost_count = status['reposts_count']
    sql_status.comment_count = status['comments_count']
    sql_status.attitude_count = status['attitudes_count']
    if status.has_key('retweeted_status'):
        sql_status.retweeted = True
    else:
        sql_status.retweeted = False

    if status.has_key('thumbnail_pic'):
        sql_status.with_pic = True
        sql_status.pic_address = status['thumbnail_pic']
    else:
        sql_status.with_pic = False

    sql_status.geo_info_province = location['province']
    sql_status.geo_info_city = location['city']

    # print sql_user.screen_name,sql_status.text 

    sql_status.user = sql_user #foreign key
    
    session.merge(sql_status) #merge

    session.flush()
    session.commit()


    sql_status = session.query(Status).filter(Status.weibo_origin_id==status['id'],
                                 Status.info_source_id==SEARCH_INFO_SOURCE_ID).first()
    
    if sql_status:
        store_category('weibo', str(sql_status.id))

def search_for_new_statuses_from_baidu():
    previous_real_count = session.query(Status).filter(Status.info_source_id==SEARCH_INFO_SOURCE_ID).count()

    lasttime = session.query(Job).filter(Job.info_source_id==SEARCH_INFO_SOURCE_ID).order_by(Job.id.desc()).first()
    deltatime = lasttime.previous_executed - timedelta(hours=2)
    starttime = time.mktime(deltatime.timetuple())

    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = info_source_id

    http://www.baidu.com/s?wd=%E7%A9%B7%E4%BA%BA&tn=baiduwb&wb=4&cl=2&rtt=2&ie=utf-8&rn=20
    for keyword in KEYWORDS :
        page = 0
        finished = False
        while(not finished):
            data = {'wd': keyword.str.encode('utf-8'),
                    'tn': 'baiduwb',
                    #'from':'news',
                    'ie': 'utf-8',
                    'rtt': 2,
                    'cl': 2,
                    'rn': 20,
                    'wb': 4, 
                    'pn': page
                   }
            
            url = "http://www.baidu.com/s?" + urllib.urlencode(data)
            page = page + 20

            headers = {
                'Host': 'news.baidu.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'
            }
    
            req = urllib2.Request(url, headers = headers)  
            response = urllib2.urlopen(req)  
            content = response.read() 
    
            soup = BeautifulSoup(content, fromEncoding="utf-8")
            #print soup.prettify()
            li_table = soup.find('ol', attrs={'id': 'weibo'})
            news_tables = soup.findAll('li')
            # res = soup.findAll('p', attrs={'class': 'res'})
            # news_tables =[]
            # for contents in res:
            #     news = contents.findAll('span')
            #     if len(news)>0:
            #         news_tables = news
            #         break


            count = count + len(news_tables)
            #print len(news_tables)
            if len(news_tables) <20:
                finished = True
                time.sleep(5)

            for news_table in news_tables:
                li_id = news_table['id']
                if li_id<pn-20:
                    finished = True
                    time.sleep(5)
                    break  
                url = news_table.a['href']
                title = news_table.a.text
                source_and_date = news_table.findAll('span', attrs={'class': 'c-author'})[-1].text.replace('&nbsp;',' ').split()
                content = ""

                source_name = source_and_date[0]
                #print news_table.findAll('span', attrs={'class': 'c-author'})[-1].text.replace('&nbsp;',' ')
                if len(source_and_date) == 3:
                    date = source_and_date[1] + ' ' + source_and_date[2]
                else:
                    date = source_and_date[0]
                try:
                    created_at = baidu_date_str_to_datetime(date)
                except:
                    created_at =  datetime.now()

                #print last_time,created_at,(last_time-created_at).days
                #check time!! 
                if (last_time-created_at).days>1 :
                    finished = True
                    time.sleep(5)
                    break
                #check time!!    
                # if created_at < last_time:
                #     finished = True
                #     time.sleep(5)
                #     break
                sql_status = session.query(Status).filter(Status.weibo_origin_id==status['id'], Status.info_source_id==SEARCH_INFO_SOURCE_ID).first()
                if not sql_status:
                    sql_status = Status()

                sql_status.weibo_origin_id = status['id'] 
                sql_status.url = "http://weibo.com/" + str(user['id']) + "/" + id2mid(status['idstr'])
                sql_status.weibo_user_screen_name = user['screen_name']
                sql_status.keyword_id = keyword_id
                sql_status.info_source_id = SEARCH_INFO_SOURCE_ID
                sql_status.text = status['text']
                sql_status.created_at = weibo_date_str_to_datetime(status['created_at'])
                sql_status.repost_count = status['reposts_count']
                sql_status.comment_count = status['comments_count']
                sql_status.attitude_count = status['attitudes_count']
                if status.has_key('retweeted_status'):
                    sql_status.retweeted = True
                else:
                    sql_status.retweeted = False

                if status.has_key('thumbnail_pic'):
                    sql_status.with_pic = True
                    sql_status.pic_address = status['thumbnail_pic']
                else:
                    sql_status.with_pic = False

                sql_status.geo_info_province = location['province']
                sql_status.geo_info_city = location['city']

                # print sql_user.screen_name,sql_status.text 

                sql_status.user = sql_user #foreign key
                
                session.merge(sql_status) #merge

                session.flush()
                session.commit()


                sql_status = session.query(Status).filter(Status.weibo_origin_id==status['id'],
                                             Status.info_source_id==SEARCH_INFO_SOURCE_ID).first()
                
                if sql_status:
                    store_category('weibo', str(sql_status.id))


            time.sleep(5)

def store_by_weibo_mid(mid, keyword_id):
    try:
        status = client.statuses.show.get(id=mid2id(mid))
        add_status_and_user_to_session(status, keyword_id)
    except Exception: #APIError
        pass

def store_by_weibo_id(idstr, keyword_id):
    try:
        status = client.statuses.show.get(id=int(idstr))
        add_status_and_user_to_session(status, keyword_id)
    except Exception: #APIError
        pass

def update_by_weibo_id(id, origin_id):
    try:
        api_status = client.statuses.show.get(id=origin_id)
        sql_status = session.query(Status).get(id)

        sql_status.repost_count = api_status['reposts_count']
        sql_status.comment_count = api_status['comments_count']
        sql_status.attitude_count = api_status['attitudes_count']
        
        session.commit()
        
        store_category('weibo', str(sql_status.id))


    except Exception: #APIError
        pass


def id2mid(id):
    mid = ''
    while len(id) > 7:
        tmp = id[-7:]
        result = base62_encode(int(tmp))
        while len(result) < 4:
            result = '0' + result
        mid = result + mid
        id = id[0:-7]

    mid = base62_encode(int(id)) + mid
    return mid 

def base62_encode(num):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
          rem = num % base
          num = num // base
          arr.append(alphabet[rem])
    arr.reverse()     #数组翻转
    return ''.join(arr)


def base62_decode(mid):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base = len(alphabet)
    strlen = len(mid)
    num = 0

    idx = 0
    for char in mid:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return str(num)


def mid2id(mid):
    num = ''
    while len(mid) > 4:
        tmp = mid[-4:]
        num_str = base62_decode(tmp)
        while len(num_str) < 7:
            num_str = '0' + num_str

        num = num_str + num
        mid = mid[0:-4]

    num = base62_decode(mid) + num
    return int(num)

def keyword_match(text):
    for keyword in KEYWORDS: 
        words = keyword.str.split(' ')

        keyword_found = True
        for word in words: 
            if text.find(word) < 0:
                keyword_found = False
                break

        if keyword_found:
            return keyword.id

    return 0

def locationId2Str(province_id, city_id):
    try:
        cities = CITIES[province_id]
        return {'province':cities['name'], 'city':cities[city_id]}
    except KeyError:
        return {'province':u'其它', 'city':u''}

    statuses = session.query(Status)
   
    for row in statuses:
        print "sss"
        store_category('weibo', str(row.id))


def main():
    # get_code()
    # hackApp()
    # client = APIClient(app_key=WEIBO_DESKTOP_APP_KEY, app_secret=WEIBO_DESKTOP_APP_SECRET, redirect_uri=CALLBACK_URL)
    # r = client.request_access_token(CODE)
    # access_token = r.access_token # 新浪返回的token，类似abc123xyz456
    # expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4

    # client.set_access_token(WEIBO_DESKTOP_ACCESS_TOKEN, WEIBO_DESKTOP_EXPIRES_IN)

    # try:
    #     search_for_new_statuses()
    #     #get_baidu_search_result()
    #     refresh_monitoring_status()
    #     #get_hots()
    # except Exception, e:
    #     store_error(SEARCH_INFO_SOURCE_ID)
    #     weibo_logger.exception(e)


if __name__ == '__main__':
    main()


