#! /usr/bin/env python
#coding=utf-8
#test by lgy OK! 
from BaseBBS import *

class CDLJL(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)

     #in this situation, override to set url 
    def nextPage(self,keyword):
        try:
            first_url = "http://www.cd090.com/portal.php"
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
            search_url = 'http://search.discuz.qq.com/f/discuz?mod=forum&formhash='+hidden_key_value['formhash']+'&srchtype=title&srhfid=0&sId='+hidden_key_value['sId']+'&ts='+hidden_key_value['ts']+'&cuId=0&cuName=&gId=7&agId=0&egIds=&fmSign=&ugSign7=&sign='+hidden_key_value['sign']+'&charset=gbk&source=discuz&fId=0&q='#+keyword.str.encode('gbk')+'&srchtxt='+keyword.str.encode('gbk')+'&searchsubmit=true'
            search_url = search_url.encode('gbk')+keyword.str.encode('gbk')+'&srchtxt='.encode('gbk')+keyword.str.encode('gbk')+'&searchsubmit=true'.encode('gbk')
            #print search_url

            response = urllib2.urlopen(search_url)

            #print response

            content = response.read()
            #just need to visit once, because it is order by time in default
            soup = BeautifulSoup(content)
            url = soup.find('a',text=u'按时间排序').parent['href']
            url = "http://search.discuz.qq.com/"+url

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
        # try:
        #     url = item.h3.a['href']
        # except Exception, e:
        #     url = item.h4.a['href']
        try:
            url = item.a['href']
            
            # try:
            #     title = item.h3.a.text
            # except Exception, e:
            #     title = item.h4.a.text
            
            title = item.a.text
            #print title

            #print title
            #there is not readcount and commentcount， so let both be None
            readCount = commentCount = 0
            #countinfo = item.p.text
            
            #countinfo = item.p.text[0:item.p.text.find(u"次回复")]

            #readCount = item.p.text[(item.p.text.find(u"–&nbsp;")+7):item.p.text.find(u"次浏览")]



    #        readCount,commentCount = self.getReadAndComment(item.p.text)
        
            #content =  item.find('p',{'class':'content'}).text
            content =  item('p')[1].text
            #print content

            userInfoTag = item('p')[-1]


            createdAt = self.convertTime(userInfoTag.text[0:userInfoTag.text.find(" -")])
            #createdAt = userInfoTag.text.find(" -")  #userInfoTag('span')[0].text # userInfoTag.contents[0].strip()[:-1].strip()

            #createdAt = self.convertTime(createdAt)

            username = userInfoTag('a')[0].text

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
    obj = CDLJL(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    

if __name__ == "__main__":
    obj = CDLJL(31)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    obj.main()
    