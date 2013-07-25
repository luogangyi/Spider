#! /usr/bin/env python
#coding=utf-8

#ok

from BaseBBS import *

class CQKXBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        try:
            url = 'http://bbs.cqkx.com/search.php?mod=my&q=%s' % (keyword.str.encode('gbk'))
            response = urllib2.urlopen(url)
            content = response.read()
            #just need to visit once, because it is order by time in default
            soup = BeautifulSoup(content)
        except:
            return []
        try:
            items = soup.find("span",id="result-items").findAll("li")
        except:
            return []
        
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        try:
            url = item.a['href']
            title = item.a.text
            #print title
            #there is not readcount and commentcount， so let both be None
            readCount = commentCount = 0
    #        readCount,commentCount = self.getReadAndComment(item.p.text)
        
            content =  item.find('p',{'class':'content'}).text
            userInfoTag = item('p')[-1]
            createdAt = userInfoTag.contents[0].strip()[:-1].strip()
            createdAt = self.convertTime(createdAt)
            username = userInfoTag.a.text
            store_bbs_post(url, username, title, content,
                           self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)
        except Exception, e:
            print e
  
def main(id):
    obj = CQKXBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main() 

if __name__ == "__main__":
    obj = CQKXBBS(18)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        