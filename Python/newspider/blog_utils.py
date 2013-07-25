#! /usr/bin/env python
#coding=utf-8

from config import *
from utils import store_category


def store_blog_post(url, blog_user_screen_name, title, content, info_source_id,
                   keyword_id, created_at, read_count, comment_count):
    try:
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
    except:
        print "store_blog_post error"
