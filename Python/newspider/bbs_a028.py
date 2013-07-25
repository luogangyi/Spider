#! /usr/bin/env python
#coding=utf8

from BaseBBS import *

class A028(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        try:
            url = 'http://www.tg280.com/search.php'
            response = urllib2.urlopen(url)
            url = response.geturl()
            url = url[:url.find('&q=')+3]+(keyword.str.encode('utf-8'))+url[url.find('&q=')+3:]
            response = urllib2.urlopen(url)
            content = response.read()
            soup = BeautifulSoup(content)
            url = soup.find('a',text=u'按时间排序').parent['href']
            url = "http://chengdu.tg280.com"+url
            #print url
            response = urllib2.urlopen(url)
            content = response.read()
            soup = BeautifulSoup(content)
        except:
            return []
        try:
            items = soup.find("span", id="result-items").findAll("li")
        except:
            return []
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        try:
            url = item.a['href']
            title = item.a.text
            #print title.encode('gbk')
            readCount = commentCount = 0
            content = item.find('p',{'class':'content'}).text
            userInfoTag = item('p')[-1]
            createdAt = userInfoTag.contents[0].strip()[:-1].strip()
            createdAt = self.convertTime(createdAt)
            username = userInfoTag.a.text
            store_bbs_post(url, username, title, content,
                       self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)
        except Exception, e:
            print e
def main(id):
    obj = A028(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()

if __name__ == "__main__":
    obj = A028(28)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        
