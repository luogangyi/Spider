#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
# fix convertTime bug by lgy.
from google_search import Google
from baidu import Baidu
from BaseNews import *
from news_utils import *

SOURCENAME = "四川电视台"
class SCTVBBS(BaseNews):
    def __init__(self,sourceId):
        BaseNews.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):

        url = 'http://www.baidu.com/baidu?word=%s&tn=bds&cl=3&ct=2097152&si=sctv.com&ie=utf-8&x=29&y=10' % keyword.str.encode('utf-8')
        response = urllib2.urlopen(url)
        content = response.read()
        #just need to visit once, because it is order by time in default
        
        soup = BeautifulSoup(content)

        items = soup.findAll("td", attrs={'class':'f'})      
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):

        url = item('a')[0]["href"]
        response = urllib2.urlopen(url)
        url = response.geturl()
        title = item.h3.a.text
        #print title
        #there is not readcount and commentcount， so let both be None
        readCount = commentCount = None
 
    
        content = content = item.find('div', attrs={'class':'c-abstract'}).text

        createdAt = self.convertTime(item.find('span', attrs={'class':'g'}).text)

        username = None
        #print url,SOURCENAME , title, content,createdAt
        add_news_to_session(url,SOURCENAME , title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)

    def convertTime(self,strtime):
        now = datetime.now()
        pattern = re.compile(r"(\d+-\d+-\d+)")
        m = pattern.search(strtime)
        if m != None :
            return m.group(1)
        #print m.group(1)
        pattern = re.compile(r"(\d+)")
        m = pattern.search(strtime)
        if m == None :
            return -1
        else:
            m = m.group(1)
        #print strtime
        if strtime.find(u'年')>-1:  
            return -1
        elif strtime.find(u'月')>-1:
            time = now-timedelta(days=(int(m)*30))
        elif strtime.find(u'天')>-1: 
            time =  now-timedelta(days=int(m))
        elif strtime.find(u'小时')>-1:
            time =  now-timedelta(hours=int(m))
        else:
            time = now
        return time.strftime("%Y-%m-%d")

def main(id):
    try:
        obj = SCTVBBS(id)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)
    # try:
    #     obj = Baidu(id,'sctv.com','news',SOURCENAME)
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)
    # try:
    #     obj = Google(id,'sctv.com','news',SOURCENAME)
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)

if __name__ == "__main__":
    main(SCTV_NEWS_INFO_SOURCE_ID)

    

        
        