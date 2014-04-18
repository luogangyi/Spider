#! /usr/bin/env python
#coding=utf-8
# update by lgy, fix a bug. 2013.12.22
from config import *
import json

from qqweibo import OAuthHandler, API, JSONParser, ModelParser
from utils import *


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
    
    #print starttime

    for keyword in KEYWORDS : 
        statuses = search_for_new_statuses_from_mobile_pages(keyword.str, starttime)
        
        # count = count + len(statuses)
        # for status in statuses:
        #     add_status_and_user_to_session(status, keyword.id)
        #     time.sleep(1)

        time.sleep(5)
    
    
    current_real_count = session.query(Status).filter(Status.info_source_id==QQ_WEIBO_INFO_SOURCE_ID).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()


def add_status_and_user_to_session(status, keyword_id):
    #print status.name
    user = api.user.userinfo(status.name)
    print status.name
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



def search_for_new_statuses_from_mobile_pages(keyword, starttime):
    page = 1
    ids = ""

    # default 5 pages, enough for most cases, but can not satisfy special
    # requierments, like history search  
    #print keyworks_encode(keyword,'utf8')
    while page < 6:
        data = {'sid': 'AdA_av4yDo9HipzXLm_SbjWP',
                'aid': 'vaction',
                'mst': 33,
                'ac': 60,
                'shinfo': 'txt.wap_paged.l',
                'shinforen': 'txt.wap_paged.k',
                'keyword': keyword.encode('utf8'),
                'dl2': 1,
                'dumpJSON': 1,
                'pageid': 'search',
                'g_f': 18106,
                'params': 'keyword='.encode('utf8')+keyword.encode('utf8')+'&type=msg'.encode('utf8'),
                'psize': 10,
                'pid': page
               }
        url = "http://ti.3g.qq.com/touch/s?" + urllib.urlencode(data)
        print url
        #print urllib.urlencode({"text":" "}),urllib.urlencode({"text":" ".encode('utf8')})
        headers = {
            'Host': 'ti.3g.qq.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
            'Referer': 'http://bbs.tianya.cn/',          
            'Connection': 'keep-alive',
            'Accept:text/html': 'application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cookie': 'g_ut=2'
        }

        req = urllib2.Request(url, headers = headers)  
        response = urllib2.urlopen(req)  
        content = response.read() 

        results = json.loads(content)
        
        result_list = results["jsonDump"]["msgs"]

        
        for item in result_list:
            #print str(item["msgId"])
            #print api.t.list(ids=str(item["msgId"]))
            try:
                status = api.t.list(ids=str(item["msgId"]))
                add_status_and_user_to_session(status, keyword.id)
                time.sleep(3)
                #ids = ids + "," + str(item["msgId"])
            except:
                continue

        page = page + 1
        time.sleep(1)

    #ids = ids[1:]
    #statuses = api.t.list(ids=ids)
    #print statuses
    #return statuses




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
