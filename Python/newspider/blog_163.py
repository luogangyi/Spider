from youdao import Youdao
from blog_utils import *
from utils import *
from baidu import Baidu
from google_search import Google
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
def main(id):
    try:
        obj = Youdao(id,'blog.163.com','blog')
        obj.main()
    except Exception, e:
        store_error(id)
        blog_logger.exception(e)
    try:
        obj = Baidu(id,'blog.163.com','blog')
        obj.main()
    except Exception, e:
        store_error(id)
        blog_logger.exception(e)
    try:
        obj = Google(id,'blog.163.com','blog')
        obj.main()
    except Exception, e:
        store_error(id)
        blog_logger.exception(e)

if __name__=="__main__":
    main(WY163_BLOG_INFO_SOURCE_ID)
