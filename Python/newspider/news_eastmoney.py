#! /usr/bin/env python
#coding=utf-8
#OK
from BaseTimeLimit import *
from news_utils import *

SOURCENAME = "东方财富资讯"
class EastMoneyNews(BaseBBS):
    '''东方财富博客   http://blog.eastmoney.com/—— 按资讯搜索 属于news故存入news表'''
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    def nextPage(self,keyword):
        try:
            url = 'http://so.eastmoney.com/Search.ashx?qw=%s&qt=2&sf=0&st=1&cpn=1&pn=10&f=0&p=0' % (keyword.str.encode('utf8'))

            content = urllib2.urlopen(url).read()
            import json
            js = json.loads(content[content.find('{'):-1])
    #        print content
            try:
                items = js['DataResult']
            except:# there is not any result,so return empty list
                return []

            return items
        except:
            return []
    
    def itemProcess(self,item):
        try:
        
            content = BeautifulSoup(item['Description']).text
            title = BeautifulSoup(item['Title']).text
            add_news_to_session(item['Url'], SOURCENAME, title, content,
                                self.INFO_SOURCE_ID, item['ShowTime'], self.keywordId)
        except Exception, e:
            print e
        
        
        
    def convertTime(self,createdAt):
        return datetime.strptime(createdAt,'%Y-%m-%d')

def main(id):
    obj = EastMoneyNews(id)
    obj.main()
    
            
if __name__=="__main__":
    obj = EastMoneyNews(49)
    obj.main()

