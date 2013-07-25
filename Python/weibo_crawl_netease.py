#! /usr/bin/env python
#coding=utf-8


from config import *
from utils import store_category, weibo_logger, weibo_date_str_to_datetime, store_error

import json
from t4py.tblog.tblog import TBlog
from t4py.http.oauth import OAuthToken


CONSUMER_KEY = 'mz2K4oGDKyWE3CFF'
CONSUMER_SECRET = 'n6z7CHKXKv7OOSp4nG0dKjgNT5AHRTz5'

token_str = 'oauth_token_secret=f4c70e9c470c67608e44041292d58b48&oauth_token=00dd97236502b7eb6d0e49ad16ad0dce'


t = TBlog(CONSUMER_KEY, CONSUMER_SECRET)
t._request_handler.access_token = OAuthToken.from_string(token_str)


NETEASE_WEIBO_INFO_SOURCE_ID = 8


def get_token():
    t = TBlog(CONSUMER_KEY, CONSUMER_SECRET)
    print t.get_auth_url() #copy the url to your browser and get PIN number
    verifier = raw_input('PIN: ').strip() #input PIN number
    return t.get_access_token(verifier)  


def search_for_new_statuses():
    previous_real_count = session.query(Status).filter(Status.info_source_id==NETEASE_WEIBO_INFO_SOURCE_ID).count()

    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = NETEASE_WEIBO_INFO_SOURCE_ID

    for keyword in KEYWORDS : 
        search_statuses = t.statuses_search({'q':keyword.str.encode('utf8')})
        statuses = json.loads(search_statuses)

        count = count + len(statuses)

        for status in statuses:
            add_status_and_user_to_session(status, keyword.id)

    current_real_count = session.query(Status).filter(Status.info_source_id==NETEASE_WEIBO_INFO_SOURCE_ID).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()



def add_status_and_user_to_session(status, keyword_id):
    user = status['user']
    if user is None or status['text'] is None: #Exception
        return

    sql_user = session.query(User).filter(User.user_origin_id==str(user['id']),
                                          User.info_source_id==NETEASE_WEIBO_INFO_SOURCE_ID).first()
    if not sql_user:
        sql_user = User()

    sql_user.user_origin_id = str(user['id'])
    sql_user.info_source_id = NETEASE_WEIBO_INFO_SOURCE_ID
    sql_user.screen_name = user['screen_name']
    sql_user.profile_image_url = user['profile_image_url']
    sql_user.status_count = user['statuses_count']
    sql_user.follower_count = user['followers_count']
    sql_user.following_count = user['friends_count']
    sql_user.verified = user['verified']
    if user['gender'] == '1':
        sql_user.gender = 'm'
    elif user['gender'] == '2':
        sql_user.gender = 'f'
    else:
        sql_user.gender = 'n'
    location = location_split(user['location'])
    sql_user.geo_info_province = location['province']
    sql_user.geo_info_city = location['city']

    
    sql_status = session.query(Status).filter(Status.weibo_origin_id==status['id'], Status.info_source_id==NETEASE_WEIBO_INFO_SOURCE_ID).first()
    if not sql_status:
        sql_status = Status()

    sql_status.weibo_origin_id = int(status['id']) 
    sql_status.url = "http://t.163.com/" + user['id'] + "/status/" + status['id']
    sql_status.weibo_user_screen_name = user['screen_name']
    sql_status.keyword_id = keyword_id
    sql_status.info_source_id = NETEASE_WEIBO_INFO_SOURCE_ID
    sql_status.text = status['text']
    sql_status.created_at = weibo_date_str_to_datetime(status['created_at'])
    sql_status.repost_count = status['retweet_count']
    sql_status.comment_count = status['comments_count']
    sql_status.attitude_count = 0
    if status['in_reply_to_status_id'] != None:
        sql_status.retweeted = True
    else:
        sql_status.retweeted = False

    sql_status.with_pic = False

    sql_status.geo_info_province = location['province']
    sql_status.geo_info_city = location['city']


    sql_status.user = sql_user #foreign key
    
    session.merge(sql_status) #merge

    session.flush()
    session.commit()

    sql_status = session.query(Status).filter(Status.weibo_origin_id==status['id'],
                                 Status.info_source_id==NETEASE_WEIBO_INFO_SOURCE_ID).first()
    if sql_status:
        store_category('weibo', str(sql_status.id))



def location_split(location_str):
    array = location_str.split(',')
    if len(array) == 2:
        return {'province':array[0], 'city':array[1]}
    else:
        return {'province':u'其它', 'city':u''}


def refresh_monitoring_status():
    #monitoring_statuses = session.query(MonitoringStatus)
    monitoring_statuses = session.query(MonitoringStatus,Status).join(Status).filter(Status.info_source_id==NETEASE_WEIBO_INFO_SOURCE_ID)

    for row in monitoring_statuses:
        if row.MonitoringStatus.expiring_at >= datetime.now(): #expired
            update_by_weibo_id(row.MonitoringStatus.weibo_status_id,
                               row.Status.weibo_origin_id)
            time.sleep(1)


def update_by_weibo_id(id, origin_id):
    status = t.statuses_show({'id': str(origin_id)})
    api_status = json.loads(status)
    sql_status = session.query(Status).get(id)

    sql_status.repost_count = api_status['retweet_count']
    sql_status.comment_count = api_status['comments_count']
    
    session.commit()
    
    store_category('weibo', str(sql_status.id))


def main():
    try:
        search_for_new_statuses()
        refresh_monitoring_status()
    except Exception, e:
        store_error(NETEASE_WEIBO_INFO_SOURCE_ID)
        weibo_logger.exception(e)


if __name__ == '__main__':
    main()
