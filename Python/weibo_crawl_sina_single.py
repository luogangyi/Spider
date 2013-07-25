#! /usr/bin/env python
#coding=utf-8
'''
Created on 2013-5-25

@author: founder
''' 

from config import *

from utils import weibo_date_str_to_datetime
from sina_api import APIClient
import urllib
import urllib2
from locations import CITIES


ACCOUNT = 'founder.fy@gmail.com'
PASSWORD = 'founder2014'

CALLBACK_URL = 'http://www.tbs-info.com/callback'
AUTH_URL = 'https://api.weibo.com/oauth2/authorize'
TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'

WEIBO_DESKTOP_APP_KEY = '140226478'
WEIBO_DESKTOP_APP_SECRET = '42fcc96d3e64d9e248649369d61632a6'

client = APIClient(app_key=WEIBO_DESKTOP_APP_KEY, app_secret=WEIBO_DESKTOP_APP_SECRET, redirect_uri=CALLBACK_URL)

#授权
def auth(client):
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
        params = resp.read()
        # print params
        access_token = params.split(",")[0].split(":")[1].split('"')[1]
        expires_in = params.split(",")[2].split(":")[1]
        uid = params.split(",")[3].split(":")[1].split('"')[1]
        # print access_token
        # print uid
        client.set_access_token(access_token, expires_in)  
    except Exception, e:
        print e

#访问限制
def getAccessLimit(client):
    r = client.account.rate_limit_status.get()
    return r

def get_repost_statuses(id):
    r = client.statuses.count.get(ids=id)
    for st in r:
        rep = st.reposts

    #每次最多获取200条，根据转发数目，确定页码
    maxPage = rep/200 + 1
    statuses = []
    print 'maxPage: '+str(maxPage)
    for i in range(1, maxPage+1):  
        r = client.statuses.repost_timeline.get(id=id,count='200',page=i)
        statuses = statuses + r.reposts

    return statuses


def save_source_status(status):
    sql_user = get_sql_user(status)
    if sql_user == None:
        return None

    sql_status = session.query(SingleSourceStatus).filter(SingleSourceStatus.origin_id==str(status['id'])).first()
    if not sql_status:
        sql_status = SingleSourceStatus()

    sql_status.origin_id = str(status['id']) 
    sql_status.url = "http://weibo.com/" + sql_user.origin_id + "/" + id2mid(status['idstr'])
    sql_status.created_at = weibo_date_str_to_datetime(status['created_at'])
    sql_status.text = status['text']
    sql_status.reposts_count = status['reposts_count']
    sql_status.comments_count = status['comments_count']
    sql_status.attitudes_count = status['attitudes_count']
    sql_status.source_app = status['source']
    if status.has_key('original_pic'):
        sql_status.pic = status['original_pic']

    sql_status.single_weibo_user = sql_user

    return sql_status


def save_repost(status, sql_source_status, repost_depth, direct_reposts_count, parent_origin_id):
    sql_user = get_sql_user(status)
    if sql_user == None:
        return
    
    sql_status = session.query(SingleRepostStatus).filter(SingleRepostStatus.origin_id==str(status['id'])).first()
    if not sql_status:
        sql_status = SingleRepostStatus()

    sql_status.origin_id = str(status['id']) 
    sql_status.url = "http://weibo.com/" + sql_user.origin_id + "/" + id2mid(status['idstr'])
    sql_status.created_at = weibo_date_str_to_datetime(status['created_at'])
    sql_status.text = status['text']
    sql_status.reposts_count = status['reposts_count']
    sql_status.comments_count = status['comments_count']
    sql_status.attitudes_count = status['attitudes_count']
    sql_status.source_app = status['source']
    if status.has_key('original_pic'):
        sql_status.pic = status['original_pic']

    sql_status.repost_depth = repost_depth
    sql_status.direct_reposts_count = direct_reposts_count
    sql_status.parent_origin_id = parent_origin_id

    sql_status.single_weibo_user = sql_user

    sql_status.single_source_status = sql_source_status

    session.merge(sql_status)
    #session.flush()
    #session.commit()


def get_sql_user(status):
    user = status['user']
    if user is None or status['text'] is None: #Exception
        return None

    sql_user = session.query(SingleWeiboUser).filter(SingleWeiboUser.origin_id==str(user['id'])).first()
    if not sql_user:
        sql_user = SingleWeiboUser()

    sql_user.origin_id = str(user['id'])
    sql_user.screen_name = user['screen_name']
    sql_user.bi_followers_count = user['bi_followers_count']
    sql_user.followers_count = user['followers_count']
    sql_user.friends_count = user['friends_count']
    sql_user.statuses_count = user['statuses_count']
    sql_user.description = user['description']
    sql_user.profile_image_url = user['profile_image_url']
    sql_user.profile_url = user['profile_url']
    sql_user.verified_type = get_verified_type(user['verified_type'])
    sql_user.created_at = weibo_date_str_to_datetime(user['created_at'])
    sql_user.gender = user['gender']
    location = locationId2Str(user['province'], user['city'])
    sql_user.province = location['province']
    sql_user.city = location['city']

    # 先提交 防重复
    session.merge(sql_user)
    session.flush()
    session.commit() 

    sql_user = session.query(SingleWeiboUser).filter(SingleWeiboUser.origin_id==str(user['id'])).first()
    if not sql_user:
        return None

    return sql_user



def locationId2Str(province_id, city_id):
    try:
        cities = CITIES[province_id]
        return {'province':cities['name'], 'city':cities[city_id]}
    except KeyError:
        return {'province':u'其它', 'city':u''}


def get_verified_type(verified_type_id):
    if verified_type_id == -1:
        return u'普通用户'
    elif verified_type_id == 0: #黄V
        return u'名人'
    elif verified_type_id == 1: #以下为蓝V
        return u'政府'
    elif verified_type_id == 2:
        return u'企业'
    elif verified_type_id == 3:
        return u'媒体'
    elif verified_type_id == 4:
        return u'校园'
    elif verified_type_id == 5:
        return u'网站'
    elif verified_type_id == 6:
        return u'应用'
    elif verified_type_id == 7:
        return u'团体（机构）'
    elif verified_type_id == 8:
        return u'待审企业'
    elif verified_type_id == 200: # 以下为达人
        return u'初级达人'
    elif verified_type_id == 220:
        return u'中高级达人'
    elif verified_type_id == 400: #
        return u'已故V用户'
    else:
        return u'未知'

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



def repost_part(id, sql_source_status):
    # 转发
    statuses = get_repost_statuses(id)
            
    ids = []
    depth = dict()
    for i in range(0,len(statuses)):
        st = statuses[i]

        # 字典格式 idstr:[reposts_count, repost_depth, index, repost_statuses, direct_reposts_count, parent_id]
        depth.update({st.idstr:[st.reposts_count, 1, i, None, 0, None]})

    
    for (k,v) in depth.items(): 
        if v[0] > 0: #有转发的继续搜索
            temp_statuses = get_repost_statuses(k)
            v[3] = temp_statuses
            for temp_st in temp_statuses:
                if depth.has_key(temp_st.idstr):
                    # 层数加1
                    depth[temp_st.idstr][1] = depth[temp_st.idstr][1] + 1
                else:
                    print "Not exist"
        else:
            v[3] = []
            

    for (k,v) in depth.items(): 
        if v[0] > 0:
            temp_statuses = v[3]
            origin_repost_depth = v[1]
            direct_reposts_count = 0
            for temp_st in temp_statuses:
                if depth.has_key(temp_st.idstr):
                    if depth[temp_st.idstr][1] == origin_repost_depth + 1:
                        direct_reposts_count = direct_reposts_count + 1
                        depth[temp_st.idstr][5] = k # 确认父亲节点
                    
            v[4] = direct_reposts_count


    #print depth
    for (k,v) in depth.items(): 
        index = v[2]
        repost_depth = v[1]
        st = statuses[index]
        direct_reposts_count = v[4]
        parent_origin_id = v[5]
        print repost_depth,v[0],direct_reposts_count, parent_origin_id

        save_repost(st, sql_source_status, repost_depth, direct_reposts_count, parent_origin_id)

    session.flush()
    session.commit()


def comment_part(id, sql_source_status):
    # 评论 
    comments = get_comments(id)

    for comment in comments:
        save_comment(comment, sql_source_status)

    session.flush()
    session.commit()


def save_comment(comment, sql_source_status):
    sql_user = get_sql_user(comment)
    if sql_user == None:
        return
    
    sql_comment = session.query(SingleComment).filter(SingleComment.origin_id==str(comment['id'])).first()
    if not sql_comment:
        sql_comment = SingleComment()

    sql_comment.origin_id = str(comment['id'])
    sql_comment.created_at = weibo_date_str_to_datetime(comment['created_at'])
    sql_comment.text = comment['text']
    sql_comment.source_app = comment['source']

    sql_comment.single_weibo_user = sql_user

    sql_comment.single_source_status = sql_source_status

    session.merge(sql_comment)
    #session.flush()
    #session.commit()


def get_comments(id):
    r = client.statuses.count.get(ids=id)
    for st in r:
        com = st.comments

    #每次最多获取200条，根据评论数目，确定页码
    maxPage = com/200 + 1
    comments = []
    print 'maxPage: '+str(maxPage)
    for i in range(1, maxPage+1):  
        r = client.comments.show.get(id=id,count='200',page=i)
        comments = comments + r.comments

    return comments



def main(): 
    auth(client)

    #s = '3597846311362964'
    s = '3599683735626207'

    source_status = client.statuses.show.get(id=s)
    sql_source_status = save_source_status(source_status)
    if sql_source_status == None:
        return

    session.merge(sql_source_status)
    session.flush()
    session.commit()

    sql_source_status = session.query(SingleSourceStatus).filter(SingleSourceStatus.origin_id==source_status['idstr']).first()
    
    if not sql_source_status:
        return

    #repost_part(s, sql_source_status)

    comment_part(s, sql_source_status)
    

if __name__ == '__main__':
    main()
