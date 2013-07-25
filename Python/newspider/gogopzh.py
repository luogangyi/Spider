#! /usr/bin/env python
#coding=utf-8

from BaseBBS import *


class GogoPZH(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        try:
            #print keyword.str.encode('gbk')
            #url = 'http://search.discuz.qq.com/f/discuz?mod=forum&formhash=4423dfa0&srchtype=title&srhfid=&srhlocality=forum%3A%3Aindex&sId=1868578&ts=1370052441&cuId=0&cuName=&gId=7&agId=0&egIds=&fmSign=&ugSign7=&sign=eb8ab11b56fc44be3814e2981c2821c9&charset=gbk&source=discuz&fId=0&searchsubmit=true&q='+(keyword.str.encode('gbk'))
            url='http://search.discuz.qq.com/f/search?sId=1868578&ts=1370052441&mySign=738802b9&searchLevel=3&menu=1&rfh=1&qs=txt.tsort.a&orderField=posted&orderType=desc&q='+(keyword.str.encode('utf-8'))
            response = urllib2.urlopen(url)
            content = response.read()
            soup = BeautifulSoup(content)
        except:
            return []
        
        try:
            items = soup.find("span",id="result-items").findAll("li")
        except:
            print 'except'
            return []
        print items
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        try:
            url = item.h3.a['href']
            title = item.h3.a.text
            #print title.encode("gbk")
            #there is not readcount and commentcount， so let both be None
            readCount = commentCount = None
            #readCount,commentCount = self.getReadAndComment(item.p.text)
        
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
    obj = GogoPZH(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    
        

if __name__ == "__main__":
    obj = GogoPZH(CQKX_INFO_SOURCE_ID)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        
