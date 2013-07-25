#! /usr/bin/env python
#coding=utf-8
#OK
from BaseBBS import *
from news_utils import *

class SCZX(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    
    def nextPage(self,keyword):
        try:
            url = 'http://zhannei.youdao.com/search?ue=gb2312&keyfrom=web.index&siteId=scol&q=' + (keyword.str.encode('gb2312'))
            response = urllib2.urlopen(url)
            content = response.read()
            content = content.decode('gbk')
            
            soup = BeautifulSoup(content)
        except:
            return []
        try:
            items = soup.find("ol", id="results").findAll("li")
            #print items
        except:
            return []
        return items
    
    def itemProcess(self,item):
        try:
            title = item.div.div.h3.a.text
            #print title.encode('gbk')
            content = item.div.findAll('div')[1].p.text
            #print content.encode('gbk')
            url = item.div.div.h3.a['href']
            #print url
            try:
                createdAt = item.div.findAll('div')[1].div.text.split(' ')[4]
                createdAt = self.convertTime(createdAt)
            except:
                createdAt = datetime.now()
            
            #print createdAt
            #here, use add_news_to_session instead store_bbs_post
            add_news_to_session(url, None, title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
        except Exception, e:
            print e
        

    def convertTime(self,time):
        return datetime.strptime(time,'%Y-%m-%d')

def main(id):
    obj = SCZX(id)
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
    obj = SCZX(37)
    obj.main()



