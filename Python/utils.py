#! /usr/bin/env python
#coding=utf-8

import time
import urllib2
from datetime import datetime
import logging  
from config import *


def baidu_date_str_to_datetime(date_str):
    if len(date_str) > 17:
        temp = datetime(*(time.strptime(date_str, '%Y-%m-%d %H:%M:%S')[0:6]))
    elif len(date_str) > 13:
        temp = datetime(*(time.strptime(date_str, '%Y-%m-%d %H:%M')[0:6]))
    else:
        temp = datetime(*(time.strptime(date_str, '%Y-%m-%d')[0:6]))
    return temp
    

def weibo_date_str_to_datetime(date_str):
    temp = datetime(*(time.strptime(date_str, '%a %b %d %H:%M:%S +0800 %Y')[0:6]))
    return temp


def store_category(info_type, idstr):
    #url = "http://localhost:8080/soya/classifier/run?info=%s&id=%s" % (info_type, idstr)

    url = "http://localhost:3010/classify/%s/%s" % (info_type, idstr)
    #print url

    response = urllib2.urlopen(url)  
    content = response.read() 

    #content

def store_error(info_source_id):
    sql_job_error = JobError()
    sql_job_error.happened_at = datetime.now()
    sql_job_error.info_source_id = info_source_id

    session.add(sql_job_error)
    session.flush()
    session.commit()


def recheck_title(keyword, title):
    keywords = keyword.str.split()
    for key in keywords:
        if key =='':
            continue
        if title.find(key)<0:
            return False
    return True


# Logging Part
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  

weibo_logger = logging.getLogger('weibo_logger')  
weibo_file_handler = logging.FileHandler(PYTHON_DIR + 'log/weibo.log')  
weibo_logger.setLevel(logging.INFO)  
weibo_file_handler.setLevel(logging.INFO)  
weibo_file_handler.setFormatter(formatter)  
weibo_logger.addHandler(weibo_file_handler)

bbs_logger = logging.getLogger('bbs_logger')  
bbs_file_handler = logging.FileHandler(PYTHON_DIR + 'log/bbs.log')  
bbs_logger.setLevel(logging.INFO)  
bbs_file_handler.setLevel(logging.INFO)
bbs_file_handler.setFormatter(formatter)  
bbs_logger.addHandler(bbs_file_handler)

news_logger = logging.getLogger('news_logger')  
news_file_handler = logging.FileHandler(PYTHON_DIR + 'log/news.log')  
news_logger.setLevel(logging.INFO)  
news_file_handler.setLevel(logging.INFO)  
news_file_handler.setFormatter(formatter)  
news_logger.addHandler(news_file_handler)

wiki_logger = logging.getLogger('wiki_logger')  
wiki_file_handler = logging.FileHandler(PYTHON_DIR + 'log/wiki.log')  
wiki_logger.setLevel(logging.INFO)  
wiki_file_handler.setLevel(logging.INFO)  
wiki_file_handler.setFormatter(formatter)  
wiki_logger.addHandler(wiki_file_handler)

blog_logger = logging.getLogger('blog_logger')  
blog_file_handler = logging.FileHandler(PYTHON_DIR + 'log/blog.log')  
blog_logger.setLevel(logging.INFO)  
blog_file_handler.setLevel(logging.INFO)  
blog_file_handler.setFormatter(formatter)  
blog_logger.addHandler(blog_file_handler)


video_logger = logging.getLogger('video_logger')  
video_file_handler = logging.FileHandler(PYTHON_DIR + 'log/video.log')  
video_logger.setLevel(logging.INFO)  
video_file_handler.setLevel(logging.INFO)  
video_file_handler.setFormatter(formatter)  
video_logger.addHandler(video_file_handler)
