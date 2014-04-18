#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29
# update by lgy, 2013.08.04 .fix bug of calculate fetched count of different category 
# update by lgy, 2013.10.17 .filter old data 
from BaseTimeLimit import *
from news_utils import *
from blog_utils import *
from bbs_utils import *
from wiki_utils import *
class Youdao(BaseBBS):
    def __init__(self,sourceId,domain,category,sourcename=""):
        BaseBBS.__init__(self,sourceId)
        self.domain = domain
        self.category = category
        self.sourcename = sourcename
    def nextPage(self,keyword):

        keyword = keyword.str.encode('utf8')
        
        domain = self.domain
        # for a month
        url = "http://www.youdao.com/search?q=site%%3A%s+%s&start=0&ue=utf8&keyfrom=web.time&lq=site%%3A%s+%s&lm=7" % (domain,keyword,domain,keyword)
        #print url
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)

        items = soup.find("ol",{'id':'results'})
        if items ==None:
            return []

        items = items.findAll("li",recursive = False)
        return items
    
    def itemProcess(self,item):
        a = item.find('a')
        
        
        url = a['href']
        title = a.text
        
        content = item.find('p').text
        citeTime = item.find('cite').text
        
        createdAt = self.convertTime(citeTime)
        #print createdAt
        year,month,day = self.getYearMonthDay(createdAt.strftime("%Y-%m-%d"))
        created_date = datetime(int(year),int(month),int(day))
        cur_date = datetime.now()

        #cur_date = time.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
        delta_days = (cur_date - created_date).days
        if delta_days >20:
            return

        #print url.encode('utf-8'), title.encode('utf-8'), content.encode('utf-8'),createdAt
        if self.category=="news":
            add_news_to_session(url, self.sourcename, title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)
        elif self.category=="blog":
            store_blog_post(url, "", title, content,
                                self.INFO_SOURCE_ID,self.keywordId, createdAt, 0,0)
        elif self.category=="bbs":
            store_bbs_post(url, "", title, content,
                                self.INFO_SOURCE_ID, self.keywordId, createdAt, 0,0)
        elif self.category=="wiki":
            store_wiki_post(url, "", title, content,
                                self.INFO_SOURCE_ID, self.keywordId, createdAt, 0,0,0)
        else:
            print "category is error" 

        
    def getYearMonthDay(self,strtime):
        
        #print strtime
        now = datetime.now()
        pattern = re.compile(r"(\d+)-(\d+)-(\d+)")
        m = pattern.search(strtime)
        if m != None :
            return m.group(1),m.group(2),m.group(3)
             
    def convertTime(self,createdAt):
        
        m = re.search(r'\d+-\d+-\d+',createdAt)
        if m.group() != None:
            createdAt = datetime.strptime(m.group(),'%Y-%m-%d')
            return createdAt
       
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

    def main(self):
        #last_time = session.query(Job).filter(Job.info_source_id==self.INFO_SOURCE_ID).order_by(Job.id.desc()).first().previous_executed    
        # if not self.isCanRun():
        #     return False
        previous_real_count = 0

        if self.category=="news":
            previous_real_count = session.query(News).filter(News.info_source_id==self.INFO_SOURCE_ID).count()
        elif self.category=="blog":
            previous_real_count = session.query(BlogPost).filter(BlogPost.info_source_id==self.INFO_SOURCE_ID).count()
        elif self.category=="bbs":
            previous_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==self.INFO_SOURCE_ID).count()
        elif self.category=="wiki":
            previous_real_count = session.query(WikiPost).filter(WikiPost.info_source_id==self.INFO_SOURCE_ID).count()
        else:
            raise Exception("category is error")

        #previous_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==self.INFO_SOURCE_ID).count()
        count = 0
        sql_job = Job()
        sql_job.previous_executed = datetime.now()
        sql_job.info_source_id = self.INFO_SOURCE_ID
        
        count=self.searchWrapper(count)
        #print "count = ",count
        
        current_real_count = 0

        if self.category=="news":
            current_real_count = session.query(News).filter(News.info_source_id==self.INFO_SOURCE_ID).count()
        elif self.category=="blog":
            current_real_count = session.query(BlogPost).filter(BlogPost.info_source_id==self.INFO_SOURCE_ID).count()
        elif self.category=="bbs":
            current_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==self.INFO_SOURCE_ID).count()
        elif self.category=="wiki":
            current_real_count = session.query(WikiPost).filter(WikiPost.info_source_id==self.INFO_SOURCE_ID).count()
        else:
            raise Exception("category is error")
        #current_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==self.INFO_SOURCE_ID).count()
        sql_job.fetched_info_count = count
        sql_job.real_fetched_info_count = current_real_count - previous_real_count
        #print "current_real_count = ",current_real_count, "previous_real_count = ",previous_real_count
        session.add(sql_job)
        session.flush()
        session.commit()
        return True
    
            
if __name__=="__main__":
    obj = Youdao(BLOG163_INFO_SOURCE_ID,'blog.163.com')
    obj.main()
#    test()
