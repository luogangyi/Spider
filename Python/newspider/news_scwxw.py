#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29
from google_search import Google
from baidu import Baidu
from news_utils import *

def main(id):
    try:
        obj = Baidu(id,'scwx.newssc.org','news','四川外宣网')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)

if __name__=="__main__":
    main(55)