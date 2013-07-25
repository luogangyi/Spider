#! /usr/bin/env python
#coding=utf-8
#ok


from BaseBBS import *

class FuFengLBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        try:
            first_url = "http://bbs.fuling.com"
            response = urllib2.urlopen(first_url)
            content = response.read()
            soup = BeautifulSoup(content)
            items = soup.find("form",id="scbar_form").findAll("input")

            hidden_key_value = {}

            for input_item in items :
                #print input_item["name"]+" "+input_item["value"]
                hidden_key_value[input_item["name"]] = input_item["value"]

            #print "============="
            second_url='http://search.fuling.com/f/discuz?mod=forum&formhash='+hidden_key_value['formhash']+\
                '&srchtype=title&srhfid=&srhlocality=forum%3A%3Aindex&sId='+hidden_key_value['sId']+\
                '&ts='+hidden_key_value['ts']+'&cuId=0&cuName=&gId=7&agId=0&egIds=&fmSign=&ugSign7=&ext_vgIds=0&'+\
                'sign='+hidden_key_value['sign']+'&charset=gbk&source=discuz&fId=0&q=&srchtxt=&searchsubmit=true'

            response = urllib2.urlopen(second_url)
            content = response.read()
            soup = BeautifulSoup(content)
            items = soup.find("form",id="topSearchBar").findAll("input",attrs={'type':'hidden'})
            for input_item in items :
                #print input_item["name"]+" "+input_item["value"]
                hidden_key_value[input_item["name"]] = input_item["value"]


            url = 'http://search.fuling.com/f/discuz?mod=forum&'+\
                'formhash='+hidden_key_value['formhash'].encode('gbk')+'&srchtype=title&srhfid=&srhlocality=forum%3A%3Aindex&'+\
                'sId='+hidden_key_value['sId'].encode('gbk')+'&ts='+hidden_key_value['ts'].encode('gbk')+'&cuId=0&cuName=&gId=7&agId=0&egIds=&fmSign=&ugSign7=&ext_vgIds=0&'+\
                'sign='+hidden_key_value['sign'].encode('gbk')+'&charset=gbk&source=discuz&fId=0&q='+keyword.str.encode('gbk')+\
                '&srchtxt='+keyword.str.encode('gbk')+'&searchsubmit=true'

            #print url
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
            url = item.a['href']
            title = item.a.text
            #there is not readcount and commentcount， so let both be None
            readCount = commentCount = 0
            #readCount,commentCount = self.getReadAndComment(item('p')[0].text)
        
        
            content = item('p')[1].text
            #print title
            #print readCount+" "+commentCount
            #content =  item.find('p',{'class':'content'}).text
            userInfoTag = item('p')[-1]
            createdAt = self.getTime(userInfoTag.text)
       
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

    def getTime(self,strtime):
        now = datetime.now()
        pattern = re.compile(r"\s*(\d\d\d\d-\d\d-\d\d\s*\d\d:\d\d:\d\d)\s*")
        m = pattern.match(strtime)
        return m.group(1)

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
    obj = FuFengLBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()

if __name__ == "__main__":
    obj = FuFengLBBS(29)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

        
        
