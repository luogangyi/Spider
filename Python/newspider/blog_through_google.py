#! /usr/bin/env python
#coding=utf8
#update by lgy ,2013.08.03
from BaseBBS import *
from blog_utils import *
from google_search import Google

if __name__=="__main__":
    try:
        obj = Google(WY163_BLOG_INFO_SOURCE_ID,'blog.163.com','blog')
        obj.main()
    except Exception, e:
        store_error(WY163_BLOG_INFO_SOURCE_ID)
        blog_logger.exception(e)

    try:
        obj = Google(Cnfol_BLOG_INFO_SOURCE_ID,'blog.cnfol.com','blog')
        obj.main()
    except Exception, e:
        store_error(Cnfol_BLOG_INFO_SOURCE_ID)
        blog_logger.exception(e)

    try:
        obj = Google(EastMoney_Blog_BLOG_INFO_SOURCE_ID,'blog.eastmoney.com','blog')
        obj.main()
    except Exception, e:
        store_error(EastMoney_Blog_BLOG_INFO_SOURCE_ID)
        blog_logger.exception(e)
        
    try:
        obj = Google(HexunBlog_BLOG_INFO_SOURCE_ID,'blog.hexun.com','blog')
        obj.main()
    except Exception, e:
        store_error(HexunBlog_BLOG_INFO_SOURCE_ID)
        blog_logger.exception(e)

    try:
        obj = Google(BlogChina_Blog_BLOG_INFO_SOURCE_ID,'blogchina.com','blog')
        obj.main()
    except Exception, e:
        store_error(BlogChina_Blog_BLOG_INFO_SOURCE_ID)
        blog_logger.exception(e)






