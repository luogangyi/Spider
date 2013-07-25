#! /usr/bin/env python
#coding=utf-8
#OK
from BaseTimeLimit import *
from news_utils import *

SOURCENAME="成都商报"
class EChengduNews(BaseTimeLimit):
    def __init__(self,sourceId):
        BaseTimeLimit.__init__(self,sourceId)
    
    def nextPage(self,keyword):
        try:
            url = 'http://so.chengdu.cn/?words=%s&sortmode=2&tn=&cwords=&twords=&inid=0&indexid=0&mtach=2' % (keyword.str.encode('utf8'))
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)
     
    #        print content
            try:
                items = soup.find("table",id='ires-table').findAll("tr")
            except:# there is not any result,so return empty list
                return []
    #        print items
            return items
        except:
            return []
    
    def itemProcess(self,item):
        try:
            createdAt = self.convertTime(item.td.h3.span.text)
            #here is important to guarantee the while loop can be over normally
            if self.setIsFinished(createdAt):
                 return
            
            a = item.td.h3.a
            title =a.text
            #print title
            url = a['href']
            content = item.td.p.text

            add_news_to_session(url, SOURCENAME, title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
        except Exception, e:
            print e
        
        
        
    def convertTime(self,createdAt):
        try:
            return datetime.strptime(createdAt,'%Y-%m-%d')
        except:
            return datetime.strptime(createdAt,'%Y-%m-%d %H:%M')
        
def main(id):
    obj = EChengduNews(id)
    obj.main()
    
if __name__=="__main__":
    obj = EChengduNews(39)
    obj.main()
