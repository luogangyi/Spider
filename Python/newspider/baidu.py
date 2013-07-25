#! /usr/bin/env python
#coding=utf-8


#! /usr/bin/env python
#coding=utf-8

from BaseTimeLimit import *
from news_utils import *

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
        try:
        	content = urllib2.urlopen(url).read()
        	soup = BeautifulSoup(content)
    	except:
    		return []
            

        try:
            items = soup.findAll("table",{'class':'result'})
        except:# there is not any result,so return empty list
            return []
        #print len(items)
        time.sleep(1)
        
        return items
    
    def itemProcess(self,item):
        try:
            a = item.find('a')
            url = a['href']
            title = a.text

            response = urllib2.urlopen(url)
            url = response.geturl()

            content = item.find('div',{'class':'c-abstract'}).text
            
            citeTime = item.find('div',{'class':'f13'}).span.text
            
            createdAt = self.convertTime(citeTime)
            
            if self.category=="news":
                add_news_to_session(url, self.sourcename, title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
            elif self.category=="blog":
                store_blog_post(url, "", title, content,
                                    self.INFO_SOURCE_ID,self.keywordId, createdAt, 0,0)
            else:
                print "category is error"  
        except Exception, e:
            print e
        
        
        
             
    def convertTime(self,createdAt):
        
        m = re.search(r'\d+-\d+-\d+',createdAt)
       
        return datetime.strptime(m.group(),'%Y-%m-%d')
        
        
def test():
    s = '<a name="dttl" target="_blank" id="uigs_d0_0" href="http://news.sctv.com/jyxw/201305/t20130508_1462577.shtml"><!--awbg0-->[图文]“高考阅卷老师冒死揭露内幕”原是“旧帖新炒” - <em><!--red_beg-->四川<!--red_end--></em>网络广...</a>'
    s = BeautifulSoup(s).a
    print s['id']
    print s['href']
        
if __name__=="__main__":
    obj = Baidu(SCTV_INFO_SOURCE_ID,'sctv.com','news')
    obj.main()
#    test()

    
    
    
