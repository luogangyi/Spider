#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
from google_search import Google
from BaseBBS import *
from baidu import Baidu
class SNW(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)

     #in this situation, override to set url 
    def nextPage(self,keyword):
   
        first_url = "http://www.suiningwang.com/portal.php/"
        response = urllib2.urlopen(first_url)
        content = response.read()
        soup = BeautifulSoup(content)
        items = soup.find("form",id="scbar_form")
        if items == None:
            return []
        items = items.findAll("input",attrs={'type':'hidden'})

        hidden_key_value = {}

        for input_item in items :
            #print input_item["name"]+" "+input_item["value"]
            hidden_key_value[input_item["name"]] = input_item["value"]

        search_url = 'http://search.suiningwang.com/f/discuz?sId='+hidden_key_value['sId']+'&ts='+hidden_key_value['ts']+'&cuId=0&cuName=&gId=7&agId=0&'

        search_url = search_url.encode('utf-8')+'egIds=&fmSign=&ugSign7=&sign='.encode('utf-8')+hidden_key_value['sign'].encode('utf-8')+'&charset=gbk&source=portal&q='.encode('utf-8')+keyword.str.encode('gbk')+'&module=forum'.encode('utf-8')


        response = urllib2.urlopen(search_url)
        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content)

        #print soup
        url = soup.find('a',text=u'按时间排序')
        if url == None:
            return []

        url = url.parent['href']
        url = "http://search.suiningwang.com/"+url

        #print url
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)

        items = soup.find("span",id="result-items")
        if items ==None:
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
        countinfo = item.p.text
        
        countinfo = item.p.text[0:item.p.text.find(u"次回复")]

        readCount = item.p.text[(item.p.text.find(u"–&nbsp;")+7):item.p.text.find(u"次浏览")]

        content =  item('p')[2].text
        #print content

        userInfoTag = item('p')[-1]


        createdAt = self.convertTime(userInfoTag.text[0:userInfoTag.text.find(" -")])

        username = userInfoTag('a')[0].text
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

def main(id):
    try:
        obj = SNW(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main()

    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)

    try:
        obj = Baidu(id,'suiningwang.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)

if __name__ == "__main__":
    main(SNW_INFO_SOURCE_ID)

    