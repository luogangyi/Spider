#! /usr/bin/env python
#coding=utf-8
from BaseTimeLimit import *
from blog_utils import *

class TIANYAWD(BaseTimeLimit):
   # def __init__(self,sourceId):
       # BaseBBS.__init__(self,sourceId)
    
    def __init__(self,sourceId):
        BaseTimeLimit.__init__(self,sourceId)
    #in this situation, override to set url 

    def convertTime(self,strtime):
        now = datetime.now()
        pattern = re.compile(r".*(\d\d\d\d-\d+-\d+).*")
        m = pattern.match(strtime)
        if not m == None :
            #print m.group(1)
            return m.group(1)

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
        try:
            url = 'http://cn.bing.com/search?form=TYNEW1&q='+ (keyword.str.encode('utf-8'))+'+site:wenda.tianya.cn&qs=n&sk=&FORM=SEENCN'
            response = urllib2.urlopen(url)
            content = response.read()
            #just need to visit once, because it is order by time in default
            soup = BeautifulSoup(content)
        except:
            return []
        try:
           items = soup.find('div',id= 'results').findAll('li',{'class':'sa_wr'})
        except:
            return []
        
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        try:
            url = item.h3.a['href']
            title = item.h3.a.text
            #there is not readcount and commentcount， so let both be None
            userInfoTag =  item.find('div',{'class':'sb_meta'})
            cite = userInfoTag.find('cite').text
            pos = len(cite)
            createdAt = userInfoTag.text[pos:]
            createdAt= self.convertTime(createdAt)
            #print createdAt

            commentCount = item.find('ul',{'class':'sp_pss'})
            if not commentCount == None:
                commentCount = commentCount.findAll('li')
                commentCount = commentCount[len(commentCount)-1]
                commentCount = commentCount.text[2:3]
            else:
                commentCount = 0
        #    sStr=  userInfoTag.text
        #    nPos = 0
        #    for c in sStr:
        #        if c == '-' and ((sStr[sStr.index(c)+3]=='-') or (sStr[sStr.index(c)+2]=='-')):
        #            nPos = sStr.index(c)
        #            break
          
        #    if not nPos ==0 
        #        createdAt = sStr[nPos-4:]
        #    else

            readCount =  0
            content =  item.p.text

            #print title +  " "+commentCount+ " " + content

            username = ""
            
            store_blog_post(url,"", title, content,
                        self.INFO_SOURCE_ID,self.keywordId, createdAt, 0,commentCount)
        except Exception, e:
            print e
 
        
    

if __name__ == "__main__":
    obj = TIANYAWD(58)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        