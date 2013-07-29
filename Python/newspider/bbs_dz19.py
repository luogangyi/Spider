#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search,bug fix

from google_search import Google
from BaseBBS import *
from baidu import Baidu
class DZ19BBS(BaseBBS):
    def nextPage(self,keyword):
        url = 'http://www.dz19.net'
        response = urllib2.urlopen(url)
        content = response.read()

        # need to visit again for which order by time, because the default is order by relevancy
        soup = BeautifulSoup(content)
        keys = {}
        scbar_form = soup.find('form',id='scbar_form')

        keys['formhash'] =  scbar_form.find('input',attrs={'name':'formhash'})['value']
        keys['srchtype'] =  scbar_form.find('input',attrs={'name':'srchtype'})['value']
        #keys['ssrhfid'] =  scbar_form.find('input',attrs={'name':'ssrhfid'})['value']
        keys['srhlocality'] =  scbar_form.find('input',attrs={'name':'srhlocality'})['value']
        keys['sId'] =  scbar_form.find('input',attrs={'name':'sId'})['value']
        keys['ts'] =  scbar_form.find('input',attrs={'name':'ts'})['value']
        keys['cuId'] =  scbar_form.find('input',attrs={'name':'cuId'})['value']
        keys['gId'] =  scbar_form.find('input',attrs={'name':'gId'})['value']
        keys['sign'] =  scbar_form.find('input',attrs={'name':'sign'})['value']
        # url = soup.find('a',text=u'按时间排序').parent['href']
        # url = "http://so.dz19.net/"+url
        keyword.str = keyword.str.replace(' ','+')
        url = 'http://so.dz19.net/f/discuz?mod=forum&formhash='+\
         keys['formhash'].encode('gbk')+'&srchtype=title&srhfid=0&srhlocality=portal%3A%3Aindex&sId=' +\
         keys['sId'].encode('gbk')+'&ts='+keys['ts'].encode('gbk')+'&cuId=0&cuName=&gId=7&agId=0&egIds=&fmSign=&ugSign7=&sign='+keys['sign'].encode('gbk')+\
         '&charset=gbk&source=discuz&fId=0&q='+ keyword.str.encode('gbk')+'&srchtxt='+ keyword.str.encode('gbk')+'&searchsubmit=true'
        #print url
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)

        if soup.find('a',text=u'24小时内')==None:
        	return []
        url = soup.find('a',text=u'24小时内').parent['href']
        url = "http://so.dz19.net/"+url
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)

        items = soup.find("span",id="result-items")
        if items == None:
            return []
        items = items.findAll("li")
        return items
    
    

        
    def search4EachItem(self,items):
        for item in items:
            self.itemProcess(item)
            
    def itemProcess(self,item):
        url = item.h3.a['href']
        title = item.h3.a.text
        readCount,commentCount = self.getReadAndComment(item.p.text)
        content =  item.find('p',{'class':'content'}).text
        userInfoTag = item('p')[-1]
        createdAt = userInfoTag.contents[0].strip()[:-1].strip()
        createdAt = self.convertTime(createdAt)
        username = userInfoTag.a.text
        #print url.encode("utf-8"),title.encode("utf-8"),username.encode("utf-8"),createdAt
        #print createdAt
        store_bbs_post(url, username, title, content,
                       self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)
    
    


  
def main(id):
    try:
        obj= DZ19BBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main()	
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    try:
        obj = Baidu(id,'dz19.net','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e) 

if __name__ == "__main__":
    main(DZ19_INFO_SOURCE_ID)


        
        