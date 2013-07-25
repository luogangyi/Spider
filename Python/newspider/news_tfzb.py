#! /usr/bin/env python
#coding=utf-8
#OK
from BaseTimeLimit import *
from news_utils import *

class TFZBNews(BaseTimeLimit):
    def __init__(self,sourceId):
        BaseTimeLimit.__init__(self,sourceId)
    
    def nextPage(self,keyword):
        try:
            url = 'http://morning.scol.com.cn/new/site/template/Paper_List.asp?paperCode=tfzb&bgcolor=E52815'
            data = {'ArticleContent': keyword.str.encode('gbk'),
                    'DataSearch': '',
                    'urllink': '../../html/tfzb/20130602/index.html+../../tfzb/20130602/index.htm+../../tfzb/20130602/tfzb_20130602.exe',
                    }
            data = urllib.urlencode(data)


            req = urllib2.Request(url, data = data)  
            response = urllib2.urlopen(req)  
            content = response.read() 
            soup = BeautifulSoup(content)
        except:
            return []
 
#        print content
        try:
            items = soup.find("table",id='Table3').findAll("table")
        except:# there is not any result,so return empty list
            return []
        #print items[0]
        #all the info is wraped in first table!!
        items = [items[0]]
        return items
    
    def itemProcess(self,item):
        try:
            i = 1
            #print "circle"
            for each_tr in item.findAll("tr")[1:-2] :
                if (i%2 ==1):
                    a = each_tr.td.a
                    url = "http://morning.scol.com.cn/"+a["href"][6:]
                    title = a.text
                    createdAt = each_tr.td.text.encode("GB18030")
                    createdAt = self.getCreateTime(createdAt)
                    #print createdAt
                    #print each_tr.td.a["href"]

                else:
                    content = each_tr.td.text[24:]
                    add_news_to_session(url, None, title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
                i = i+1
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
    obj = TFZBNews(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()

        
if __name__=="__main__":
    obj = TFZBNews(TFZB_INFO_SOURCE_ID)
    obj.main()
