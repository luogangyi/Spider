#! /usr/bin/env python
#coding=utf-8
#test OK (不按时间排序）

from baidu import Baidu
from news_utils import *

def main(id):
	try:
        obj = Baidu(id,'www.cdwb.com.cn','news','成都晚报')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)



if __name__=="__main__":
    main(53)