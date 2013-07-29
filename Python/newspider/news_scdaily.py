#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 
from baidu import Baidu
from news_utils import *

def main(id):
    try:
        obj = Baidu(id,'scol.com.cn','news','四川日报')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)

if __name__=="__main__":
    main(40)

