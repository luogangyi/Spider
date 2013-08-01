#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
from BaseBBS import *
from baidu import Baidu
from google_search import Google


class TianFuLBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        first_url = "http://www.scol.cn/"
        response = urllib2.urlopen(first_url)
        content = response.read()
        soup = BeautifulSoup(content)

        items = soup.find("form",id="search-bar")
        if items == None:
            return []
        items = items.findAll("input",attrs={'type':'hidden'})

        hidden_key_value = {}

        for input_item in items :
            #print input_item["name"]+" "+input_item["value"]
            hidden_key_value[input_item["name"]] = input_item["value"]

        search_url = 'http://www.scol.cn/search.php?searchsubmit=yes'
        data = {'mod':'forum',
                'formhash':hidden_key_value['formhash'].encode('gbk'),
                'srchtype':hidden_key_value['srchtype'].encode('gbk'),
                'srhfid':hidden_key_value['srhfid'].encode('gbk'),
                'srhlocality':hidden_key_value['srhlocality'].encode('gbk'),
                'srchtxt':keyword.str.encode('gbk'),
                }

        data = urllib.urlencode(data)
        req = urllib2.Request(search_url, data = data)  
        response = urllib2.urlopen(req)

        url = response.url
        #print url
        response = urllib2.urlopen(url)
        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content)
        
        items = soup.find("div",id="threadlist")
        if items == None:
            return []
        items = items.findAll("li")
        
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):

            url = item.a['href']
            title = item.a.text

            #print title
            #there is not readcount and commentcount， so let both be None
            readCount = commentCount = 0
            readCount,commentCount = self.getReadAndComment(item('p')[0].text)
        
            #print title
            content = item('p')[1].text
            #print readCount+" "+commentCount
            #content =  item.find('p',{'class':'content'}).text
            userInfoTag = item('p')[2]
            createdAt = userInfoTag.span.text
            createdAt = self.convertTime(createdAt)
            username = userInfoTag.a.text
            #print url, username, title, content, createdAt
            store_bbs_post(url, username, title, content,
                           self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)


    def getReadAndComment(self,content):
        pattern = re.compile(r'\s*(\d*).*-\s*(\d*).*')
        m = pattern.match(content)
        return m.group(2),m.group(1)

def main(id):
    try:
        obj = TianFuLBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e) 

    # try:
    #     obj = Baidu(id,'www.scol.cn','bbs')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e)

    # try:
    #     obj = Google(id,'www.scol.cn','bbs')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e)

if __name__ == "__main__":
    main(TianFu_INFO_SOURCE_ID)

    

        
        