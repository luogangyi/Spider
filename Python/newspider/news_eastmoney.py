#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
from baidu import Baidu
from BaseNews import *
from news_utils import *
from google_search import Google

SOURCENAME = "东方财富资讯"
class EastMoneyNews(BaseNews):
    '''东方财富博客   http://blog.eastmoney.com/—— 按资讯搜索 属于news故存入news表'''
    def __init__(self,sourceId):
        BaseNews.__init__(self,sourceId)
    
    def nextPage(self,keyword):

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

    
    def itemProcess(self,item):

        
        content = BeautifulSoup(item['Description']).text
        title = BeautifulSoup(item['Title']).text
        #print item['Url'], SOURCENAME, title, content,item['ShowTime']
        add_news_to_session(item['Url'], SOURCENAME, title, content,
                            self.INFO_SOURCE_ID, item['ShowTime'], self.keywordId)

        
        
    def convertTime(self,createdAt):
        return datetime.strptime(createdAt,'%Y-%m-%d')

def main(id):
    try:
        obj = EastMoneyNews(id)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)

    # try:
    #     obj = Baidu(id,'blog.eastmoney.com','news',SOURCENAME )
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)

    # try:
    #     obj = Google(id,'blog.eastmoney.com','news',SOURCENAME )
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)

    
            
if __name__=="__main__":
    main(EastMoney_NEWS_INFO_SOURCE_ID)
