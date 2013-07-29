#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
from baidu import Baidu
from BaseTimeLimit import *
from news_utils import *

SOURCENAME="成都商报"
class EChengduNews(BaseTimeLimit):
    def __init__(self,sourceId):
        BaseTimeLimit.__init__(self,sourceId)
    
    def nextPage(self,keyword):

        url = 'http://so.chengdu.cn/?words=%s&sortmode=2&tn=&cwords=&twords=&inid=0&indexid=0&mtach=2' % (keyword.str.encode('utf8'))
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)
 

        items = soup.find("table",id='ires-table')
        if items == None:
            return []
        items= items.findAll("tr")
        return items
    
    def itemProcess(self,item):
        createdAt = self.convertTime(item.td.h3.span.text)

        a = item.td.h3.a
        title =a.text

        url = a['href']
        content = item.td.p.text
        #print url, SOURCENAME, title, content,createdAt
        add_news_to_session(url, SOURCENAME, title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)


    def convertTime(self,createdAt):
        try:
            return datetime.strptime(createdAt,'%Y-%m-%d')
        except:
            return datetime.strptime(createdAt,'%Y-%m-%d %H:%M')
        
def main(id):
    try:
        obj = EChengduNews(id)
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    try:
        obj = Baidu(id,'chengdu.cn','news',SOURCENAME )
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    
if __name__=="__main__":
    main(39)

