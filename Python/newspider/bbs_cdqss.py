#! /usr/bin/env python    
#coding=utf-8
# update by lgy, 2013.7.28
# update by lgy, 2013.7.30, add google search

from BaseBBS import *
from baidu import Baidu
from google_search import Google
class CDQSS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
   
        url = 'http://bbs.chengdu.cn/tsearch.php?tn=cdqssad&searchsubmit=yes&q1=&q2=&words=%s&q3=&pagenum=20&qsst=0&qsstra=&qsstc=&sortmode=2' % (keyword.str.encode('utf-8'))
        response = urllib2.urlopen(url)
        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content)

        items = soup.find("table", {"class":"searchresult"})
        if items == None:
            return []
        items = items.findAll("tbody")

        return items

    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):

        url = item.tr.th.a['href']
        url = 'http://bbs.chengdu.cn/' + url
        title = item.tr.th.a.text
        #print title
        #readCount,commentCount = self.getReadAndComment(item.p.text)
        readCount = commentCount = 0
        content =  ""
        createdAt = item.tr.find('td', {'class':'lastpost'}).text
        createdAt = self.convertTime(createdAt)
        #print createdAt
        username = item.tr.find('td', {'class':'author'}).text
        #print username.encode('utf-8')
        store_bbs_post(url, username, title, content,
                   self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)


def main(id):
    try:
        obj = CDQSS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e) 
    # try:
    #     obj = Baidu(id,'bbs.chengdu.cn','bbs')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e) 
    # try:
    #     obj = Google(id,'bbs.chengdu.cn','bbs')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e)   


            
if __name__ == "__main__":
    main(CDQSS_INFO_SOURCE_ID)


        
        
