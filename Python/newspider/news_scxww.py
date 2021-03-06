#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
from google_search import Google
from baidu import Baidu
from BaseNews import *
from news_utils import *

SOURCENAME = "四川新闻网"
class SCXWW(BaseNews):
    def __init__(self,sourceId):
        BaseNews.__init__(self,sourceId)

     #in this situation, override to set url 
    def nextPage(self,keyword):

        url = 'http://www.jike.com/so?q=%s&site=newssc.org&trade_id=6541630579976406454&se_type=4' % (keyword.str.encode('utf-8'))
        response = urllib2.urlopen(url)
        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content)

        items = soup.find("ul",id="toolLink")
        if items == None:
            return []
        items = items.findAll("li")
 
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        url = item.div.a['href']
        title = item.div.a.text

        readCount = commentCount = 0
        content =  item.p.text

        createdAt = self.convertTime(item.span.text)

        username = ""
        print url, SOURCENAME, title, content,createdAt
        add_news_to_session(url, SOURCENAME, title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)

    
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
            return strtime

def main(id):
    try:
        obj =  SCXWW(id)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)
    # try:
    #     obj = Baidu(id,'newssc.org','news',SOURCENAME)
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)

    # try:
    #     obj = Google(id,'newssc.org','news',SOURCENAME)
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)
  
  

if __name__ == "__main__":
    main(SCXWW_NEWS_INFO_SOURCE_ID)
    
