#! /usr/bin/env python
#coding=utf-8
# update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
# update by lgy, 2013.12.25, fix bug
from BaseBBS import *
from baidu import Baidu
from google_search import Google

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

        #search_url = 'http://search.suiningwang.com/f/discuz?sId='+hidden_key_value['sId']+'&ts='+hidden_key_value['ts']+'&cuId=0&cuName=&gId=7&agId=0&'
        
        #search_url = search_url.encode('utf-8')+'egIds=&fmSign=&ugSign7=&sign='.encode('utf-8')+hidden_key_value['sign'].encode('utf-8')+'&charset=gbk&source=portal&q='.encode('utf-8')+keyword.str.encode('gbk')+'&module=forum'.encode('utf-8')

        search_url = 'http://www.suiningwang.com/search.php?searchsubmit=yes&mod=forum&formhash='+hidden_key_value['formhash']+'&srchtype=title&srhfid=0&srhlocality=portal::index&searchsubmit=true&srchtxt='
        search_url = search_url.encode('gbk')+keyword.str.encode('gbk')

        response = urllib2.urlopen(search_url)
        content = response.read()
        soup = BeautifulSoup(content)

        items = soup.findAll("li",attrs={'class':'pbw'})
        
        return items

    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        url = 'http://www.suiningwang.com/'+item.h3.a['href']
        title = item.h3.a.text
        #print title
        #there is not readcount and commentcount， so let both be None
        readCount = commentCount = 0
        countinfo = item.find("p",attrs={'class':'xg1'}).text
        commentCount,readCount = self.getCommentInfo(countinfo)
        #print commentCount,readCount

        content =  item('p')[-2].text
        #print content

        userInfoTag = item('p')[-1]


        createdAt = self.convertTime(userInfoTag.text[0:userInfoTag.text.find(" -")])
        #print createdAt
        username = userInfoTag('a')[0].text
        print url, username, title, content,createdAt
        store_bbs_post(url, username, title, content,
                        self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)


        
    
    def getCommentInfo(self,countinfo):
        pattern = re.compile(r"(\d+).*?(\d+).*?")
        m = pattern.search(countinfo)
        if m.group()!=None: 
            return m.group(1),m.group(2)
        return 0,0

    def convertTime(self,strtime):
        pattern = re.compile(r"\d+-\d+-\d+")
        m=pattern.search(strtime)
        if m !=None:
            return m.group()
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

    # try:
    #     obj = Baidu(id,'suiningwang.com','bbs')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e)
        
    # try:
    #     obj = Google(id,'suiningwang.com','bbs')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e)

if __name__ == "__main__":
    main(SNW_INFO_SOURCE_ID)

    