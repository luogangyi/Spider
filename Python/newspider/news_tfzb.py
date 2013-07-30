#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
from google_search import Google
from baidu import Baidu
from BaseTimeLimit import *
from news_utils import *

SOURCENAME = "天府早报"
class TFZBNews(BaseTimeLimit):
    def __init__(self,sourceId):
        BaseTimeLimit.__init__(self,sourceId)
    
    def nextPage(self,keyword):

        url = 'http://morning.scol.com.cn/new/site/template/Paper_List.asp?paperCode=tfzb&bgcolor=E52815'
        data = {'ArticleContent': keyword.str.encode('gbk'),
                'DataSearch': '',
                'urllink': '../../html/tfzb/20130602/index.html+../../tfzb/20130602/index.htm+../../tfzb/20130602/tfzb_20130602.exe',
                }
        data = urllib.urlencode(data)


        req = urllib2.Request(url, data = data)  
        response = urllib2.urlopen(req)  
        content = response.read() 
        soup = BeautifulSoup(content,fromencoding="gbk")

        items = soup.find("table",id='Table3')
        if items==None:
            return []
        items = items.findAll("table")

        return [items[0]],len(items[0].findAll("tr")[1:-2])

    def searchWrapper(self,count):
        for keyword in KEYWORDS:
            self.keywordId = keyword.id
            print keyword.id
#            pageIndex = 1
            isFinished = False
            while not isFinished:                
                items,count_temp = self.nextPage(keyword)
                count += count_temp
                self.search4EachItem(items)
#                pageIndex += 1
                isFinished = True #just crawl the first page
            time.sleep(5)
        return count

    def itemProcess(self,item):

        i = 1
        #print "circle"
        for each_tr in item.findAll("tr")[1:-2] :
            if (i%2 ==1):
                a = each_tr.td.a
                url = "http://morning.scol.com.cn/"+a["href"][6:]
                title = a.text
                createdAt = each_tr.td.text
                createdAt = self.getCreateTime(createdAt)
                #print createdAt
                #print each_tr.td.a["href"]

            else:
                content = each_tr.td.text[24:]
                #print url, None, title, content,createdAt
                add_news_to_session(url, SOURCENAME, title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)
            i = i+1




        
        
    def getCreateTime(self,content):
        pattern = re.compile(r'.*(\d\d\d\d-\d+-\d+).*')
        m = pattern.match(content)
        return m.group(1) 

    def convertTime(self,createdAt):
        try:
            return datetime.strptime(createdAt,'%Y-%m-%d')
        except:
            return datetime.strptime(createdAt,'%Y-%m-%d %H:%M')
def main(id):
    try:
        obj = TFZBNews(id)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)
    try:
        obj = Baidu(id,'morning.scol.com.cn','news',SOURCENAME)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)
        
    try:
        obj = Google(id,'morning.scol.com.cn','news',SOURCENAME)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)


        
if __name__=="__main__":
    main(TFZB_NEWS_INFO_SOURCE_ID)
