#! /usr/bin/env python
#coding=utf-8
#test OK (不按时间排序）
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
from baidu import Baidu
from news_utils import *
from google_search import Google

def main(id):
    # try:
    #     obj = Baidu(id,'www.cdwb.com.cn','news','成都晚报')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)

    # try:
    #     obj = Google(id,'www.cdwb.com.cn','news','成都晚报')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)
    return



if __name__=="__main__":
    main(CDWB_NEWS_INFO_SOURCE_ID)