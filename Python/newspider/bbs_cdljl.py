#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.28 ,add baidu search
from BaseBBS import *
from baidu import Baidu
class CDLJL(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)

     #in this situation, override to set url 
    def nextPage(self,keyword):
        
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
        try:
            url = soup.find('a',text=u'按时间排序').parent['href']
        except:
            return []
        url = "http://search.discuz.qq.com/"+url

        #print url
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)

        items = soup.find("span",id="result-items")
        if items == None:
            return []
        items = items == items.findAll("li")

        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):

        url = item.a['href']
        title = item.a.text

        readCount = commentCount = 0
        userInfoTag = item('p')[-1]

        createdAt = self.convertTime(userInfoTag.text[0:userInfoTag.text.find(" -")])
        content =  item('p')[1].text
        username = userInfoTag('a')[0].text
        #print url.encode('utf-8'), username.encode('utf-8'), title.encode('utf-8'), content.encode('utf-8')
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

def main(id):
    try:
        obj = CDLJL(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e) 
    try:
        obj = Baidu(id,'www.cd090.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e) 

if __name__ == "__main__":
    main(CDLJL_INFO_SOURCE_ID)


    