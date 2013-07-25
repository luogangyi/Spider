#! /usr/bin/env python
#coding=utf-8

from BaseTimeLimit import *
from blog_utils import *
from news_cnfol import CnfolNews

class CnfolBlog(CnfolNews):
    '''中金博客   http://blog.cnfol.com/ —— 按博客搜索 属于blog故存入blog_posts表'''
    def __init__(self,sourceId):
        CnfolNews.__init__(self,sourceId)
    
    def nextPage(self,keyword):
        try:
            url = 'http://search.cnfol.com/%s/blog/1/10' % (keyword.str.encode('utf8'))
          
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)
            
            btsz = soup.findAll('div',{'class':'btsz'})
            btszx = soup.findAll('div',{'class':'btszx'})
            nrsz = soup.findAll('div',{'class':'nrsz'})
            
            items = []
            for (i,t) in enumerate(btsz):
                items.append([t,btszx[i],nrsz[i]])
            
           
            return items
        except:
            return []
    
    def itemProcess(self,item):
        
        try:
            a = item[0].a
            url  = a['href']
            title = a.text
            #print title
            createdAt = self.convertTime(item[1].text)
            content = item[2].text
        
            store_blog_post(url,"", title, content,
                                self.INFO_SOURCE_ID,self.keywordId, createdAt, 0,0)
        except Exception, e:
            print e
    
def main(id):
    obj = CnfolBlog(id)
    obj.main()
    
        
if __name__=="__main__":
    obj = CnfolBlog(43)
    obj.main()

#ok