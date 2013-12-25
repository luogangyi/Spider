#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
# no in-site search, 2013.12.25
from BaseBBS import *
from baidu import Baidu
from google_search import Google

class MSLT(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)

     #in this situation, override to set url 
    def nextPage(self,keyword):
        url = "http://bbs.qx818.com/search.php"
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)
        formhash = soup.find("div",id="ct").find("input",attrs={'type':'hidden'})["value"]
      
        data = {'formhash': formhash,
                'srchtxt': keyword.str.encode("gbk"),
                'searchsubmit': 'yes',
                }
        data = urllib.urlencode(data)


        req = urllib2.Request(url, data = data)  

        response = urllib2.urlopen(req)  

        url = response.url
        response = urllib2.urlopen(url)
        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content)
        items = soup.find("div",id="threadlist")
        if items == None:
            return []

        items = items.findAll("li")
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):

        url = "http://qx818.cn/"+item.h3.a['href']
        title = item.h3.a.text
        #print title
        #there is not readcount and commentcount， so let both be None
        readCount = commentCount = 0
#        readCount,commentCount = self.getReadAndComment(item.p.text)
    
        #content =  item.find('p',{'class':'content'}).text
        content =  item('p')[1].text
        #print content

        userInfoTag = item('p')[-1]



        createdAt = userInfoTag('span')[0].text # userInfoTag.contents[0].strip()[:-1].strip()

        createdAt = self.convertTime(createdAt)

        username = userInfoTag.a.text
        print url, username, title, content
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
    # try:
    #     obj = MSLT(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    #     obj.main()

    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e)

    try:
        obj = Baidu(id,'bbs.qx818.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    # try:
    #     obj = Google(id,'bbs.qx818.com','bbs')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e)


if __name__ == "__main__":
    main(MSLT_INFO_SOURCE_ID)

    

        
        