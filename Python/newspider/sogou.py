#! /usr/bin/env python
#coding=utf-8


#! /usr/bin/env python
#coding=utf-8

from BaseTimeLimit import *
from news_utils import *

class Sogou(BaseBBS):
    def __init__(self,sourceId,domain):
        BaseBBS.__init__(self,sourceId)
        self.domain = domain
    
    def nextPage(self,keyword):
        try:
            keyword = keyword.str.encode('utf8')
            
            domain = self.domain
            #for a day
            url = "http://www.sogou.com/web?sitequery=%s&num=100&query=%s+site%%3A%s&bstype=&q=%s" % (domain,keyword,domain,keyword) +"&fieldstripurl=&located=0&tro=on&filetype=&exclude=&ie=utf8&fieldtitle=&fieldcontent=&sourceid=inttime_day&interV=kKIOkrELjbkMmLkElbYTkKIKmbELjboJmLkEkL8TkKIMkLELjbcQmLkEmrELjbgRmLkEkLYTkKIM%0Alo%3D%3D_-483884962&tsn=1&interation=" 
            # for a month
            url = "http://www.sogou.com/web?sitequery=%s&num=100&query=%s+site%%3A%s&bstype=&q=%s" % (domain,keyword,domain,keyword) +"&fieldstripurl=&located=0&tro=on&filetype=&exclude=&ie=utf8&fieldtitle=&fieldcontent=&sourceid=inttime_month&interV=kKIOkrELjbkMmLkElbYTkKIKmbELjboJmLkEkL8TkKIMkLELjbcQmLkEmrELjbgRmLkEkLYTkKIM%0Alo%3D%3D_-483884962&tsn=3&interation=" 
            
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)
        except:
            return []

        try:
            items = soup.find("div",{'class':'results'}).findAll("div",recursive = False)
        except:# there is not any result,so return empty list
            return []
#        print len(items)
        return items
    
    def itemProcess(self,item):
        try:
            a = item.h3.find('a')
            a = self.deleteAnnotation(a).a
            
            
            url = a['href']
            title = a.text
            
            content = self.deleteAnnotation(item.div).div.text
            citeTime = item.find('cite').text
            
            createdAt = self.convertTime(citeTime)
            
            
            add_news_to_session(url, None, title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
        except Exception, e:
            print e
        
        
    def deleteAnnotation(self,tag):
        content = str(tag)
        pattern = re.compile(r'<!--.*?-->')
        content = pattern.sub('',content)
        return BeautifulSoup(content)
             
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
        
        
def test():
    s = '<a name="dttl" target="_blank" id="uigs_d0_0" href="http://news.sctv.com/jyxw/201305/t20130508_1462577.shtml"><!--awbg0-->[图文]“高考阅卷老师冒死揭露内幕”原是“旧帖新炒” - <em><!--red_beg-->四川<!--red_end--></em>网络广...</a>'
    s = BeautifulSoup(s).a
    print s['id']
    print s['href']
        
if __name__=="__main__":
    obj = Sogou(SCTV_INFO_SOURCE_ID,'sctv.com')
    obj.main()
#    test()
