#! /usr/bin/env python
#coding=utf-8

from config import *
from utils import store_category, news_logger, baidu_date_str_to_datetime, store_error
from news_utils import *


def main():
    try:
        search_for_google_news_posts(KEYWORDS, GOOGLE_NEWS_INFO_SOURCE_ID)
    except Exception, e:
        news_logger.exception(e) 
        store_error(GOOGLE_NEWS_INFO_SOURCE_ID)


if __name__ == '__main__':
    main()
