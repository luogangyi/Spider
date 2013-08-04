#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
from google_search import Google
from baidu import Baidu
from BaseNews import *
from news_utils import *

SOURCENAME = '和讯资讯'
class HexunNews(BaseNews):
    '''和讯博客  http://blog.hexun.com/—— 按资讯搜索 属于news故存入news表'''
    def __init__(self,sourceId):
        BaseNews.__init__(self,sourceId)
    
    def nextPage(self,keyword):

        url = 'http://news.search.hexun.com/cgi-bin/search/info_search.cgi?f=0&key=%s&s=1&pg=1&t=0' % (keyword.str.encode('gbk'))

        content = urllib2.urlopen(url).read()

        soup = BeautifulSoup(content,fromEncoding='gbk')

        items = soup.find("div",{'class':'search_result'})
        if items == None:
            return []
        items = items.find('div',{"class":'list'})
        if items == None:
            return []
        items = items.ul.findAll('li',recursive=False)
        return items
    
    def itemProcess(self,item):

        ult = item.find('div',{'class':'ul_t'})
        a = ult.find('a')
        url  = a['href']
        title = a.text
        title = self.deleteTag(title)
        createdAt = self.convertTime(ult.h4.text)
        content = item.find('div',{'class':'cont'}).text
        content = self.deleteTag(content)
        #print url, SOURCENAME, title, content,createdAt
        add_news_to_session(url, SOURCENAME, title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)

        
        
    def deleteTag(self,content):
        return BeautifulSoup(content).text
    
    def convertTime(self,strtime):
        now = datetime.now()
        pattern = re.compile(r"\d*")

        if strtime.find(u'天')>-1:
            m = pattern.search(strtime)
            m = m.group()        
            return now-timedelta(days=int(m))
        elif strtime.find(u'小时')>-1:
            m = pattern.search(strtime)
            m = m.group()
            return now-timedelta(hours=int(m))
        else:
            return datetime.strptime(strtime.encode('utf8'),'%Y年%m月%d日 %H:%M')

def main(id):
    try:
        obj = HexunNews(id)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)

    # try:
    #     obj = Baidu(id,'news.hexun.com','news',SOURCENAME )
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)

    # try:
    #     obj = Google(id,'news.hexun.com','news',SOURCENAME )
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)
    
        
if __name__=="__main__":
    main(Hexun_NEWS_INFO_SOURCE_ID)


