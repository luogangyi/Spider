#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29
from BaseTimeLimit import *
from news_utils import *
from blog_utils import *
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
        print url
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
        print url.encode('utf-8'), title.encode('utf-8'), content.encode('utf-8')
        if self.category=="news":
            add_news_to_session(url, self.sourcename, title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)
        elif self.category=="blog":
            store_blog_post(url, "", title, content,
                                self.INFO_SOURCE_ID,self.keywordId, createdAt, 0,0)
        elif self.category=="bbs":
            store_bbs_post(url, "", title, content,
                                self.INFO_SOURCE_ID, self.keywordId, createdAt, 0,0)
        else:
            print "category is error" 

        
        

             
    def convertTime(self,createdAt):
        
        m = re.match(r'.*?-.*?-.*?(\d.+)',createdAt)
        strtime = m.group(1)
       
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
            return datetime.strptime(strtime.strip(),'%Y-%m-%d')

    
            
if __name__=="__main__":
    obj = Youdao(BLOG163_INFO_SOURCE_ID,'blog.163.com')
    obj.main()
#    test()
