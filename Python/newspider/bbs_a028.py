#! /usr/bin/env python
#coding=utf8
# update by lgy, 2013.7.28

from BaseBBS import *
from baidu import Baidu
class A028(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):

        url = 'http://www.tg280.com/search.php'
        response = urllib2.urlopen(url)
        url = response.geturl()
        url = url[:url.find('&q=')+3]+(keyword.str.encode('utf-8'))+url[url.find('&q=')+3:]
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)
        try:
            url = soup.find('a',text=u'按时间排序').parent['href']
        except:
            return []
        url = "http://chengdu.tg280.com"+url
        #print url
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)

        items = soup.find("span", id="result-items")
        if items == None:
            return []
        items = items.findAll("li")

        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):

        url = item.a['href']
        title = item.a.text
        #print title.encode('gbk')
        readCount = commentCount = 0
        content = item.find('p',{'class':'content'}).text
        userInfoTag = item('p')[-1]
        createdAt = userInfoTag.contents[0].strip()[:-1].strip()
        createdAt = self.convertTime(createdAt)
        username = userInfoTag.a.text
        #print url.encode('utf-8'), username.encode('utf-8'), title.encode('utf-8'), content.encode('utf-8')
        store_bbs_post(url, username, title, content,
                   self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)

def main(id):
    try:
        obj = A028(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    try:
        obj = Baidu(id,'www.tg280.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e) 


if __name__ == "__main__":
    main(A028_INFO_SOURCE_ID)
    

        
        
