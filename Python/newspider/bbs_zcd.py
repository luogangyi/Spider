#! /usr/bin/env python
#coding=utf-8

#ok

from BaseBBS import *

class ZCDBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        try:
            first_url = "http://www.chengtu.com"
            response = urllib2.urlopen(first_url)
            content = response.read()
            soup = BeautifulSoup(content)
            items = soup.find("form",{'class':'topsearch'}).findAll("input")
            hidden_key_value = {}

            for input_item in items :
                
                try:
                    hidden_key_value[input_item['name']] = input_item['value']
                    #print input_item["name"]+" "+input_item["value"]
                except:
                    break
            
            url='http://www.chengtu.com/search.php?formhash='+hidden_key_value['formhash'].encode('gbk')+\
            '&mod='+hidden_key_value['mod'].encode('gbk')+'&srchtype='+hidden_key_value['srchtype'].encode('gbk')+'&srhfid='+\
            hidden_key_value['srhfid'].encode('gbk')+'&srchtxt='+keyword.str.encode('gbk')+'&orderField=posted&orderType=desc'
            #print url.encode('gbk')
            response = urllib2.urlopen(url)
            content = response.read()
            #just need to visit once, because it is order by time in default
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
            try:
                url = item.h3.a['href']
                title = item.h3.a.text
            except:
                url = item.h4.a['href']
                title = item.h4.a.text
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
    obj = ZCDBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

if __name__ == "__main__":
    obj = ZCDBBS(20)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        
