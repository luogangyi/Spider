#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29
from config import *
from utils import store_category


def store_wiki_post(url, wiki_user_screen_name, title, content, info_source_id,
                   keyword_id, created_at, read_count, comment_count, answered):

        sql_post = session.query(WikiPost).filter(WikiPost.url==url).first()
        if not sql_post:
           sql_post = WikiPost()

        sql_post.info_source_id = info_source_id
        sql_post.url = url
        sql_post.keyword_id = keyword_id
        sql_post.wiki_user_screen_name = wiki_user_screen_name
        sql_post.created_at = created_at
        sql_post.title = title
        sql_post.content = content
        sql_post.read_count = read_count
        sql_post.comment_count = comment_count
        sql_post.answered = answered

        session.merge(sql_post) #merge

        session.flush()
        session.commit()
        # sql_post = session.query(WikiPost).filter(WikiPost.url==url).first()
        # if sql_post:
        #     store_category('wiwi', str(sql_post.id))
