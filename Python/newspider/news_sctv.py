#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
from google_search import Google
from baidu import Baidu
from BaseBBS import *
from news_utils import *

SOURCENAME = "四川电视台"
class SCTVBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):

        url = 'http://www.baidu.com/baidu?word=%s&tn=bds&cl=3&ct=2097152&si=sctv.com&ie=utf-8&x=29&y=10' % keyword.str.encode('utf-8')
        response = urllib2.urlopen(url)
        content = response.read()
        #just need to visit once, because it is order by time in default
        
        soup = BeautifulSoup(content)

        items = soup.findAll("td", attrs={'class':'f'})      
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):

        url = item('a')[0]["href"]
        response = urllib2.urlopen(url)
        url = response.geturl()
        title = item.h3.a.text
        #print title
        #there is not readcount and commentcount， so let both be None
        readCount = commentCount = None
 
    
        content = content = item.find('div', attrs={'class':'c-abstract'}).text

        createdAt = self.convertTime(item.find('span', attrs={'class':'g'}).text.split(' ')[1])

        username = None
        print url,SOURCENAME , title, content,createdAt
        add_news_to_session(url,SOURCENAME , title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)


def main(id):
    try:
        obj = SCTVBBS(id)
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    try:
        obj = Baidu(id,'sctv.com','news',SOURCENAME)
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)


if __name__ == "__main__":
    main(34)

    

        
        