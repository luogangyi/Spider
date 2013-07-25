#! /usr/bin/env python
#coding=utf-8
#test OK (不按时间排序）

from baidu import Baidu
from news_utils import *

def main(id):
    #若是博客，则把类型news改为blog
    obj = Baidu(id,'www.scwmw.gov.cn','news','四川文明网')
    obj.main()


if __name__=="__main__":
    main(52)