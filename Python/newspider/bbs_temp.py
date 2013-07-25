#! /usr/bin/env python
#coding=utf-8

from config import *
from bbs_utils import *
from utils import bbs_logger


gIsFinished = False
gLastTime = 0
gKeywordId = 0
def wrap_search():
    try:
        gLastTime = session.query(Job).filter(Job.info_source_id==DZ19_INFO_SOURCE_ID).order_by(Job.id.desc()).first().previous_executed
        
        previous_real_count = session.query(BBSPost).count()
        count = 0
        sql_job = Job()
        sql_job.previous_executed = datetime.now()
        sql_job.info_source_id = DZ19_INFO_SOURCE_ID
        
        count=search_dz19(count)
        
        current_real_count = session.query(BBSPost).count()
        
        sql_job.fetched_info_count = count
        sql_job.real_fetched_info_count = current_real_count - previous_real_count
        
        session.add(sql_job)
        session.flush()
        session.commit()  
    except:
        print ""
    
def search_dz19(count):
    try:
        for keyword in KEYWORDS:
            global gKeywordId
            gKeywordId = keyword.id
            print 'gk',keyword.id
            print 'gs',gKeywordId
            print keyword.str.encode('gbk')
            keyword = keyword.str.encode('utf8')
            
            pageIndex = 1
            isFinished = False
            while(not isFinished):
                url = "http://so.dz19.net/f/search?q=%s&sId=3075480&ts=1369894104&mySign=0e28fb0d&menu=1&rfh=1&qs=txt.form.a&orderField=posted&orderType=desc&page=%s" % (keyword,pageIndex)
                count += nextPage(url)
                pageIndex += 1
                isFinished = True #just crawl the first page
                
        return count
    except:
        return 0
        
def nextPage(url):
    try:
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)
        items = soup.find("span",id="result-items").findAll("li")
        for item in items:
            itemProcess(item)
        return len(items)
    except:
        return 0
        
def itemProcess(item):
    try:
        url = item.h3.a['href']
        title = item.h3.a.text
        readCount,commentCount = getReadAndComment(item.p.text)
        content =  item.find('p',{'class':'content'}).text
        userInfoTag = item('p')[-1]
        createdAt = userInfoTag.contents[0].strip()[:-1].strip()
        createdAt = convertTime(createdAt)
        username = userInfoTag.a.text
        print createdAt
        print url,title,readCount,commentCount,createdAt,username
        print content
        global gKeywordId
        print 'gg',gKeywordId
        store_bbs_post(url, username, title, content,
                       DZ19_INFO_SOURCE_ID, gKeywordId, createdAt, readCount, commentCount)
    except Exception, e:
        print e

def convertTime(strtime):
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
        
        
#    if createAt < gLastTime:
#        gIsFinished = True
#        return
    


#def getContent(url):
#    content = urllib2.urlopen(url).read()
#    soup = BeautifulSoup(content)
#    
#    postList = soup.find('div',id="postlist")
#    title = postList.table.find('span',id='thread_subject').text
#    content = postList.div
    
    
def getReadAndComment(content):
    print content
    pattern = re.compile(r'\s*(\d*)\D*(\d*)')
    m = pattern.match(content)
    print m.group(2),m.group(1)
    return m.group(2),m.group(1)


    
if __name__ == '__main__':
    wrap_search()