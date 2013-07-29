#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
from google_search import Google
from baidu import Baidu
from BaseTimeLimit import *
from BaseBBS import *
from wiki_utils import *

class TIANYAWD(BaseTimeLimit):
   # def __init__(self,sourceId):
       # BaseBBS.__init__(self,sourceId)
    
    def __init__(self,sourceId):
        BaseTimeLimit.__init__(self,sourceId)
    #in this situation, override to set url 

    def convertTime(self,strtime):
        now = datetime.now()

        pattern = re.compile(r"\d*")
        if strtime.find(u'今天')>-1:       
            return now

        elif strtime.find(u'昨天')>-1:       
            return now-timedelta(days=1)

        elif strtime.find(u'前天')>-1:      
            return now-timedelta(days=2)
            
        elif strtime.find(u'天')>-1:
            m = pattern.search(strtime)
            m = m.group()        
            return now-timedelta(days=int(m))

        elif strtime.find(u'小时')>-1:
            m = pattern.search(strtime)
            m = m.group()
            return now-timedelta(hours=int(m))

        elif (strtime.find(u'年')>-1) and (strtime.find(u'月')>-1) and (strtime.find(u'日')>-1 ):
            pattern2 = re.compile(r"(\d+).(\d+).(\d+).")
            m = pattern2.search(strtime)
            get_date = date(int(m.group(1)),int(m.group(2)),int(m.group(3)))
            return get_date

        else:
            return strtime

    def nextPage(self,keyword):
        #print  (keyword.str.encode('utf-8'))
        url = 'http://cn.bing.com/search?form=TYNEW1&q='+ (keyword.str.encode('utf-8'))+'+site:wenda.tianya.cn&qs=n&sk=&FORM=SEENCN'
        response = urllib2.urlopen(url)
        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content)

        items = soup.find('div',id= 'results')
        if items == None:
            return []

        items = items.findAll('li',{'class':'sa_wr'})
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        url = item.h3.a['href']
        title = item.h3.a.text
        #there is not readcount and commentcount， so let both be None
        userInfoTag =  item.find('div',{'class':'sb_meta'})
        cite = userInfoTag.find('cite').text
        pos = len(cite)
        createdAt = userInfoTag.text[pos:]
        createdAt= self.convertTime(createdAt)
       

        commentCount = item.find('ul',{'class':'sp_pss'})
        if not commentCount == None:
            commentCount = commentCount.findAll('li')
            commentCount = commentCount[len(commentCount)-1]
            commentCount = commentCount.text[2:3]
        try:
            commentCount = int(commentCount)
        except: 
            commentCount = 0

        readCount =  0
        content =  item.p.text
        username = ''
        
        print url, username, title, content,createdAt

        store_wiki_post(url, username, title, content,
                       self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount,0)
        
    
def main(id):
    try:
        obj = TIANYAWD(id)
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    try:
        obj = Baidu(id,'wenda.tianya.cn','wiki')
        obj.main()
    except Exception, e:
        store_error(id)
        wiki_logger.exception(e)

    

if __name__ == "__main__":
    main(58)


    

        
        