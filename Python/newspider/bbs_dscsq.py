#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search,bug fix

from google_search import Google
from BaseBBS import *
from baidu import Baidu


class DSCSQ(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)

     #in this situation, override to set url 
    def nextPage(self,keyword):

        url = 'http://so.91town.com/search.php?wd=%s&fid=0&s=1&cityid=41' % (keyword.str.encode('utf-8'))
        #print url
        urllib2.urlopen(url)

        url2 = 'http://so.91town.com/search.php?o=1&p=1'
        #print url
        response = urllib2.urlopen(url2)


        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content)

        lists = soup.find("ul",id="s_list")
        if lists == None:
            return []
        items = lists.findAll("li")

        
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        url = item.h1.a['href']
        #print url
        title = item.h1.text
        content =  item('div')[0].text
        #print content

        userInfoTag = item('p')[0]


        readCount = commentCount = None


        readCount=userInfoTag('span')[1].text

        commentCount=userInfoTag('span')[0].text



        pattern = re.compile(ur"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d")

        createdAt = None
        m = pattern.search(userInfoTag.text)
        if m:
            createdAt = m.group()  
        username = userInfoTag.a.text

        #print url, username.encode('utf-8'), title.encode('utf-8'), content.encode('utf-8')

        store_bbs_post(url, username, title, content,
                      self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)


        
    
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

  
def main(id):
    try:
        obj = DSCSQ(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main() 
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e) 
    try:
        obj = Baidu(id,'91town.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e) 
 

if __name__ == "__main__":
    main(DSCSQ_INFO_SOURCE_ID)
    

        
        

