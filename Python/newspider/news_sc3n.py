#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
from baidu import Baidu
from BaseBBS import *
from news_utils import *

class Sc3N(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    
    def nextPage(self,keyword):

        url = 'http://www.baidu.com/baidu?tn=bds&cl=3&ct=2097152&si=sannong.newssc.org&word=' + (keyword.str.encode('gb2312'))
        response = urllib2.urlopen(url)
        content = response.read()
        
        soup = BeautifulSoup(content)
        items = soup.findAll("td", attrs={'class':'f'})

        return items
    
    def itemProcess(self,item):

        title = item.h3.a.text
        #print title
        #print title.encode('gbk')
        content = item.find('div', attrs={'class':'c-abstract'}).text
        #print content.encode('gbk')
        url = item.h3.a['href']
        response = urllib2.urlopen(url)
        url = response.geturl()
        
        #print item.find('span', attrs={'class':'g'}).prettify()
        createdAt = self.convertTime(item.find('span', attrs={'class':'g'}).text)
        #print createdAt
        #here, use add_news_to_session instead store_bbs_post
        #print url, '四川三农新闻网', title, content,createdAt
        add_news_to_session(url, '四川三农新闻网', title, content,
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
        obj = Sc3N(id)
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    try:
        obj = Baidu(id,'sannong.newssc.org','news',SOURCENAME)
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)

if __name__=="__main__":
    main(35)




