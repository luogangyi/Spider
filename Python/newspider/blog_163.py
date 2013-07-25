from youdao import Youdao
from news_utils import *

def main(id):
    obj = Youdao(id,'blog.163.com','blog')
    obj.main()

if __name__=="__main__":
    obj = Youdao(41,'blog.163.com','blog')
    obj.main()
#    test()


#ok