#! /usr/bin/env python
#coding=utf8
# update by lgy, 2013.7.28, add baidu search
# update by lgy, 2013.7.30, add google search
# update by lgy, 2013.12.26, fix bug
from BaseBBS import *
from baidu import Baidu
from google_search import Google
from utils import *

class A028(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        #print keyword.str.encode('utf-8')
        'http://chengdu.tg280.com/f/discuz?mod=forum&formhash=93e22997&srchtype=title&srhfid=0&srhlocality=portal%3A%3Aindex&sId=3441295&ts=1388022832&cuId=0&cuName=&gId=7&agId=0&egIds=&fmSign=&ugSign7=&sign=f80abb9e910afd19843cf88c89385f24&charset=utf-8&source=discuz&fId=0&q=%E9%82%AE%E5%82%A8&srchtxt=%E9%82%AE%E5%82%A8&searchsubmit=true'
        
        url = 'http://www.a028.com/index.php'
        response = urllib2.urlopen(url)
        content = response.read()

        # need to visit again for which order by time, because the default is order by relevancy
        soup = BeautifulSoup(content)
        keys = {}
        scbar_form = soup.find('form',id='scbar_form')

        keys['formhash'] =  scbar_form.find('input',attrs={'name':'formhash'})['value']
        keys['srchtype'] =  scbar_form.find('input',attrs={'name':'srchtype'})['value']
        keys['srhfid'] =  scbar_form.find('input',attrs={'name':'srhfid'})['value']
        keys['srhlocality'] =  scbar_form.find('input',attrs={'name':'srhlocality'})['value']
        keys['sId'] =  scbar_form.find('input',attrs={'name':'sId'})['value']
        keys['ts'] =  scbar_form.find('input',attrs={'name':'ts'})['value']
        keys['cuId'] =  scbar_form.find('input',attrs={'name':'cuId'})['value']
        keys['gId'] =  scbar_form.find('input',attrs={'name':'gId'})['value']
        keys['sign'] =  scbar_form.find('input',attrs={'name':'sign'})['value']
        #keys['ext_vgIds'] = scbar_form.find('input',attrs={'name':'ext_vgIds'})['value']

        url = 'http://chengdu.tg280.com/f/discuz?mod=forum&formhash='+keys['formhash']+\
                '&srchtype=title&srhfid=0&srhlocality=portal%3A%3Aindex&sId='+keys['sId']+\
                '&ts='+keys['ts']+'&cuId=0&cuName=&gId=7&agId=0&egIds=&fmSign=&ugSign7=&sign='+keys['sign']+\
                '&charset=utf-8&source=discuz&fId=0&searchsubmit=true&q='
        url = url.encode('utf-8')+keyword.str.encode('utf-8')+'&srchtxt='.encode('utf-8')+keyword.str.encode('utf-8')


        # url = 'http://www.tg280.com/search.php'
        # response = urllib2.urlopen(url)
        # url = response.geturl()
        # url = url[:url.find('&q=')+3]+(keyword.str.encode('utf-8'))+url[url.find('&q=')+3:]
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)
        try:
            url = soup.find('a',text=u'按时间排序').parent['href']
        except:
            return []
        url = "http://chengdu.tg280.com"+url
        #print url
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)
        #print soup.prettify()
        items = soup.find("span", id="result-items")
        if items == None:
            return []
        items = items.findAll("li")

        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item,keyword):

        url = item.h3.a['href']
        title = item.h3.a.text
        #print title.encode('gbk')
        readCount = commentCount = 0
        content = item.find('p',{'class':'content'}).text
        userInfoTag = item('p')[-1]
        createdAt = userInfoTag.contents[0].strip()[:-1].strip()
        createdAt = self.convertTime(createdAt)
        username = userInfoTag.a.text
        #print title,keyword.str,createdAt

        if not recheck_title(keyword,title):
            return
        #print url.encode('utf-8'), username.encode('utf-8'), title.encode('utf-8'), content.encode('utf-8'),createdAt
        store_bbs_post(url, username, title, content,
                   self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)

    def searchWrapper(self,count):
        for keyword in KEYWORDS:
            self.keywordId = keyword.id
            print keyword.id
#            pageIndex = 1
            isFinished = False
            while not isFinished:                
                items = self.nextPage(keyword)
                count += len(items)
                self.search4EachItem(items,keyword)
#                pageIndex += 1
                isFinished = True #just crawl the first page
                time.sleep(5)
            time.sleep(5)
        return count

    def search4EachItem(self,items,keyword):
        for item in items:
            self.itemProcess(item,keyword)
def main(id):
    try:
        obj = A028(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    # try:
    #     obj = Baidu(id,'www.tg280.com','bbs')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e)  
    # try:
    #     obj = Google(id,'www.tg280.com','bbs')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e) 



if __name__ == "__main__":
    main(A028_INFO_SOURCE_ID)
    

        
        
