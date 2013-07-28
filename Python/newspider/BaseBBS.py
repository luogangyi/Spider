#! /usr/bin/env python
#coding=utf-8

from config import *
from bbs_utils import *
import HTMLParser

class BaseBBS(object):
    def __init__(self,sourceId):
        self.INFO_SOURCE_ID = sourceId
        #self.getRunInterval()
        self.setCookie2Urllib2()
        self.html_parser = HTMLParser.HTMLParser()
    
    def getRunInterval(self):
        self.runInterval = session.query(InfoSource).filter(InfoSource.id==self.INFO_SOURCE_ID).first().period
        self.runInterval = timedelta(minutes=self.runInterval)

    def setCookie2Urllib2(self):
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)    
    def isCanRun(self):
        job = session.query(Job).filter(Job.info_source_id==self.INFO_SOURCE_ID).order_by(Job.id.desc()).first()
        if not job:
            return True
        else:
            self.lasttime = job.previous_executed
            if datetime.now()-self.lasttime >= self.runInterval:
                return True
            else:
                return False
            
        
    def main(self):
        last_time = session.query(Job).filter(Job.info_source_id==self.INFO_SOURCE_ID).order_by(Job.id.desc()).first().previous_executed    
        # if not self.isCanRun():
        #     return False
        previous_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==self.INFO_SOURCE_ID).count()
        previous_real_count = session.query(BBSPost).count()
        count = 0
        sql_job = Job()
        sql_job.previous_executed = datetime.now()
        sql_job.info_source_id = self.INFO_SOURCE_ID
        
        count=self.searchWrapper(count)

        current_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==self.INFO_SOURCE_ID).count()
        sql_job.fetched_info_count = count
        sql_job.real_fetched_info_count = current_real_count - previous_real_count
 
        session.add(sql_job)
        session.flush()
        session.commit()
        return True
    #依次搜索关键词
    def searchWrapper(self,count):
        for keyword in KEYWORDS:
            self.keywordId = keyword.id
            print keyword.id
#            pageIndex = 1
            isFinished = False
            while not isFinished:                
                items = self.nextPage(keyword)
                count += len(items)
                self.search4EachItem(items)
#                pageIndex += 1
                isFinished = True #just crawl the first page
            time.sleep(5)
        return count
    
    #需要根据实际页面重写该函数
    def nextPage(self,keyword):
        url = 'http://www.dz19.net/search.php?mod=my&q=%s' % (keyword.str.encode('gbk'))
        response = urllib2.urlopen(url)
        content = response.read()
        
        # need to visit again for which order by time, because the default is order by relevancy
        soup = BeautifulSoup(content)
        url = soup.find('a',text=u'按时间排序').parent['href']
        url = "http://so.dz19.net/"+url
        
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)

        try:
            items = soup.find("span",id="result-items").findAll("li")
        except:# there is not any result,so return empty list
            return []
        return items
    
    

        
    def search4EachItem(self,items):
        for item in items:
            self.itemProcess(item)

    #需要根据实际页面重写该函数        
    def itemProcess(self,item):
        url = item.h3.a['href']
        title = item.h3.a.text
        readCount,commentCount = self.getReadAndComment(item.p.text)
        content =  item.find('p',{'class':'content'}).text
        userInfoTag = item('p')[-1]
        createdAt = userInfoTag.contents[0].strip()[:-1].strip()
        createdAt = self.convertTime(createdAt)
        username = userInfoTag.a.text
        store_bbs_post(url, username, title, content,
                       self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)
    #需要根据实际页面重写该函数 
    def getReadAndComment(self,content):
        pattern = re.compile(r'\s*(\d*)\D*(\d*)')
        m = pattern.match(content)
        return m.group(2),m.group(1)
    
    #需要根据实际页面重写该函数                 
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
        
    def getCompletedURL(self,host,url):
        if url.find('http')>-1:
            return url
        else:
            return host+url
    

    
            

if __name__ == "__main__":
    obj = BaseBBS(DZ19_INFO_SOURCE_ID)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    
    
        
        

        
