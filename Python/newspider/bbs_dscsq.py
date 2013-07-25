#! /usr/bin/env python
#coding=utf-8
#ok


from BaseBBS import *



class DSCSQ(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)

     #in this situation, override to set url 
    def nextPage(self,keyword):
        try:
            url = 'http://so.91town.com/search.php?wd=%s&fid=0&s=1&cityid=41' % (keyword.str.encode('utf-8'))
            #print url
            urllib2.urlopen(url)

            url2 = 'http://so.91town.com/search.php?o=1&p=1'
            #print url
            response = urllib2.urlopen(url2)


            content = response.read()
            #just need to visit once, because it is order by time in default
            soup = BeautifulSoup(content)
        except:
            return []
        #print soup
        try:
            items = soup.find("ul",id="s_list").findAll("li")
        except:
            return []
        
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        try:
            url = item.h1.a['href']
            #print url
            title = item.h1.text
            #print title
            #there is not readcount and commentcount， so let both be None
            
    #        readCount,commentCount = self.getReadAndComment(item.p.text)
        
            #content =  item.find('p',{'class':'content'}).text
            content =  item('div')[0].text
            #print content

            userInfoTag = item('p')[0]


            readCount = commentCount = None


            readCount=userInfoTag('span')[1].text

            commentCount=userInfoTag('span')[0].text



            pattern = re.compile(ur"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d")

            createdAt = None
            m = pattern.search(userInfoTag.text)
            if m:
                createdAt = m.group()  

             # userInfoTag.contents[0].strip()[:-1].strip()
            #print createdAt

            #createdAt = self.convertTime(createdAt)

            username = userInfoTag.a.text
            store_bbs_post(url, username, title, content,
                          self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)
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
    obj = DSCSQ(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()  

if __name__ == "__main__":
    obj = DSCSQ(21)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        

