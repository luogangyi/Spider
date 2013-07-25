#! /usr/bin/env python    
#coding=utf-8

#ok

from BaseBBS import *

class CDQSS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        try:      
            url = 'http://bbs.chengdu.cn/tsearch.php?tn=cdqssad&searchsubmit=yes&q1=&q2=&words=%s&q3=&pagenum=20&qsst=0&qsstra=&qsstc=&sortmode=2' % (keyword.str.encode('utf-8'))
            response = urllib2.urlopen(url)
            content = response.read()
            #just need to visit once, because it is order by time in default
            soup = BeautifulSoup(content)
        except:
            return []
        try:
            items = soup.find("table", {"class":"searchresult"}).findAll("tbody")
        except:
            return []
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        try:
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
            #print username.encode('gbk')
            store_bbs_post(url, username, title, content,
                       self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)
        except Exception, e:
            print e

def main(id):
    obj = CDQSS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
            
if __name__ == "__main__":
    obj = CDQSS(25)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        
