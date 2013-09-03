#!/usr/bin/python
#-*-coding:utf-8-*-

from config import *
from bbs_utils import *
from utils import *
from baidu import Baidu
from goole_search import Google

MOP_INFO_SOURCE_ID = 20


def main():
    try:
        obj = Baidu(id,'dzh.mop.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)

    try:
        obj = Google(id,'dzh.mop.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)

if __name__ == '__main__':
    main()
