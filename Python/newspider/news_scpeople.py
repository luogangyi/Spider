#! /usr/bin/env python
#coding=utf-8
#OK
from BaseBBS import *
from news_utils import *
SOURCENAME = "人民网四川频道"
class ScPeopleNews(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    
    def nextPage(self,keyword):
        try:
            url = "http://search.people.com.cn/rmw/GB/rmwsearch/gj_searchht.jsp"
            keyword = keyword.str.encode('utf8')
            data = "basenames=rmwsite&where=(CONTENT%3D("+keyword+")%20or%20TITLE%3D("+keyword+")%20or%20AUTHOR%3D("+keyword+"))%20and%20(CLASS2%3D(%E5%9B%9B%E5%B7%9D%20or%20%E5%9B%9B%E5%B7%9D%E9%A2%91%E9%81%93))&curpage=1&pagecount=20&classvalue=ALL&classfield=CLASS3&isclass=1&keyword=mail&sortfield=-INPUTTIME&_=" 
            
            request = urllib2.Request(url,data=data)
            response = urllib2.urlopen(request)
    #        print data
            content = response.read()
    #        file = open('out.html','w')
    #        file.write(content)
            
            soup = BeautifulSoup(content)
        except:
            return []
#        print content
        try:
            items = soup.findAll('result')
#            print items
        except:
            return []
        return items
    
    def itemProcess(self,item):
        try:
            title = item.title.text
            #print title
            content = item.content.text[21:]
            url = item.docurl.text
            createdAt = self.convertTime(item.publishtime.text)
        	#print createdAt    
            #here, use add_news_to_session instead store_bbs_post
            add_news_to_session(url, SOURCENAME, title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
        except Exception, e:
            print e
        

    def convertTime(self,time):
        pattern = re.compile(r'(\d+)\D*(\d+)\D*(\d+)\D*(\d+)\D*(\d+)\D*(\d+)\D*')
        m = pattern.match(time)
        return datetime(int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5)),int(m.group(6)))


def main(id):
    obj = ScPeopleNews(id)
    return obj.main()

#def handlexml():
#    file = open('out.html','r')
#    soup = BeautifulSoup(file.read())
##    print soup.prettify()
#    item =soup.find('result')
#    convertTime(item.publishtime.text)
#    
#def convertTime(time):
#    pattern = re.compile(r'(\d+)\D*(\d+)\D*(\d+)\D*(\d+)\D*(\d+)\D*(\d+)\D*')
#    m = pattern.match(time)
#    return datetime(int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5)),int(m.group(6)))
#
if __name__=="__main__":
    obj = ScPeopleNews(33)
    obj.main()



