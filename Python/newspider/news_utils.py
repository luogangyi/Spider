#! /usr/bin/env python
#coding=utf-8

from config import *
from utils import *

SCPeople_NEWS_INFO_SOURCE_ID = 33
SCTV_NEWS_INFO_SOURCE_ID = 34
SC3N_NEWS_INFO_SOURCE_ID = 35
SCXWW_NEWS_INFO_SOURCE_ID = 36
SCZX_NEWS_INFO_SOURCE_ID = 37
SCCHINA_NEWS_INFO_SOURCE_ID = 38
EChengDU_NEWS_INFO_SOURCE_ID = 39
STOCKSC_NEWS_INFO_SOURCE_ID = 40
SCRB_NEWS_INFO_SOURCE_ID = 46
TFZB_NEWS_INFO_SOURCE_ID = 47
Cnfol_NEWS_INFO_SOURCE_ID = 48
EastMoney_NEWS_INFO_SOURCE_ID = 49
SINASC_NEWS_INFO_SOURCE_ID = 50
XinHuaSC_NEWS_INFO_SOURCE_ID = 51
SCWMW_NEWS_INFO_SOURCE_ID = 52
CDWB_NEWS_INFO_SOURCE_ID = 53
CHINAWESTNEWS_NEWS_INFO_SOURCE_ID = 54
SCWXW_NEWS_INFO_SOURCE_ID = 55
HXDSB_NEWS_INFO_SOURCE_ID = 56
XNSB_NEWS_INFO_SOURCE_ID = 57
Hexun_NEWS_INFO_SOURCE_ID = 60



def add_news_to_session(url, source_name, title, content, info_source_id, created_at, keyword_id):

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

