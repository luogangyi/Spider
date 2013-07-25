#! /usr/bin/env python
#coding=utf-8
#OK
from BaseBBS import *
from news_utils import *

SOURCENAME = "四川电视台"
class SCTVBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        try:
            url = 'http://www.baidu.com/baidu?word=%s&tn=bds&cl=3&ct=2097152&si=sctv.com&ie=utf-8&x=29&y=10' % keyword.str.encode('utf-8')
            response = urllib2.urlopen(url)
            content = response.read()
            #just need to visit once, because it is order by time in default
            
            soup = BeautifulSoup(content)
        except:
            return []
        try:
            items = soup.findAll("td", attrs={'class':'f'})
        except:
            return []
        
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        try:
            url = item('a')[0]["href"]
            response = urllib2.urlopen(url)
            url = response.geturl()
            title = item.h3.a.text
            #print title
            #there is not readcount and commentcount， so let both be None
            readCount = commentCount = None
     
        
            content = content = item.find('div', attrs={'class':'c-abstract'}).text
            #print readCount+" "+commentCount
            #content =  item.find('p',{'class':'content'}).text
            #userInfoTag = item('p')[2]
            #createdAt = userInfoTag.span.text
            createdAt = self.convertTime(item.find('span', attrs={'class':'g'}).text.split(' ')[1])
            #Sprint createdAt
            username = None
             # print username+" "+createdAt
            add_news_to_session(url,SOURCENAME , title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
        except Exception, e:
            print e

def main(id):
    obj = SCTVBBS(id)
    return obj.main()

if __name__ == "__main__":
    obj = SCTVBBS(34)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        