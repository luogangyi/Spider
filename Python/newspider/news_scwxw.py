#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29
# update by lgy, 2013.7.30, add google search
from google_search import Google
from baidu import Baidu
from news_utils import *

def main(id):
    try:
        obj = Baidu(id,'scwx.newssc.org','news','四川外宣网')
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)
    try:
        obj = Google(id,'scwx.newssc.org','news','四川外宣网')
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)

if __name__=="__main__":
    main(SCWXW_NEWS_INFO_SOURCE_ID)