#! /usr/bin/env python
#coding=utf-8
#update by lgy,2013.8.4

from config import *
from utils import *

SINA_BLOG_INFO_SOURCE_ID = 14
WY163_BLOG_INFO_SOURCE_ID = 41
HexunBlog_BLOG_INFO_SOURCE_ID =42
Cnfol_BLOG_INFO_SOURCE_ID = 43
EastMoney_Blog_BLOG_INFO_SOURCE_ID = 44
BlogChina_Blog_BLOG_INFO_SOURCE_ID = 59

def store_blog_post(url, blog_user_screen_name, title, content, info_source_id,
                   keyword_id, created_at, read_count, comment_count):
    sql_post = session.query(BlogPost).filter(BlogPost.url==url).first()
    if not sql_post:
       sql_post = BlogPost()

    sql_post.info_source_id = info_source_id
    sql_post.url = url
    sql_post.keyword_id = keyword_id
    sql_post.blog_user_screen_name = blog_user_screen_name
    sql_post.created_at = created_at
    sql_post.title = title
    sql_post.content = content
    sql_post.read_count = read_count
    sql_post.comment_count = comment_count

    session.merge(sql_post) #merge

    session.flush()
    session.commit()

    sql_post = session.query(BlogPost).filter(BlogPost.url==url).first()
    if sql_post:
        store_category('blog', str(sql_post.id))

