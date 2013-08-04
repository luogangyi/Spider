#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
from baidu import Baidu
from BaseNews import *
from news_utils import *
from google_search import Google

SOURCENAME = "中金资讯"
class CnfolNews(BaseNews):
    '''中金博客   http://blog.cnfol.com/ —— 按文章搜索 属于news故存入news表'''
    def __init__(self,sourceId):
        BaseNews.__init__(self,sourceId)
    
    def nextPage(self,keyword):
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

    
    def itemProcess(self,item):

        a = item[0].a
        url  = a['href']
        title = a.text
        createdAt = self.convertTime(item[1].text)
        content = item[2].text
        #print url, SOURCENAME, title, content, createdAt
        add_news_to_session(url, SOURCENAME, title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)

        
        
        
    def convertTime(self,createdAt):
        m = re.search(r'\d+-\d+-\d+ \d+:\d+',createdAt)
        return datetime.strptime(m.group(),'%Y-%m-%d %H:%M')

def main(id):
    try:
        obj = CnfolNews(id)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)
    # try:
    #     obj = Baidu(id,'blog.cnfol.com','news',SOURCENAME )
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)

    # try:
    #     obj = Google(id,'blog.cnfol.com','news',SOURCENAME )
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)



    
        
if __name__=="__main__":
    main(Cnfol_NEWS_INFO_SOURCE_ID)


