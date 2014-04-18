#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search,bug fix!
# update by lgy, 2013.7.30, add google search
# update by lgy, 2013.10.11 .fix time bug
# update by lgy, 2013.10.30,fix bugs
from google_search import Google
from baidu import Baidu
from BaseNews import *
from news_utils import *

SOURCENAME = "四川在线"
class SCZX(BaseNews):
    def __init__(self,sourceId):
        BaseNews.__init__(self,sourceId)
    
    
    def nextPage(self,keyword):

        url = 'http://zhannei.youdao.com/search?ue=gb2312&keyfrom=web.index&siteId=scol&q=' + (keyword.str.encode('gb2312'))
        response = urllib2.urlopen(url)
        content = response.read()
        
        soup = BeautifulSoup(content,fromEncoding='gbk')

        items = soup.find("ol", id="results")
        if items==None:
            return []
        items = items.findAll("li")

        return items
    
    def itemProcess(self,item):

        title = item.div.div.h3.a.text

        content = item.div.findAll('div')[1].p.text
        #print content.encode('gbk')
        url = item.div.div.h3.a['href']
        #print url
        try:
            print item.div.findAll('div')[1].div.text
            createdAt = item.div.findAll('div')[1].div.text.split(' ')[4]
            print createdAt
            createdAt = self.convertTime(createdAt)
        except:
            createdAt = datetime.now()
            createdAt = "0000-00-00"
        #print url, SOURCENAME, title, content,createdAt
        add_news_to_session(url, SOURCENAME, title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)

        

    def convertTime(self,time):
        return datetime.strptime(time,'%Y-%m-%d')

def main(id):
    # try:
    #     obj =  SCZX(id)
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)

    try:
        obj = Baidu(id,'scol.com.cn','news',SOURCENAME)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)
  
    # try:
    #     obj = Google(id,'scol.com.cn','news',SOURCENAME)
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)


if __name__=="__main__":
    main(SCZX_NEWS_INFO_SOURCE_ID)



