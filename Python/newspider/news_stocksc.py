#! /usr/bin/env python
#coding=utf-8
#OK
from BaseTimeLimit import *
from news_utils import *

#这个网站并未按时间排序，所以只能用BaseBBS，不能用有时间判断退出的BaseTimeLimit类。
SOURCENAME = "金融投资报"
class StockSCNews(BaseBBS):
    '''金融投资报  http://www.stocknews.sc.cn/'''
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    def nextPage(self,keyword):
        try:
            url = 'http://www.stocknews.sc.cn/www/index.php?mod=index&con=search&act=search&keywords=%s&page=1' % (keyword.str.encode('gbk'))
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content)
        except:
            return []
#        print content
        try:
            items = soup.find("div",id='main').findAll("div",recursive=False)
        except:# there is not any result,so return empty list
            return []

        return items
    
    def itemProcess(self,item):
        try:
            a = item.div.find('a')
            title = a.text
            #print title
            url = self.getCompletedURL('http://www.stocknews.sc.cn/',a['href'])

            createdAt = item.div('div')[-2].text
            createdAt = self.convertTime(createdAt)
            
            content =item('div')[1].text
            
            add_news_to_session(url, SOURCENAME, title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
        except Exception, e:
            print e
        
        
        
    def convertTime(self,createdAt):
        return datetime.strptime(createdAt,'%Y-%m-%d')

def main(id):
    obj = StockSCNews(id)
    obj.main()
    
        
if __name__=="__main__":
    obj = StockSCNews(40)
    obj.main()
