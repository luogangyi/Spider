#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search

from BaseBBS import *

class YZLTBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        
        url='http://search.soufun.com/bbs/search.jsp?&btnSearch=++&fld=all&author=&forum=&city=&sort=date&newwindow=1&q='+keyword.str.encode('gb2312')
        response = urllib2.urlopen(url)
        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content)

        items = soup.find("div",id='content')
        if items == None:
            return []
        items = items.findAll("div",{'class':'result'})

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

        url = item.find("div",{'class':'postTitle'}).a['href']
        title = item.find("div",{'class':'postTitle'}).a.text

        readCount = commentCount = 0

        createdAt =  item.find('div',{'class':'postTitle'}).contents[2].string 
        createdAt = self.convertTime(createdAt)

        content =item.find('div',{'class':'postSource'}).contents[1].text
    
        userInfoTag = item('p')[-1]
    
        username = userInfoTag.a.text

        #print url, username, title, content,createdAt
        store_bbs_post(url, username, title, content,
                   self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)


def main(id):
    try:
        obj = YZLTBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e) 
    try:
        obj = Baidu(id,'soufun.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)


if __name__ == "__main__":
    obj = YZLTBBS(YZLT_INFO_SOURCE_ID)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        
