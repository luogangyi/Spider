#! /usr/bin/env python
#coding=utf-8

#ok

from BaseBBS import *
from datetime import date

class WYSQBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        #print (keyword.str.encode('utf-8'))
        try:
            url = 'http://news.youdao.com/search?q='+(keyword.str.encode('utf-8'))+'&start=0&length=10&ue=utf8&s=bytime&tl=&keyfrom=rnews.precom' 
            response = urllib2.urlopen(url)
            content = response.read()
            #just need to visit once, because it is order by time in default
            soup = BeautifulSoup(content)
           # print soup
        except:
            return []
        try:
            items = soup.find("ul",id="results").findAll("li")
        except:
            return []
        return items
    


    def convertTime(self,strtime):
        now = datetime.now()

        pattern = re.compile(r"\d*")
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
    def itemProcess(self,item):
        try:
            url = item.h3.a['href']
            title = item.h3.a.text
            #there is not readcount and commentcount， so let both be None
            readCount = commentCount = 0
    #        readCount,commentCount = self.getReadAndComment(item.p.text)
        
            content =  item.p.text
            userInfoTag = item.find('span',{'class':'green stat'}).text
            userInfoTagArray = userInfoTag.split(' ')
        #    userInfoTag = item('p')[-1]
            createdAt = userInfoTagArray[1]
            #print createdAt.encode('utf-8')
    	    createdAt = self.convertTime(createdAt)
    	    username = userInfoTagArray[0]
            store_bbs_post(url, username, title, content,
                           self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)
        except Exception, e:
            print e
  

def main(id):
    obj = WYSQBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()  

if __name__ == "__main__":
    obj = WYSQBBS(26)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        
