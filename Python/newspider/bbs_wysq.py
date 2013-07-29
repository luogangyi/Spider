#! /usr/bin/env python
#coding=utf-8
#modifeid by lgy,2013.07.20
#测试通过,*网易bbs搜索速度较慢

from BaseBBS import *
from datetime import date
from config import *
from bbs_utils import *
from utils import bbs_logger, store_error
from baidu import Baidu
class WYSQBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url
    # try/except放在顶层main中处理
    def nextPage(self,keyword):
        #print (keyword.str.encode('utf-8'))

        #url = 'http://news.youdao.com/search?q='+(keyword.str.encode('utf-8'))+'&scope=s&keyfrom=rnews.precom' 
        url = 'http://bbs.163.com/bbs/search.do?q='+(keyword.str.encode('utf-8'))+'&searchRan=bbs&boardid=photo&searchType=title'
        response = urllib2.urlopen(url)
        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content)
       # print soup
        items = soup.findAll("div",attrs={"class":re.compile(r"singleResult.*")})
        return items
    


    def convertTime(self,strtime):
        now = datetime.now()

        #time format "2012-11-09 12:13:24"
        pattern = re.compile(r"\d+-\d+-\d+\s+\d+:\d+:\d+")
        m = pattern.search(strtime)
        if m != None:
            return m.group()

        if strtime.find(u'今天')>-1:       
            return now

        elif strtime.find(u'昨天')>-1:       
            return now-timedelta(days=1)

        elif strtime.find(u'前天')>-1:      
            return now-timedelta(days=2)
            
        elif strtime.find(u'天')>-1:
            m = pattern.search(strtime)
            m = m.group()        
            return now-timedelta(days=int(m))

        elif strtime.find(u'小时')>-1:
            m = pattern.search(strtime)
            m = m.group()
            return now-timedelta(hours=int(m))

        elif (strtime.find(u'年')>-1) and (strtime.find(u'月')>-1) and (strtime.find(u'日')>-1 ):
            pattern2 = re.compile(r"(\d+).(\d+).(\d+).")
            m = pattern2.search(strtime)
            get_date = date(int(m.group(1)),int(m.group(2)),int(m.group(3)))
            return get_date

        else:
            return now

    #in this situation, override to modify the readCount, commentCount
    #单条异常只对 时间 做特别处理.其他异常交给main处理
    def itemProcess(self,item):
        url = item.h3.a['href']
        title = item.h3.a.text
        #there is not readcount and commentcount， so let both be None
        readCount = commentCount = 0
        content =  item.find('div',attrs={'class':'textA'}).text
        content = self.html_parser.unescape(content)
        username = item.find('div',attrs={'class':'relate'}).a.text
        try:
            createdAt = item.h3.span.text
            #print createdAt.encode('utf-8')
            createdAt = self.convertTime(createdAt)
        except Exception, e:
            createdAt = datetime.now()
            bbs_logger.exception(e) 

        #print url,username.encode('utf-8'),title.encode('utf-8'),content.encode('utf-8'),createdAt,readCount,commentCount
        store_bbs_post(url, username, title, content,
                       self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)

  

def main(id):
    try:
        obj = WYSQBBS(WYSQ_INFO_SOURCE_ID)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main()
    except Exception, e:
        store_error(WYSQ_INFO_SOURCE_ID)
        bbs_logger.exception(e) 
    try:
        obj = Baidu(id,'bbs.163.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)

if __name__ == "__main__":
    main(WYSQ_INFO_SOURCE_ID)
    

        
        
