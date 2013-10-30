#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
# update by lgy, 2013.10.30, fix bug
from BaseBBS import *
from baidu import Baidu
from google_search import Google

class ZCDBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):
        first_url = "http://www.chengtu.com"
        cookie_jar = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17')]
        urllib2.install_opener(opener)

        # get cookie
        #cookie_url = '''http://www.chengtu.com'''
        #opener.open(cookie_url)


        headers = {
                'Host': 'www.chengtu.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'
        }
    
        req = urllib2.Request(first_url, headers = headers)  
        response = opener.open(req)
        #response = urllib2.urlopen(first_url)
        content = response.read()
        soup = BeautifulSoup(content)
        items = soup.find("form",{'class':'topsearch'}).findAll("input")
        hidden_key_value = {}

        for input_item in items :
            try:
                hidden_key_value[input_item['name']] = input_item['value']
            except:
                break
        
        url='http://www.chengtu.com/search.php?formhash='+hidden_key_value['formhash'].encode('gbk')+\
        '&mod='+hidden_key_value['mod'].encode('gbk')+'&srchtype='+hidden_key_value['srchtype'].encode('gbk')+'&srhfid='+\
        hidden_key_value['srhfid'].encode('gbk')+'&srchtxt='+keyword.str.encode('gbk')+'&orderField=posted&orderType=desc'
        print url

        req = urllib2.Request(url, headers = headers)  
        response = urllib2.urlopen(req)  
        content = response.read()
        #just need to visit once, because it is order by time in default
        soup = BeautifulSoup(content)
        print soup.prettify()
        items = soup.find("span",id="result-items")
        if items == None:
            return []
        items = items.findAll("li")
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):

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
        #print url, username, title, content, createdAt
        store_bbs_post(url, username, title, content,
                   self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)

                    
def main(id):
    # try:
    #     obj = ZCDBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e) 
    try:
        obj = Baidu(id,'www.chengtu.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)

    # try:
    #     obj = Google(id,'www.chengtu.com','bbs')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     bbs_logger.exception(e)

    

if __name__ == "__main__":
    main(ZCD_INFO_SOURCE_ID)


        
        
