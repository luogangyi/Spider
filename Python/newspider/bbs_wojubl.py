#! /usr/bin/env python
#coding=utf-8

#ok

from BaseBBS import *

class WOJUBLBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        try:
            first_url = "http://www.wojubl.com/"
            response = urllib2.urlopen(first_url)
            content = response.read()
            soup = BeautifulSoup(content)
            items = soup.find("form",id="scbar_form").findAll("input",attrs={'type':'hidden'})

            hidden_key_value = {}

            for input_item in items :
                #print input_item["name"]+" "+input_item["value"]
                hidden_key_value[input_item["name"]] = input_item["value"]

            search_url = 'http://www.wojubl.com/search.php?searchsubmit=yes'
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
        except:
            return []
        try:
            items = soup.find("div",id="threadlist").findAll("li")
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
            #readCount = commentCount = None
            readCount,commentCount = self.getReadAndComment(item('p')[0].text)
        
        
            content = item('p')[1].text
            #print readCount+" "+commentCount
            #content =  item.find('p',{'class':'content'}).text
            userInfoTag = item('p')[2]
            createdAt = userInfoTag.span.text
            createdAt = self.convertTime(createdAt)
            username = userInfoTag.a.text
             # print username+" "+createdAt
            store_bbs_post(url, username, title, content,
                           self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)
        except Exception, e:
            print e
    
    def getReadAndComment(self,content):
        pattern = re.compile(r'\s*(\d*).*-\s*(\d*).*')
        m = pattern.match(content)
        return m.group(2),m.group(1)

def main(id):
    obj = WOJUBLBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()

if __name__ == "__main__":
    obj = WOJUBLBBS(30)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        