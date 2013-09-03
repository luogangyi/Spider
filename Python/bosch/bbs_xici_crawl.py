#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search,bug fix
# update by lgy, 2013.7.30, add google search

from BaseBBS import *
# from baidu import Baidu
# from google_search import Google

class XICI(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)

     #in this situation, override to set url 
    def nextPage(self,keyword,page):

        
        url = 'http://www.xici.net/s/?page=%d&k=%s&bid=0&t=2&timesort=1' % (page,keyword.str.encode('gbk'))
        #print keyword.str,url
        response = urllib2.urlopen(url)

        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content)
        lists = soup.find("ul",attrs={'class':'result_list'})

        if lists == None:
            return []
        items = lists.findAll("li")

        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
    	p_tags = item.findAll('p')
        url = p_tags[0].a['href']
        #print url
        title = p_tags[0].a.text
        content =  p_tags[1].text
        #print content

        userInfoTag = p_tags[-1]
        a_tags = userInfoTag.findAll('a')
        username = a_tags[-1].text
        time = userInfoTag.findAll('font')[-1].text
        createdAt = "20"+time

        readCount = commentCount = 0

        #print url, username.encode('utf-8'), title.encode('utf-8'), content.encode('utf-8')
        #print url, username, title, content,createdAt
        store_bbs_post(url, username, title, content,
                      self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)


        
    
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

        #依次搜索关键词,最多翻5页
    def searchWrapper(self,count):
        for keyword in KEYWORDS:
            self.keywordId = keyword.id
            print keyword.id
            pageIndex = 1
            isFinished = False
            while not isFinished:                
                items = self.nextPage(keyword,pageIndex)
                current_len = len(items)
                count += current_len
                if(current_len == 0 or pageIndex >=5):
                	isFinished = True
                self.search4EachItem(items)
                pageIndex += 1
                
            	time.sleep(5)
        return count

  
def main(id):
    try:
        obj = XICI(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main() 
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e) 
    # try:
    #     obj = Baidu(id,'91town.com','bbs')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e) 
    # try:
    #     obj = Google(id,'91town.com','bbs')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e) 
 

if __name__ == "__main__":
    main(DSCSQ_INFO_SOURCE_ID)
    

        
        



