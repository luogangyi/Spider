#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.28 ,add baidu search, fix a bug!

from BaseBBS import *

class CDZXBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):

        url='http://www.cd.ccoo.cn/s/?k='+keyword.str.encode('gb2312')
        #url='http://www.cd.ccoo.cn/s/?k=%CE%D2'
        response = urllib2.urlopen(url)
        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content)
        #print soup.prettify()
        items = soup.find("div",{'class':'main_rt'}).findAll("div",'nr_a')
        return items

    def convertTime(self,strtime):
           #print strtime
           pattern = re.compile(r'.*(\d\d\d\d-\d+-\d+).*')
           m = pattern.match(strtime)
           return m.group(1)
    
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        if item.div.find("a") ==None:
            return
        url = item.div.a['href']
        url = 'http://www.cd.ccoo.cn/s/'+url
        title = item.div.a.text
        readCount = commentCount = 0

        content =  item.find('div',{'class':'ty'}).text
        userInfoTag = item.find('div',{'class':'rq'}).text

        createdAt = userInfoTag
        createdAt = self.convertTime(createdAt)

        username =' '
        #print content.encode("utf-8")
        store_bbs_post(url, username, title, content,
                   self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)

def main(id):
    try:
        obj = CDZXBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main()
        obj = Baidu(id,'www.cd.ccoo.cn','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e) 

    
if __name__ == "__main__":
    obj = CDZXBBS(CDZX_INFO_SOURCE_ID)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        
