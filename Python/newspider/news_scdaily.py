#! /usr/bin/env python
#coding=utf-8
#OK
from baidu import Baidu
from news_utils import *

def main(id):
    #若是博客，则把类型news改为blog
    obj = Baidu(id,'scol.com.cn','news','四川日报')
    obj.main()


if __name__=="__main__":
    main(40)

#    test()
