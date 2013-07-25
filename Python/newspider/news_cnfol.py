#! /usr/bin/env python
#coding=utf-8
#OK
from BaseTimeLimit import *
from news_utils import *

SOURCENAME = "中金资讯"
class CnfolNews(BaseBBS):
    '''中金博客   http://blog.cnfol.com/ —— 按文章搜索 属于news故存入news表'''
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    def nextPage(self,keyword):
        try:
            url = 'http://search.cnfol.com/%s/article/1/10' % (keyword.str.encode('utf8'))
            #print url
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)
            
            btsz = soup.findAll('div',{'class':'btsz'})
            btszx = soup.findAll('div',{'class':'btszx'})
            nrsz = soup.findAll('div',{'class':'nrsz'})
            
            items = []
            for (i,t) in enumerate(btsz):
                items.append([t,btszx[i],nrsz[i]])
            
            #print len(items)
            return items
        except:
            return []
    
    def itemProcess(self,item):
        try:
            a = item[0].a
            url  = a['href']
            title = a.text
            createdAt = self.convertTime(item[1].text)
            content = item[2].text

            add_news_to_session(url, SOURCENAME, title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
        except Exception, e:
            print e
        
        
        
    def convertTime(self,createdAt):
        m = re.search(r'\d+-\d+-\d+ \d+:\d+',createdAt)
        return datetime.strptime(m.group(),'%Y-%m-%d %H:%M')

def main(id):
    obj = CnfolNews(id)
    obj.main()
    
        
if __name__=="__main__":
    obj = CnfolNews(48)
    obj.main()

