#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
#fix a bug of title
from google_search import Google
from baidu import Baidu
from BaseNews import *
from news_utils import *

SOURCENAME = "中国新闻网四川新闻"
class ScChinaNews(BaseNews):

    def nextPage(self,keyword):

        url = 'http://www.sc.chinanews.com.cn/uda/SearchInfo.aspx?txtkey=%s' % (keyword.str.encode('utf8'))
        print url
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)

        # items = soup.find('div',id="SearchList")
        # if items== None:
        #     return []
        items = soup.findAll("li")
        # print len(items)
        return items
    

    def itemProcess(self,item):

        url = item.find('a')['href']
        url = self.getCompleteURL('http://www.sc.chinanews.com.cn/',url)
        createdAt = self.convertTime(item.contents[-1])
        
        
        content = self.getDetailPage(url)
        soup = BeautifulSoup(content)
        
        news_nr = soup.find('div',{'class':'news_nr'})
        title = news_nr.find('div',{'class':'new_h1'})
        #print news_nr.prettify()

        if title != None:
            title = title.text
            timeAndSource = soup.find('div',{'class':'new_txtct'})('span')
        #print title
        else:
            title = news_nr.h1.text
        
        content = soup.find('div',id='newbody').text
        if len(content) >256:
            content = content[0:255]
        print url, SOURCENAME, title, content,createdAt
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
        m = re.search(u'\w*：(\w*)',sourceName)
        return m.group(1)
        
def main(id):
    try:
        obj = ScChinaNews(id)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)

    # try:
    #     obj = Baidu(id,'sc.chinanews.com.cn','news',SOURCENAME)
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)

    # try:
    #     obj = Google(id,'sc.chinanews.com.cn','news',SOURCENAME)
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)
    
if __name__=="__main__":
    main(SCCHINA_NEWS_INFO_SOURCE_ID)
#    dt = datetime.strptime("[2010-12-04T10:30:53]", "[%Y-%m-%dT%H:%M:%S]")
#    print dt

    

        

