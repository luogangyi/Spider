#! /usr/bin/env python
#coding=utf-8

from BaseTimeLimit import *
from news_utils import *
source_name = "四川日报"
class SCRBNews(BaseTimeLimit):
    def __init__(self,sourceId):
        BaseTimeLimit.__init__(self,sourceId)
    
    def nextPage(self,keyword):
        try:
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
        except:
            return []

        #print soup.prettify()

        try:
            items = soup.findAll("div",{'style':'line-height:30px;padding-left:10px; width:90%; height:30px; margin:auto; background-color:#E0DDD8; '})
        except:# there is not any result,so return empty list
            return []
        #print items
        return items
    
    def itemProcess(self,item):
        try:
            divs = item.findAll("div")
            url = divs[0].a['href']
            url = 'http://epaper.scdaily.cn'+url
            title = divs[0].a.text.encode("utf-8")
            #print divs[0].a
            createdAt =  divs[-1].text
            parent_div = item.parent
            content = parent_div.findAll("div")[-1].text
            createdAt = self.convertTime(createdAt)
            #print content.encode("utf-8")
            add_news_to_session(url, source_name, title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
        except Exception, e:
            print e

   
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
    obj = SCRBNews(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()

        
if __name__=="__main__":
    obj = SCRBNews(46)
    obj.main()
