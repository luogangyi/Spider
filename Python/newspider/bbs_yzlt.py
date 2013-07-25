#! /usr/bin/env python
#coding=utf-8

#ok

from BaseBBS import *

class YZLTBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        try:
            url='http://search.soufun.com/bbs/search.jsp?&btnSearch=++&fld=all&author=&forum=&city=&sort=date&newwindow=1&q='+keyword.str.encode('gb2312')
            response = urllib2.urlopen(url)
            content = response.read()
            #just need to visit once, because it is order by time in default
            soup = BeautifulSoup(content)
        except:
            return []
        try:
            items = soup.find("div",id='content').findAll("div",{'class':'result'})
        except:
            return []
        return items
    

    def convertTime(self,strtime):
        strtime = strtime.strip()
        now = datetime.now()
        pattern = re.compile(r".*(\d\d\d\d-\d+-\d+\s+\d\d:\d\d:\d\d).*")
        m = pattern.match(strtime)
        if not m == None :
            return m.group(1)

        pattern = re.compile(r"\d+")
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
            return strtime
            

    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        try:
            url = item.find("div",{'class':'postTitle'}).a['href']
        #print url
            title = item.find("div",{'class':'postTitle'}).a.text
        #print title.encode('gbk')
        #there is not readcount and commentcount， so let both be None
            readCount = commentCount = 0
#        readCount,commentCount = self.getReadAndComment(item.p.text)
            createdAt =  item.find('div',{'class':'postTitle'}).contents[2].string
    	    print createdAt    
            createdAt = self.convertTime(createdAt)
            print createdAt
		#print createdAt.encode('gbk')
            content =item.find('div',{'class':'postSource'}).contents[1].text
        
            userInfoTag = item('p')[-1]
       
        
            username = userInfoTag.a.text
            #store_bbs_post(url, username, title, content,
                       #self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)
        except Exception, e:
            print e

def main(id):
    obj = YZLTBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()    

if __name__ == "__main__":
    obj = YZLTBBS(32)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        
