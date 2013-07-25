#! /usr/bin/env python
#coding=utf-8

from config import *
from utils import news_logger, store_error
from news_utils import *


def main():
    try:
        search_for_baidu_news_posts(KEYWORDS, BAIDU_NEWS_INFO_SOURCE_ID)
    except Exception, e:
        news_logger.exception(e) 
        store_error(BAIDU_NEWS_INFO_SOURCE_ID)


if __name__ == '__main__':
    main()
