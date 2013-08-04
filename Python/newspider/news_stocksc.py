#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
from google_search import Google
from baidu import Baidu
from BaseNews import *
from news_utils import *

#这个网站并未按时间排序，所以只能用BaseBBS，不能用有时间判断退出的BaseTimeLimit类。
SOURCENAME = "金融投资报"
class StockSCNews(BaseNews):
    '''金融投资报  http://www.stocknews.sc.cn/'''
    def __init__(self,sourceId):
        BaseNews.__init__(self,sourceId)
    
    def nextPage(self,keyword):

        url = 'http://www.stocknews.sc.cn/www/index.php?mod=index&con=search&act=search&keywords=%s&page=1' % (keyword.str.encode('gbk'))
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)

        items = soup.find("div",id='main')
        if items==None:
            return []
        items = items.findAll("div",recursive=False)

        return items
    
    def itemProcess(self,item):

        a = item.div.find('a')
        title = a.text
        #print title
        url = self.getCompletedURL('http://www.stocknews.sc.cn/',a['href'])

        createdAt = item.div('div')[-2].text
        createdAt = self.convertTime(createdAt)
        
        content =item('div')[1].text
        #print url, SOURCENAME, title, content,createdAt
        add_news_to_session(url, SOURCENAME, title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)
  
        
    def convertTime(self,createdAt):
        return datetime.strptime(createdAt,'%Y-%m-%d')

def main(id):
    try:
        obj = StockSCNews(id)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)
    # try:
    #     obj = Baidu(id,'stocknews.sc.cn','news',SOURCENAME)
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)
  
    # try:
    #     obj = Google(id,'stocknews.sc.cn','news',SOURCENAME)
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     news_logger.exception(e)    
        
if __name__=="__main__":
    main(STOCKSC_NEWS_INFO_SOURCE_ID)

