#! /usr/bin/env python
#coding=utf-8

from config import *
from sohu_api import *
from utils import store_category, weibo_logger, weibo_date_str_to_datetime

SOHU_WEIBO_INFO_SOURCE_ID = 9


def search_for_new_statuses():
    previous_real_count = session.query(Status).count()

    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = SOHU_WEIBO_INFO_SOURCE_ID

    for keyword in KEYWORDS : 
        statuses = search_by_keyword(keywords=keyword.str.encode('utf8'))
    
        query_ids = ''
        for status in statuses:
            query_ids = query_ids + ',' + status['id']
        query_ids = query_ids[1:]
        
        time.sleep(2)
        counts = get_count_by_ids(query_ids)

        count = count + len(statuses)

        for i in range(0,len(statuses)):
            if len(counts) < len(statuses):
                weibo_logger.error("sohu weibo request count timeout for request: " + query_ids)
                break

            status = statuses[i]
            temp_count = counts[i]
            add_status_and_user_to_session(status, temp_count, keyword.id)

            time.sleep(5)
       
    current_real_count = session.query(Status).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()



def add_status_and_user_to_session(status, count, keyword_id):
    user = status['user']
    if user is None or status['text'] is None or status['text'] == "@#@_@#@" : #Exception
        return

    sql_user = session.query(User).filter(User.user_origin_id==str(user['id']),
                                          User.info_source_id==SOHU_WEIBO_INFO_SOURCE_ID).first()
    if not sql_user:
        sql_user = User()

    sql_user.user_origin_id = user['id']
    sql_user.info_source_id = SOHU_WEIBO_INFO_SOURCE_ID
    sql_user.screen_name = user['screen_name']
    sql_user.profile_image_url = user['profile_image_url']
    sql_user.status_count = user['statuses_count']
    sql_user.follower_count = user['followers_count']
    sql_user.following_count = user['friends_count']
    sql_user.verified = user['verified']
    sql_user.gender = 'n'
    sql_user.geo_info_province = u'其它'
    sql_user.geo_info_city = u''

    
    sql_status = session.query(Status).filter(Status.weibo_origin_id==status['id'],
                                 Status.info_source_id==SOHU_WEIBO_INFO_SOURCE_ID).first()
    if not sql_status:
        sql_status = Status()

    sql_status.weibo_origin_id = int(status['id']) 
    sql_status.url = "http://t.sohu.com/m/" + status['id']
    sql_status.weibo_user_screen_name = user['screen_name']
    sql_status.keyword_id = keyword_id
    sql_status.info_source_id = SOHU_WEIBO_INFO_SOURCE_ID
    sql_status.text = status['text']
    sql_status.created_at = weibo_date_str_to_datetime(status['created_at'])
    sql_status.repost_count = count['transmit_count']
    sql_status.comment_count = count['comments_count']
    sql_status.attitude_count = 0
    if status.has_key('retweeted_status'):
        sql_status.retweeted = True
    else:
        sql_status.retweeted = False

    if status['middle_pic'] != '':
        sql_status.with_pic = True
        sql_status.pic_address = status['middle_pic']
    else:
        sql_status.with_pic = False

    sql_status.geo_info_province = u'其它'
    sql_status.geo_info_city = u''


    sql_status.user = sql_user #foreign key
    
    session.merge(sql_status) #merge

    session.flush()
    session.commit()

    sql_status = session.query(Status).filter(Status.weibo_origin_id==status['id'],
                                 Status.info_source_id==SOHU_WEIBO_INFO_SOURCE_ID).first()
    if sql_status:
        store_category('weibo', str(sql_status.id))


def refresh_monitoring_status():
    monitoring_statuses = session.query(MonitoringStatus,Status).join(Status).filter(Status.info_source_id==SOHU_WEIBO_INFO_SOURCE_ID)

    for row in monitoring_statuses:
        if row.MonitoringStatus.expiring_at >= datetime.now(): #expired
            update_by_weibo_id(row.MonitoringStatus.weibo_status_id,
                               row.Status.weibo_origin_id)
            time.sleep(1)



def update_by_weibo_id(id, origin_id):
    api_status = get_count_by_ids(str(origin_id))[0]
    sql_status = session.query(Status).get(id)

    sql_status.repost_count = api_status['transmit_count']
    sql_status.comment_count = api_status['comments_count']
    
    session.commit()
    
    store_category('weibo', str(sql_status.id))


def main():
    try:
        search_for_new_statuses()
        refresh_monitoring_status()
    except Exception, e:
        store_error(SOHU_WEIBO_INFO_SOURCE_ID)
        weibo_logger.exception(e)


if __name__ == '__main__':
    main()
