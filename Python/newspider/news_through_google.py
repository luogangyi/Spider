#! /usr/bin/env python
#coding=utf8
#update by lgy ,2013.08.03
from BaseBBS import *
from news_utils import *
from google_search import Google

if __name__ == '__main__':
    try:
        obj = Google(CDWB_NEWS_INFO_SOURCE_ID,'www.cdwb.com.cn','news','成都晚报')
        obj.main()
    except Exception, e:
        store_error(CDWB_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    try:
        obj = Google(CHINAWESTNEWS_NEWS_INFO_SOURCE_ID,'chinawestnews.net','news','中国西部网')
        obj.main()
    except Exception, e:
        store_error(CHINAWESTNEWS_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)


    try:
        obj = Google(EChengDU_NEWS_INFO_SOURCE_ID,'news.chengdu.cn','news',"成都商报" )
        obj.main()
    except Exception, e:
        store_error(EChengDU_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    try:
        obj = Google(Hexun_NEWS_INFO_SOURCE_ID,'news.hexun.com','news','和讯资讯' )
        obj.main()
    except Exception, e:
        store_error(Hexun_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    try:
        obj = Google(HXDSB_NEWS_INFO_SOURCE_ID,'wccdaily.com.cn','news','华西都市报')
        obj.main()
    except Exception, e:
        store_error(HXDSB_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    try:
        obj = Google(SC3N_NEWS_INFO_SOURCE_ID,'sannong.newssc.org','news',"四川三农新闻网")
        obj.main()
    except Exception, e:
        store_error(SC3N_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    try:
        obj = Google(SCCHINA_NEWS_INFO_SOURCE_ID,'sc.chinanews.com.cn','news',"中国新闻网四川新闻")
        obj.main()
    except Exception, e:
        store_error(SCCHINA_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    # try:
    #     obj = Google(SCPeople_NEWS_INFO_SOURCE_ID,'sc.people.com.cn','news',"人民网四川频道")
    #     obj.main()
    # except Exception, e:
    #     store_error(SCPeople_NEWS_INFO_SOURCE_ID)
    #     news_logger.exception(e)

    try:
        obj = Google(SCRB_NEWS_INFO_SOURCE_ID,'scdaily.cn','news',"四川日报" )
        obj.main()
    except Exception, e:
        store_error(SCRB_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    try:
        obj = Google(SCTV_NEWS_INFO_SOURCE_ID,'sctv.com','news',"四川电视台")
        obj.main()
    except Exception, e:
        store_error(SCTV_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    try:
        obj = Google(SCWMW_NEWS_INFO_SOURCE_ID,'www.scwmw.gov.cn','news','四川文明网')
        obj.main()
    except Exception, e:
        store_error(SCWMW_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    try:
        obj = Google(SCWXW_NEWS_INFO_SOURCE_ID,'scwx.newssc.org','news','四川外宣网')
        obj.main()
    except Exception, e:
        store_error(SCWXW_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    try:
        obj = Google(SCXWW_NEWS_INFO_SOURCE_ID,'newssc.org','news',"四川新闻网")
        obj.main()
    except Exception, e:
        store_error(SCXWW_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    try:
        obj = Google(SCZX_NEWS_INFO_SOURCE_ID,'scol.com.cn','news',"四川在线")
        obj.main()
    except Exception, e:
        store_error(SCZX_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    try:
        obj = Google(SINASC_NEWS_INFO_SOURCE_ID,'sc.sina.com.cn','news','新浪四川')
        obj.main()
    except Exception, e:
        store_error(SINASC_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    try:
        obj = Google(STOCKSC_NEWS_INFO_SOURCE_ID,'stocknews.sc.cn','news',"金融投资报")
        obj.main()
    except Exception, e:
        store_error(STOCKSC_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)
  
    try:
        obj = Google(TFZB_NEWS_INFO_SOURCE_ID,'morning.scol.com.cn','news',"天府早报")
        obj.main()
    except Exception, e:
        store_error(TFZB_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)
        
    try:
        obj = Google(XinHuaSC_NEWS_INFO_SOURCE_ID,'www.sc.xinhuanet.com','news','新华网四川频道')
        obj.main()
    except Exception, e:
        store_error(XinHuaSC_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)

    try:
        obj = Google(XNSB_NEWS_INFO_SOURCE_ID,'xnsb.newssc.org','news','西南商报')
        obj.main()
    except Exception, e:
        store_error(XNSB_NEWS_INFO_SOURCE_ID)
        news_logger.exception(e)


