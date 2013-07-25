#! /usr/bin/env python
#coding=utf-8

from config import *
from utils import store_category


SCPEOPLE_INFO_SOURCE_ID = 3
SCCHINA_INFO_SOURCE_ID = 4
EChengdu_INFO_SOURCE_ID = 5
StockSC_INFO_SOURCE_ID = 6
SCTV_INFO_SOURCE_ID = 7
EastMoney_INFO_SOURCE_ID = 8
Cnfol_INFO_SOURCE_ID = 1
Hexun_INFO_SOURCE_ID = 2
BLOG163_INFO_SOURCE_ID = 3
SCXWW_INFO_SOURCE_ID = 3

def add_news_to_session(url, source_name, title, content, info_source_id, created_at, keyword_id):
    try:
        sql_news = session.query(News).filter(News.url==url).first()
        if not sql_news:
            sql_news = News()
        else:
            return

        sql_news.url = url
        sql_news.source_name = source_name
        sql_news.title = title
        sql_news.content = content
        sql_news.info_source_id = info_source_id 
        sql_news.keyword_id = keyword_id
        sql_news.created_at = created_at

        session.merge(sql_news) #merge

        session.flush()
        session.commit()


        sql_news = session.query(News).filter(News.url==url,
                             News.info_source_id==info_source_id).first()
        if sql_news:
            store_category('news', str(sql_news.id))
    except:
        print "add_news_to_session error"
