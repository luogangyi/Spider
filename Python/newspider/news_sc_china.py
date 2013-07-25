#! /usr/bin/env python
#coding=utf-8
#OK
from BaseBBS import *
from news_utils import *

SOURCENAME = "中国新闻网四川新闻"
class ScChinaNews(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
        
    def setLastTime(self):
        job = session.query(Job).filter(Job.info_source_id==self.INFO_SOURCE_ID).order_by(Job.id.desc()).first()
        if job:
            self.lasttime= job.previous_executed
        else:
            self.lasttime = datetime.now() - timedelta(days=365)
            
    def main(self):
        try:
            if not self.isCanRun():
                return False
            
            self.setLastTime()
            previous_real_count = session.query(BBSPost).count()
            count = 0
            sql_job = Job()
            sql_job.previous_executed = datetime.now()
            sql_job.info_source_id = self.INFO_SOURCE_ID
            
            count=self.searchWrapper(count)
            
            current_real_count = session.query(BBSPost).count()
            
            sql_job.fetched_info_count = count
            sql_job.real_fetched_info_count = current_real_count - previous_real_count
            
            session.add(sql_job)
            session.flush()
            session.commit()
            return True
        except:
            return False
    def searchWrapper(self,count):
        for keyword in KEYWORDS:
            self.keywordId = keyword.id
#            pageIndex = 1
            self.isFinished = False
            while not self.isFinished:                
                items = self.nextPage(keyword)
                count += len(items)
                self.search4EachItem(items)
#                pageIndex += 1
                self.isFinished = True #just crawl the first page
        return count
    
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
    
    def search4EachItem(self,items):
        for item in items:
            if not self.isFinished:
                self.itemProcess(item)
    
    def itemProcess(self,item):
        try:
            url = item.find('a')['href']
            url = self.getCompleteURL('http://www.sc.chinanews.com.cn/',url)
            #print url
            #must convert string to datetime
            createdAt = self.convertTime(item.contents[-1])
            
            #here is important to guarantee the while loop can be over normally
            if self.setIsFinished(createdAt):
                 return
            
            content = self.getDetailPage(url)
            soup = BeautifulSoup(content)
            
            soup = soup.find('div',{'class':'news_nr'})
            
            
            
            title = soup.find('div',{'class':'news_h1'}).text
            #print title
            timeAndSource = soup.find('div',{'class':'new_txtct'})('span')

            sourceName = self.getSourceName(timeAndSource[1].text)
            content = soup.find('div',id='newbody').text
            #print con
            
            
     
            
            #here, use add_news_to_session instead store_bbs_post
            add_news_to_session(url, SOURCENAME, title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
        except Exception, e:
            print e
    
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
    obj = ScChinaNews(id)
    return obj.main()
    
if __name__=="__main__":
    obj = ScChinaNews(38)
    obj.main()
#    dt = datetime.strptime("[2010-12-04T10:30:53]", "[%Y-%m-%dT%H:%M:%S]")
#    print dt

    

        

