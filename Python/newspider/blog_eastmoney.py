#! /usr/bin/env python
#coding=utf-8

from BaseTimeLimit import *
from blog_utils import *
from news_eastmoney import EastMoneyNews
from baidu import Baidu
class EastMoneyBlog(EastMoneyNews):
    '''东方财富博客   http://blog.eastmoney.com/ —— 按博客搜索 属于blog故存入blog_posts表'''
    def __init__(self,sourceId):
        EastMoneyNews.__init__(self,sourceId)
    
    def nextPage(self,keyword):

        url = 'http://so.eastmoney.com/Search.ashx?qw=%s&qt=3&sf=0&st=1&cpn=1&pn=10&f=0&p=0' % (keyword.str.encode('utf8'))
        
        content = urllib2.urlopen(url).read()
        import json
        js = json.loads(content[content.find('{'):-1])
#        print content
        try:
            items = js['DataResult']
        except:# there is not any result,so return empty list
            return []
      
        return items

    def itemProcess(self,item):
        
    
        content = BeautifulSoup(item['Description']).text
        title = BeautifulSoup(item['Title']).text
        #print item['Url'], item['Author'], title, content, item['ShowTime']
        store_blog_post(item['Url'], item['Author'], title, content,
                            self.INFO_SOURCE_ID,self.keywordId, item['ShowTime'],0,0 )

        
        
        
    def convertTime(self,createdAt):
        return datetime.strptime(createdAt,'%Y-%m-%d')
    
def main(id):
    try:
        obj = EastMoneyBlog(id)
        obj.main()
    except Exception, e:
        store_error(id)
        blog_logger.exception(e)

    try:
        obj = Baidu(id,'blog.eastmoney.com','blog')
        obj.main()
    except Exception, e:
        store_error(id)
        blog_logger.exception(e)
    
   

if __name__=="__main__":
    main(EastMoney_Blog_BLOG_INFO_SOURCE_ID)

