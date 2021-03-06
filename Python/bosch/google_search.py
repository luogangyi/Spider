#! /usr/bin/env python
#coding=utf-8
#written by huaiweicheng
# update by lgy 2013.7.30
# update by lgy , add filer:recheck_title,recheck_url
# update by lgy ,2013.08.04. add retry, adjust sleep time;
# update by lgy, 2013.08.04 .fix bug of calculate fetched count of different category 
from BaseTimeLimit import *
from news_utils import *
from blog_utils import *
from bbs_utils import *
from wiki_utils import *


class Google(BaseBBS):
    def __init__(self,sourceId,domain,category,sourcename=""):
        BaseBBS.__init__(self,sourceId)
        self.domain = domain
        self.category = category
        self.sourcename = sourcename
    
    def nextPage(self,keyword):

        items = []
        keyword = keyword.str.encode('utf8')
        domain = self.domain
        try:
            cookie_jar = cookielib.LWPCookieJar()
            cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17')]
            urllib2.install_opener(opener)

            # get cookie
            cookie_url = '''http://www.google.com.hk?hl=zh-CN'''
            opener.open(cookie_url)


            # for recent weak
                   #url = 'http://www.baidu.com/s?q1=%s&q2=&q3=&q4=&rn=100&lm=7&ct=0&ft=&q5=&q6=%s&tn=baiduadv' % (keyword,domain)
            url = 'http://www.google.com.hk/search?as_q=%s&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=lang_zh-CN&cr=&as_qdr=w&as_sitesearch=%s&as_occt=any&safe=active&as_filetype=&as_rights=' % (keyword,domain)
            headers = {
                    'Host': 'www.google.com.hk',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'
                }
            #print url
            req= urllib2.Request(url, headers = headers)  
            response = opener.open(req)
            content = response.read() 
            #content= urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)          
            #print soup    
            items = soup.findAll("li",{'class':'g'})
            #print len(items)
            time.sleep(10)
        except:
            time.sleep(60)
            print "retry!"

            cookie_jar = cookielib.LWPCookieJar()
            cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17')]
            urllib2.install_opener(opener)

            # get cookie
            cookie_url = '''http://www.google.com.hk?hl=zh-CN'''
            opener.open(cookie_url)

            # for recent weak
                   #url = 'http://www.baidu.com/s?q1=%s&q2=&q3=&q4=&rn=100&lm=7&ct=0&ft=&q5=&q6=%s&tn=baiduadv' % (keyword,domain)
            url = 'http://www.google.com.hk/search?as_q=%s&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=lang_zh-CN&cr=&as_qdr=w&as_sitesearch=%s&as_occt=any&safe=active&as_filetype=&as_rights=' % (keyword,domain)
            headers = {
                    'Host': 'www.google.com.hk',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'
                }
            req= urllib2.Request(url, headers = headers)  
            response = opener.open(req)
            content = response.read() 
            #content= urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)          
            #print soup    
            items = soup.findAll("li",{'class':'g'})
            #print len(items)
            time.sleep(10)

        return items

    def itemProcess(self,item,keyword):
        a = item.find('a')
        url = a['href']
        title = a.text
        #recheck url
        if recheck_url(url):
            return
        #recheck title
        if not recheck_title(keyword,title):
            return
        content = item.find('div',{'class':'s'}).find('span',{'class':'st'}).text
        content=self.extractcontent(content)
        citeTime =  item.find('div',{'class':'s'}).find('span',{'class':'f'}).text
        
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
            time.sleep(20)
        return count

    def search4EachItem(self,items,keyword):
        for item in items:
            self.itemProcess(item,keyword)         
        
        
    def extractcontent(self,content):
        m = re.search(ur'([\s\S]*)-([\s\S]*)',content.encode('utf8'))
        return m.group(2)
             
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
    s = '<a name="dttl" target="_blank" id="uigs_d0_0" href="http://news.sctv.com/jyxw/201305/t20130508_1462577.shtml"><!--awbg0-->[å›¾æ–‡]â€œé«˜è€ƒé˜…å·è€å¸ˆå†’æ­»æ­éœ²å†…å¹•â€åŽŸæ˜¯â€œæ—§å¸–æ–°ç‚’â€ - <em><!--red_beg-->å››å·<!--red_end--></em>ç½‘ç»œå¹¿...</a>'
    s = BeautifulSoup(s).a
    print s['id']
    print s['href']
        
if __name__=="__main__":
    obj = Google(1,'sina.com','news')
    obj.main()

    
