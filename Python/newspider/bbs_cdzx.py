#! /usr/bin/env python
#coding=utf-8

#ok

from BaseBBS import *

class CDZXBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        try:
            url='http://www.cd.ccoo.cn/s/?k='+keyword.str.encode('gb2312')
            #url='http://www.cd.ccoo.cn/s/?k=%CE%D2'
            response = urllib2.urlopen(url)
            content = response.read()
            #just need to visit once, because it is order by time in default
            soup = BeautifulSoup(content)
            items = soup.find("div",{'class':'main_rt'}).findAll("div",'nr_a')
            return items
        except:
            return []
    def convertTime(self,strtime):
           #print strtime
           pattern = re.compile(r'.*(\d\d\d\d-\d+-\d+).*')
           m = pattern.match(strtime)
           return m.group(1)
    
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        try:
            url = item.div.a['href']
            url = 'http://www.cd.ccoo.cn/s/'+url
            title = item.div.a.text
            print url
        #print title.encode('gbk')
        #there is not readcount and commentcount， so let both be None
            readCount = commentCount = 0
#        readCount,commentCount = self.getReadAndComment(item.p.text)
    
            content =  item.find('div',{'class':'ty'}).text
            userInfoTag = item.find('div',{'class':'rq'}).text
        #print userInfoTag.encode('gbk')
            createdAt = userInfoTag
            createdAt = self.convertTime(createdAt)
        #print createdAt
            username =' '
            store_bbs_post(url, username, title, content,
                       self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)
        except Exception, e:
            print e
def main(id):
    obj = CDZXBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    
if __name__ == "__main__":
    obj = CDZXBBS(45)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        
