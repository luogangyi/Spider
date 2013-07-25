#! /usr/bin/env python
#coding=utf-8
#OK
from BaseTimeLimit import *
from news_utils import *

SOURCENAME = '和讯资讯'
class HexunNews(BaseBBS):
    '''和讯博客  http://blog.hexun.com/—— 按资讯搜索 属于news故存入news表'''
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    def nextPage(self,keyword):
        try:
            url = 'http://news.search.hexun.com/cgi-bin/search/info_search.cgi?f=0&key=%s&s=1&pg=1&t=0' % (keyword.str.encode('gbk'))
    #        print url
            content = urllib2.urlopen(url).read()
    #        print content
            soup = BeautifulSoup(content)
        except:
            return []
#        print soup.find("div",{'class':'search_result'})
        try:
            items = soup.find("div",{'class':'search_result'}).find('div',{"class":'list'}).ul.findAll('li',recursive=False)
        except:# there is not any result,so return empty list
            return []
#        print len(items)
        return items
    
    def itemProcess(self,item):
        try:
            ult = item.find('div',{'class':'ul_t'})
            a = ult.find('a')
            url  = a['href']
            title = a.text
            title = self.deleteTag(title)
            createdAt = self.convertTime(ult.h4.text)
            content = item.find('div',{'class':'cont'}).text
            content = self.deleteTag(content)

            add_news_to_session(url, SOURCENAME, title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
        except Exception, e:
            print e

        
        
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
    obj = HexunNews(id)
    obj.main()
    
        
if __name__=="__main__":
    obj = HexunNews(Hexun_INFO_SOURCE_ID)
    obj.main()


