#! /usr/bin/env python
#coding=utf-8
# update by lgy 2013.07.28
# add category bbs, wiki, and update try/except
# update by lgy , add filer:recheck_title,recheck_url
# update by lgy ,2013.08.04. add retry, adjust sleep time;
# update by lgy, 2013.08.04 .fix bug of calculate fetched count of different category 
from BaseTimeLimit import *
from news_utils import *
from blog_utils import *
from bbs_utils import *
from wiki_utils import *

class Baidu(BaseBBS):
    def __init__(self,sourceId,domain,category,sourcename=""):
        BaseBBS.__init__(self,sourceId)
        self.domain = domain
        self.category = category
        self.sourcename = sourcename
    
    def nextPage(self,keyword):
        keyword = keyword.str.encode('utf8')
        domain = self.domain
        # for a month
        url = 'http://www.baidu.com/s?q1=%s&q2=&q3=&q4=&rn=100&lm=7&ct=0&ft=&q5=&q6=%s&tn=baiduadv' % (keyword,domain)

        items = []
        try:
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)
            items = soup.findAll("table",{'class':'result'})
            time.sleep(2)
        except:
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)
            items = soup.findAll("table",{'class':'result'})
            print "retry!"
            time.sleep(2)
        
        return items
    
    def itemProcess(self,item,keyword):

        a = item.find('a')
        url = a['href']
        title = a.text

        #recheck title!
        if not recheck_title(keyword,title):
            return



        response = urllib2.urlopen(url)
        url = response.geturl()

        #recheck url
        if recheck_url(url):
            return
        content = item.find('div',{'class':'c-abstract'}).text
        
        citeTime = item.find('div',{'class':'f13'}).span.text
        
        #print citeTime

        createdAt = self.convertTime(citeTime)
        
        #print url, title,content,createdAt
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
        
        
        
             
    def convertTime(self,strtime):
        
        print strtime
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

    def searchWrapper(self,count):
        for keyword in KEYWORDS:
            self.keywordId = keyword.id
            print keyword.id
#            pageIndex = 1
            isFinished = False
            while not isFinished:                
                items = self.nextPage(keyword)
                count += len(items)
                self.search4EachItem(items,keyword)
#                pageIndex += 1
                isFinished = True #just crawl the first page
            time.sleep(1)
        return count

    def search4EachItem(self,items,keyword):
        for item in items:
            self.itemProcess(item,keyword)    


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


def test():
    s = '<a name="dttl" target="_blank" id="uigs_d0_0" href="http://news.sctv.com/jyxw/201305/t20130508_1462577.shtml"><!--awbg0-->[图文]“高考阅卷老师冒死揭露内幕”原是“旧帖新炒” - <em><!--red_beg-->四川<!--red_end--></em>网络广...</a>'
    s = BeautifulSoup(s).a
    print s['id']
    print s['href']


# for test!!
if __name__=="__main__":
    obj = Baidu(1,'news.chengdu.cn','news')
    obj.main()
#    test()

    
    
    
