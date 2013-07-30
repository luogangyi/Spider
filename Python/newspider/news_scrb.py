#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
from google_search import Google
from baidu import Baidu
from BaseTimeLimit import *
from news_utils import *

source_name = "四川日报"
class SCRBNews(BaseTimeLimit):
    def __init__(self,sourceId):
        BaseTimeLimit.__init__(self,sourceId)
    
    def nextPage(self,keyword):

        url = 'http://epaper.scdaily.cn/www/index.php?mod=index&con=search&act=advanceResult'
        data = {'condition': 'content'.encode('gbk'),
                'keywords': keyword.str.encode('gbk'),
                'hidden': '7463',
                }
        data = urllib.urlencode(data)


        req = urllib2.Request(url, data = data)  
        response = urllib2.urlopen(req)  
        content = response.read() 
        soup = BeautifulSoup(content, fromEncoding="gbk")


        items = soup.findAll("div",{'style':'line-height:30px;padding-left:10px; width:90%; height:30px; margin:auto; background-color:#E0DDD8; '})

        return items
    
    def itemProcess(self,item):

        divs = item.findAll("div")
        url = divs[0].a['href']
        url = 'http://epaper.scdaily.cn'+url
        title = divs[0].a.text.encode("utf-8")
        #print divs[0].a
        createdAt =  divs[-1].text
        parent_div = item.parent
        content = parent_div.findAll("div")[-1].text
        createdAt = self.convertTime(createdAt)
        #print url, source_name, title, content,createdAt
        add_news_to_session(url, source_name, title, content,
                            self.INFO_SOURCE_ID, createdAt, self.keywordId)


   
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
        obj = SCRBNews(id)
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)
    try:
        obj = Baidu(id,'scdaily.cn','news',SOURCENAME )
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)

    try:
        obj = Google(id,'scdaily.cn','news',SOURCENAME )
        obj.main()
    except Exception, e:
        store_error(id)
        news_logger.exception(e)
        
if __name__=="__main__":
    main(SCRB_NEWS_INFO_SOURCE_ID)

