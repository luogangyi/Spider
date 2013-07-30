#! /usr/bin/env python
#coding=utf-8

#update by lgy 2013.7.28 ,add baidu search, fix a bug!
# update by lgy, 2013.7.30, add google search
from BaseBBS import *
from baidu import Baidu
from google_search import Google
class CQKXBBS(BaseBBS):
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    #in this situation, override to set url 
    def nextPage(self,keyword):

        url = 'http://bbs.cqkx.com/forum.php'
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
        keys['srhfid'] =  scbar_form.find('input',attrs={'name':'srhfid'})['value']

        # url = soup.find('a',text=u'按时间排序').parent['href']
        # url = "http://so.dz19.net/"+url
        keyword.str = keyword.str.replace(' ','+')
        url = 'http://bbs.cqkx.com/search.php?searchsubmit=yes&mod=forum&formhash='+\
         keys['formhash'].encode('gbk')+'&srchtype=title&srhfid='+keys['srhfid'].encode('gbk')+'&srhlocality='+keys['srhlocality'].encode('gbk') +'&srchtxt='+ keyword.str.encode('gbk')
        #print url
        response = urllib2.urlopen(url)
        content = response.read()
        soup = BeautifulSoup(content)
        ##############
        # url = 'http://bbs.cqkx.com/search.php?mod=forum&searchid=91&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw=%s' % (keyword.str.encode('gbk'))
        # response = urllib2.urlopen(url)
        # content = response.read()
        # #just need to visit once, because it is order by time in default
        # soup = BeautifulSoup(content)
        items = soup.find("div",id="threadlist")
        if items == None:
            return []
        items = items.findAll("li")
        return items
    
    #in this situation, override to modify the readCount, commentCount
    def itemProcess(self,item):
        url = item.h3.a['href']
        url = "http://bbs.cqkx.com/" + url
        title = item.h3.a.text
        #print title
        #there is not readcount and commentcount， so let both be None
        #readCount = commentCount = 0
#        readCount,commentCount = self.getReadAndComment(item.p.text)
        p_tags = item.findAll('p')
        comment_tag = p_tags[0].text
        readCount,commentCount = self.getReadAndComment(comment_tag)
        content = p_tags[1].text
        #content =  item.find('p',{'class':'content'}).text
        userInfoTag = p_tags [-1]
        createdAt = userInfoTag.find('span').text
        #createdAt = self.convertTime(createdAt)
        username = userInfoTag.a.text
        #print username.encode('utf-8'),content.encode('utf-8'),createdAt, readCount, commentCount
        store_bbs_post(url, username, title, content,
                       self.INFO_SOURCE_ID, self.keywordId, createdAt, readCount, commentCount)
def main(id):
    try:
        obj = CQKXBBS(id)#Source_id defined in bbs_utils.py which is accroding the databse table keywords
        obj.main()

    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)

    try:
        obj = Baidu(id,'bbs.cqkx.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)
    try:
        obj = Google(id,'bbs.cqkx.com','bbs')
        obj.main()
    except Exception, e:
        store_error(id)
        bbs_logger.exception(e)


if __name__ == "__main__":
    main(CQKX_INFO_SOURCE_ID)

        
        