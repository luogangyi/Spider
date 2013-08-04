#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
from BaseTimeLimit import *
from blog_utils import *
from news_cnfol import CnfolNews
from baidu import Baidu
from google_search import Google

class CnfolBlog(CnfolNews):
    '''中金博客   http://blog.cnfol.com/ —— 按博客搜索 属于blog故存入blog_posts表'''
    def __init__(self,sourceId):
        CnfolNews.__init__(self,sourceId)
    
    def nextPage(self,keyword):
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

    
    def itemProcess(self,item):

        a = item[0].a
        url  = a['href']
        title = a.text
        #print title
        createdAt = self.convertTime(item[1].text)
        content = item[2].text
        #print title, content,createdAt
        store_blog_post(url,"", title, content,
                            self.INFO_SOURCE_ID,self.keywordId, createdAt, 0,0)

    
def main(id):
    try:
        obj = CnfolBlog(id)
        obj.main()
    except Exception, e:
        store_error(id)
        blog_logger.exception(e)
    # try:
    #     obj = Baidu(id,'blog.cnfol.com','blog')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     blog_logger.exception(e)
    # try:
    #     obj = Google(id,'blog.cnfol.com','blog')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     blog_logger.exception(e)
    
        
if __name__=="__main__":
    main(Cnfol_BLOG_INFO_SOURCE_ID)
#ok