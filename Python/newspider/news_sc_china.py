#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
from google_search import Google
from baidu import Baidu
from BaseBBS import *
from news_utils import *

SOURCENAME = "中国新闻网四川新闻"
class ScChinaNews(BaseBBS):

    def nextPage(self,keyword):
        try:
            url = 'http://www.sc.chinanews.com.cn/uda/SearchInfo.aspx?txtkey=%s' % (keyword.str.encode('utf8'))
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)
        except:
            return []
 
#        print content
        try:
            items = soup.find("ul").findAll("li")
        except:# there is not any result,so return empty list
            return []
#        print items
        return items
    

    def itemProcess(self,item):

        url = item.find('a')['href']
        url = self.getCompleteURL('http://www.sc.chinanews.com.cn/',url)
 
        createdAt = self.convertTime(item.contents[-1])
        
        
        content = self.getDetailPage(url)
        soup = BeautifulSoup(content)
        
        soup = soup.find('div',{'class':'news_nr'})
        
        
        
        title = soup.find('div',{'class':'news_h1'}).text
        #print title
        timeAndSource = soup.find('div',{'class':'new_txtct'})('span')

        sourceName = self.getSourceName(timeAndSource[1].text)
        content = soup.find('div',id='newbody').text
        #print url, sourceName, title, content,createdAt
        add_news_to_session(url, SOURCENAME, title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)

    
    def getDetailPage(self,url):
        return urllib2.urlopen(url).read()
    
    def setIsFinished(self,createdAt):
        if createdAt < self.lasttime:
            self.isFinished = True
        return self.isFinished
    
    def getCompleteURL(self,host,url):
        if url.find('http')>-1:
            return url
        else:
            return host+url
    def convertTime(self,createdAt):
        return datetime.strptime(createdAt,'[%Y-%m-%d]')
            
    def getSourceName(self,sourceName):
        m = re.match(r'\w*:(\w*)',sourceName)
        return m.group(1)
        
def main(id):
    try:
        obj = ScChinaNews(id)
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    try:
        obj = Baidu(id,'sc.chinanews.com.cn','news',SOURCENAME)
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    
if __name__=="__main__":
    main(38)
#    dt = datetime.strptime("[2010-12-04T10:30:53]", "[%Y-%m-%dT%H:%M:%S]")
#    print dt

    

        

