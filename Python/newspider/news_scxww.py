#! /usr/bin/env python
#coding=utf-8
#OK
from BaseBBS import *
from news_utils import *
SOURCENAME= "四川新闻网"
class SCXWW(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)

     #in this situation, override to set url 
    def nextPage(self,keyword):
        try:
            url = 'http://www.jike.com/so?q=%s&site=newssc.org&trade_id=6541630579976406454&se_type=4' % (keyword.str.encode('utf-8'))
            response = urllib2.urlopen(url)
            content = response.read()
            #just need to visit once, because it is order by time in default
            soup = BeautifulSoup(content)
        except:
            return []
        #print soup
        try:
            items = soup.find("ul",id="toolLink").findAll("li")
        except:
            return []
        
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        try:
            url = item.div.a['href']
            title = item.div.a.text
            #print title
            #there is not readcount and commentcount， so let both be None
            readCount = commentCount = None

           

    #        readCount,commentCount = self.getReadAndComment(item.p.text)
        
            #content =  item.find('p',{'class':'content'}).text
            content =  item.p.text
            #print content

           


            createdAt = self.convertTime(item.span.text)
            #createdAt = userInfoTag.text.find(" -")  #userInfoTag('span')[0].text # userInfoTag.contents[0].strip()[:-1].strip()

            #print createdAt
            #createdAt = self.convertTime(createdAt)

            username = None

            #store_bbs_post(url, username, title, content,
            #               self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)
            add_news_to_session(url, SOURCENAME, title, content,
                                self.INFO_SOURCE_ID, createdAt, self.keywordId)
        except Exception, e:
            print e
        
    
    def convertTime(self,strtime):
        now = datetime.now()
        pattern = re.compile(r"\d*")
    
        if strtime.find(u'天')>-1:
            m = pattern.search(strtime)
            m = m.group()        
            return now-timedelta(days=int(m))
        elif strtime.find(u'小时')>-1:
            m = pattern.search(strtime)
            m = m.group()
            return now-timedelta(hours=int(m))
        else:
            return strtime

def main(id):
    obj = SCXWW(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

if __name__ == "__main__":
    obj = SCXWW(36)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    
