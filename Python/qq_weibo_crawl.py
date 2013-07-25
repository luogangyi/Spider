#! /usr/bin/env python
#coding=utf-8

from config import *

from qqweibo import OAuthHandler, API, JSONParser, ModelParser
from utils import store_category, weibo_logger, store_error


API_KEY = '801322882'
API_SECRET = '0f4b0f472813b31c23720623014e22e9'

a = OAuthHandler(API_KEY, API_SECRET)

def get_token():
    print a.get_authorization_url()
    verifier = raw_input('PIN: ').strip()
    print a.get_access_token(verifier)


# or directly use:
#token = 'e9fc735b76ba4e75a6ebaefe61ee66fc'
token = 'd169abff38d747cfa8bdb21123577482'
#tokenSecret = 'ec07bda1b332156d1554470893b16b6d'
tokenSecret = '25d60b4c67c488a4d5291dcb9bd43fd8'
a.setToken(token, tokenSecret)

api = API(a)

QQ_WEIBO_INFO_SOURCE_ID = 7


def search_for_new_statuses():
    previous_real_count = session.query(Status).filter(Status.info_source_id==QQ_WEIBO_INFO_SOURCE_ID).count()

    lasttime = session.query(Job).filter(Job.info_source_id==QQ_WEIBO_INFO_SOURCE_ID).order_by(Job.id.desc()).first()
    deltatime = lasttime.previous_executed - timedelta(hours=2)
    starttime = time.mktime(deltatime.timetuple())
    endtime = time.mktime(datetime.now().timetuple())

    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = QQ_WEIBO_INFO_SOURCE_ID


    for keyword in KEYWORDS : 
        statuses = api.search.tweet(keyword=keyword.str, pagesize=30, page=1,
                                    needdup=1, starttime=starttime,
                                    endtime=endtime)

        count = count + len(statuses)
        for status in statuses:
            add_status_and_user_to_session(status, keyword.id)
            time.sleep(1)

        time.sleep(5)
    
    
    current_real_count = session.query(Status).filter(Status.info_source_id==QQ_WEIBO_INFO_SOURCE_ID).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()


def add_status_and_user_to_session(status, keyword_id):
    user = api.user.userinfo(status.name)

    sql_user = session.query(User).filter(User.user_origin_id==user.name,
                                             User.info_source_id==QQ_WEIBO_INFO_SOURCE_ID).first()
    if not sql_user:
        sql_user = User()

    sql_user.user_origin_id = user.name
    sql_user.info_source_id = QQ_WEIBO_INFO_SOURCE_ID
    sql_user.screen_name = user.nick
    if user.head == "":
        sql_user.profile_image_url = ""
    else:
        sql_user.profile_image_url = user.head + '/100'
    sql_user.status_count = user.tweetnum
    sql_user.follower_count = user.fansnum
    sql_user.following_count = user.idolnum
    sql_user.verified = user.isvip
    if user.sex == 1:
        sql_user.gender = 'm'
    elif user.sex == 2:
        sql_user.gender = 'f'
    else:
        sql_user.gender = 'n'
    location = location_split(user.location)
    sql_user.geo_info_province = location['province']
    sql_user.geo_info_city = location['city']

    
    sql_status = session.query(Status).filter(Status.weibo_origin_id==status.id,
                                                 Status.info_source_id==QQ_WEIBO_INFO_SOURCE_ID).first()
    if not sql_status:
        sql_status = Status()

    sql_status.weibo_origin_id = status.id
    sql_status.url = "http://t.qq.com/p/t/" + str(status.id)
    sql_status.weibo_user_screen_name = user.nick
    sql_status.keyword_id = keyword_id
    sql_status.info_source_id = QQ_WEIBO_INFO_SOURCE_ID
    sql_status.text = status.origtext
    sql_status.created_at = datetime.fromtimestamp(status.timestamp)
    sql_status.repost_count = status.count
    sql_status.comment_count = status.mcount
    sql_status.attitude_count = 0

    if status.type != 1:
        sql_status.retweeted = True
    else:
        sql_status.retweeted = False

    if status.image is None:
        sql_status.with_pic = False
    else:
        sql_status.with_pic = True
        sql_status.pic_address = status.image[0]

    sql_status.geo_info_province = location['province']
    sql_status.geo_info_city = location['city']


    sql_status.user = sql_user #foreign key
    
    session.merge(sql_status) #merge

    session.flush()
    session.commit()

    sql_status = session.query(Status).filter(Status.weibo_origin_id==status.id,
                                                 Status.info_source_id==QQ_WEIBO_INFO_SOURCE_ID).first()
    if sql_status:
        store_category('weibo', str(sql_status.id)) 



def search_for_new_statuses_from_mobile_pages():
    cookie_jar = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36')]
    urllib2.install_opener(opener)

    # get cookie and login url
    cookie_url = '''http://pt.3g.qq.com/s?aid=nLoginmb&g_ut=2'''
    response = opener.open(cookie_url)
    content = response.read()  

    soup = BeautifulSoup(content)

    login_url_input = soup.find('input', attrs={'name':"login_url"})
    login_url = login_url_input['value']

    form = soup.find('form')
    post_url = form['action']

    print post_url
    print cookie_jar

    username = 'tbs.spider.01@qq.com'
    password = 'k3GhB4Wh'

    post_data = urllib.urlencode({'qq':username,
                                  'pwd':password,
                                  'goUrl':'http://ti.3g.qq.com/g/s?aid=h',
                                  'qfrom':'mblog',
                                  'r_sid':'',
                                  'sidtype':1,
                                  'login_url':login_url,
                                })


    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Referer": "http://pt.3g.qq.com/s?aid=nLoginmb&g_ut=2",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Content-Type": "application/x-www-form-urlencoded",
               "Accept-Encoding": "gzip,deflate,sdch",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
               "Host": "pt.3g.qq.com",
               "Connection": "Keep-alive",
               "Cache-Control": "max-age=0",
               "Origin": "http://pt.3g.qq.com"
              }


    req = urllib2.Request(url=post_url,data=post_data,headers=headers)
    response = urllib2.urlopen(req) 
    print response.readlines()
    print response.info() 
    print response.status() 


def location_split(location_str):
    array = location_str.split()
    if len(array) == 2:
        return {'province':u'', 'city':array[1]}
    elif len(array) == 3:
        return {'province':array[1], 'city':array[2]}
    else:
        return {'province':u'其它', 'city':u''}



def refresh_monitoring_status():
    monitoring_statuses = session.query(MonitoringStatus,Status).join(Status).filter(Status.info_source_id==QQ_WEIBO_INFO_SOURCE_ID)

    for row in monitoring_statuses:
        if row.MonitoringStatus.expiring_at >= datetime.now():
            update_by_weibo_id(row.MonitoringStatus.weibo_status_id,
                               row.Status.weibo_origin_id)
            time.sleep(1)


def update_by_weibo_id(id, origin_id):
    try:
        api_status = api.tweet.show(origin_id)
        sql_status = session.query(Status).get(id)

        sql_status.repost_count = api_status.count
        sql_status.comment_count = api_status.mcount
        
        session.commit()
        
        store_category('weibo', str(sql_status.id))

    except Exception, e: #APIError
        store_error(QQ_WEIBO_INFO_SOURCE_ID)
        weibo_logger.exception(e)


def main():
    try:
        search_for_new_statuses()
        refresh_monitoring_status()
    except Exception, e:
        store_error(QQ_WEIBO_INFO_SOURCE_ID)
        weibo_logger.exception(e)

if __name__ == '__main__':
    main()
