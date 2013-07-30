#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
from BaseBBS import *
from baidu import Baidu
from google_search import Google

class MSRBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):

        first_url = "http://bbs.meishanren.com/"
        response = urllib2.urlopen(first_url)
        content = response.read()
        soup = BeautifulSoup(content)
        items = soup.find("form",id="scbar_form").findAll("input",attrs={'type':'hidden'})

        hidden_key_value = {}

        for input_item in items :
            #print input_item["name"]+" "+input_item["value"]
            hidden_key_value[input_item["name"]] = input_item["value"]
           # print input_item["name"]+" "+input_item["value"]


        #print keyword.str.encode('gbk')+'abc'
        search_url = 'http://so.meishanren.com/f/discuz?mod=forum&formhash='+hidden_key_value['formhash']+\
                    '&srchtype=title&srhfid=&srhlocality=forum%3A%3Aindex&sId='+hidden_key_value['sId']+'&ts='+\
                    hidden_key_value['ts']+'&cuId=0&cuName=&gId=7&agId=0&egIds=&fmSign=&ugSign7=&ext_vgIds=0&'+\
                    'sign='+hidden_key_value['sign']+'&charset=gbk&source=discuz&fId=0&q='
        search_url = search_url.encode('gbk')+keyword.str.encode('gbk')+'&srchtxt='.encode('gbk')+keyword.str.encode('gbk')+'&searchsubmit=true'.encode('gbk')
        #print search_url

        response = urllib2.urlopen(search_url)
        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content)
        url = soup.find('a',text=u'按时间排序')
        if url == None:
            return []
        url = url.parent['href']
        url = "http://so.meishanren.com/"+url
        #print url
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)

        items = soup.find("span",id="result-items")
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
#        readCount,commentCount = self.getReadAndComment(item.p.text)
    
        content =  item.find('p',{'class':'content'}).text
        userInfoTag = item('p')[-1]
        createdAt = userInfoTag.contents[0].strip()[:-1].strip()
        createdAt = self.convertTime(createdAt)
        username = userInfoTag.a.text
        #print url, username, title, content, createdAt
        store_bbs_post(url, username, title, content,
                       self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)

 
def main(id):
    try:
        obj = MSRBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main()

    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)

    try:
        obj = Baidu(id,'bbs.meishanren.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    try:
        obj = Google(id,'bbs.meishanren.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)

if __name__ == "__main__":
    main(MSR_INFO_SOURCE_ID)

    

        
        