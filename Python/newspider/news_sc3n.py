#! /usr/bin/env python
#coding=utf-8
#OK
from BaseBBS import *
from news_utils import *

class Sc3N(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    
    def nextPage(self,keyword):
        try:
            url = 'http://www.baidu.com/baidu?tn=bds&cl=3&ct=2097152&si=sannong.newssc.org&word=' + (keyword.str.encode('gb2312'))
            response = urllib2.urlopen(url)
            content = response.read()
            
            soup = BeautifulSoup(content)
            items = soup.findAll("td", attrs={'class':'f'})
            #print items
        except:
            return []
        return items
    
    def itemProcess(self,item):
        try:
            title = item.h3.a.text
            #print title
            #print title.encode('gbk')
            content = item.find('div', attrs={'class':'c-abstract'}).text
            #print content.encode('gbk')
            url = item.h3.a['href']
            response = urllib2.urlopen(url)
            url = response.geturl()
            
            createdAt = self.convertTime(item.find('span', attrs={'class':'g'}).text.split(' ')[1])
            #print createdAt
            #here, use add_news_to_session instead store_bbs_post
            add_news_to_session(url, '四川三农新闻网', title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
        except Exception, e:
            return
        

    def convertTime(self,time):
        return datetime.strptime(time,'%Y-%m-%d')

def main(id):
    obj = Sc3N(id)
    obj.main()

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
    obj = Sc3N(35)
    obj.main()



