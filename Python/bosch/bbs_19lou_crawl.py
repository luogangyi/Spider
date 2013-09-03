#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search,bug fix
# update by lgy, 2013.7.30, add google search

from BaseBBS import *
from urllib import quote
# from baidu import Baidu
# from google_search import Google

class BBS19lou(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)

     #in this situation, override to set url 
    def nextPage(self,keyword):

        keyword.str = keyword.str.replace(' ','%20')
        url = 'http://www.19lou.com/search/thread?keyword=%s&fid=0&sorts=createdTime&timeType=0&fids=undefined' % (keyword.str.encode('gbk'))
        print keyword.str,url


        headers = {
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
        }

        req = urllib2.Request(url, headers = headers)  
        response = urllib2.urlopen(req)  

        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content,fromEncoding='gbk')
        lists = soup.find("ul",attrs={'class':'search-list link0'})

        if lists == None:
            return []
        items = lists.findAll("li")

        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):

        div_tags = item.findAll('div')
        user_div = div_tags[0]
        cont_div = div_tags[1]

        username = user_div.a.text
        url = cont_div.h3.a['href']
        #print url
        title = cont_div.h3.a.text
        createdAt =  cont_div.h3.span.text
        #print content
        p_tags = cont_div.findAll('p')
        content = p_tags[0].text

        commentInfoTag = p_tags[-1].find('span',attrs={'class':'fr'})
        if commentInfoTag == None:
            readCount = commentCount = 0
        else:
            readCount = commentInfoTag.span.text
            commentCount = commentInfoTag.findAll('a')[-1].text
        

       
        #print url, username.encode('utf-8'), title.encode('utf-8'), content.encode('utf-8')
        print url, username, title, content,createdAt, readCount, commentCount
        # store_bbs_post(url, username, title, content,
        #               self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)


        
    
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
    try:
        obj = BBS19lou(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
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
    

        
        



