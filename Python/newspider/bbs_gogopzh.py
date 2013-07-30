#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
from BaseBBS import *
from baidu import Baidu
from google_search import Google

class GogoPZH(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):

        #print keyword.str.encode('gbk')
        #url = 'http://search.discuz.qq.com/f/discuz?mod=forum&formhash=4423dfa0&srchtype=title&srhfid=&srhlocality=forum%3A%3Aindex&sId=1868578&ts=1370052441&cuId=0&cuName=&gId=7&agId=0&egIds=&fmSign=&ugSign7=&sign=eb8ab11b56fc44be3814e2981c2821c9&charset=gbk&source=discuz&fId=0&searchsubmit=true&q='+(keyword.str.encode('gbk'))
        url = 'http://www.gogopzh.com/bbs/search.php?mod=my&q=' + (keyword.str.encode('gbk'))
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)
        url = soup.find('a',text=u'按时间排序')
        if url == None:
            return []
        url = url.parent['href']
        url = "http://search.discuz.qq.com"+url
        #print url
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)

        items = soup.find("span",id="result-items")
        if items == None:
            return []
        items = items.findAll("li")

        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):

        url = item.a['href']
        title = item.a.text
        #print title
        #there is not readcount and commentcount， so let both be None
        readCount = commentCount = 0
        #readCount,commentCount = self.getReadAndComment(item.p.text)
    
        content =  item.find('p',{'class':'content'}).text
        userInfoTag = item('p')[-1]
        createdAt = userInfoTag.contents[0].strip()[:-1].strip()
        createdAt = self.convertTime(createdAt)
        username = userInfoTag.a.text
        #print username, title, content,createdAt
        store_bbs_post(url, username, title, content,
                       self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)

def main(id):
    try:
        obj = GogoPZH(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main()

    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)

    try:
        obj = Baidu(id,'www.gogopzh.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    try:
        obj = Google(id,'www.gogopzh.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
        

if __name__ == "__main__":
    main(GogoPZH_INFO_SOURCE_ID)

    

        
        
