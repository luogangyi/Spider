#! /usr/bin/env python
#coding=utf-8

from config import *
from utils import store_category

TIANYA_INFO_SOURCE_ID = 4
BAIDU_TIEBA_INFO_SOURCE_ID = 12
WYSQ_INFO_SOURCE_ID = 26


def store_bbs_post(url, bbs_user_screen_name, title, content, info_source_id,
                   keyword_id, created_at, read_count, comment_count):
    sql_post = session.query(BBSPost).filter(BBSPost.url==url).first()
    if not sql_post:
       sql_post = BBSPost()

    sql_post.info_source_id = info_source_id
    sql_post.url = url
    sql_post.keyword_id = keyword_id
    sql_post.bbs_user_screen_name = bbs_user_screen_name
    sql_post.created_at = created_at
    sql_post.title = title
    sql_post.content = content
    sql_post.read_count = read_count
    sql_post.comment_count = comment_count

    session.merge(sql_post) #merge

    session.flush()
    session.commit()

    sql_post = session.query(BBSPost).filter(BBSPost.url==url).first()
    if sql_post:
        store_category('bbs', str(sql_post.id))
