#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
from google_search import Google
from baidu import Baidu
from BaseNews import *
from news_utils import *


SOURCENAME = "人民网四川频道"
class ScPeopleNews(BaseNews):
    def __init__(self,sourceId):
        BaseNews.__init__(self,sourceId)
    
    
    def nextPage(self,keyword):

        url = "http://search.people.com.cn/rmw/GB/rmwsearch/gj_searchht.jsp"
        keyword = keyword.str.encode('utf8')
        data = "basenames=rmwsite&where=(CONTENT%3D("+keyword+")%20or%20TITLE%3D("+keyword+")%20or%20AUTHOR%3D("+keyword+"))%20and%20(CLASS2%3D(%E5%9B%9B%E5%B7%9D%20or%20%E5%9B%9B%E5%B7%9D%E9%A2%91%E9%81%93))&curpage=1&pagecount=20&classvalue=ALL&classfield=CLASS3&isclass=1&keyword=mail&sortfield=-INPUTTIME&_=" 
        
        request = urllib2.Request(url,data=data)
        response = urllib2.urlopen(request)

        content = response.read()
        print content
        soup = BeautifulSoup(content)
        print soup.pretiffy()
        items = soup.findAll('result')

        return items
    
    def itemProcess(self,item):
        print item.pretiffy()
        title = item.title.text
        #print title
        content = item.content.text[21:]
        url = item.docurl.text
        createdAt = self.convertTime(item.publishtime.text)

        #print url, SOURCENAME, title, content,createdAt
        add_news_to_session(url, SOURCENAME, title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)

        

    def convertTime(self,time):
        pattern = re.compile(r'(\d+)\D*(\d+)\D*(\d+)\D*(\d+)\D*(\d+)\D*(\d+)\D*')
        m = pattern.match(time)
        return datetime(int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5)),int(m.group(6)))


def main(id):
    # try:
    #     obj = ScPeopleNews(id)
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)

    try:
        obj = Baidu(id,'people.com.cn','news',SOURCENAME)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)

    try:
        obj = Google(id,'people.com.cn','news',SOURCENAME)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)

if __name__=="__main__":
    main(SCPeople_NEWS_INFO_SOURCE_ID)



