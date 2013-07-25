#! /usr/bin/env python
#coding=utf-8
#test by lgy OK! 
from BaseBBS import *

class MSRBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        try:
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
            url = soup.find('a',text=u'按时间排序').parent['href']
            url = "http://so.meishanren.com/"+url
            #print url
            response = urllib2.urlopen(url)
            content = response.read()
            soup = BeautifulSoup(content)
        except:
            return []
        try:
            items = soup.find("span",id="result-items").findAll("li")
        except:
            return []
        
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        try:
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
            store_bbs_post(url, username, title, content,
                           self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)
        except Exception, e:
            print e
 
def main(id):
    obj = MSRBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
       

if __name__ == "__main__":
    obj = MSRBBS(22)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        