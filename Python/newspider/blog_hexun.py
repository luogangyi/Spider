#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
# update by lgy, 2013.8.4, fix bugs.
# update by lgy, 2013.10.30, fix bugs.
# update by lgy, 2013.12.26, fix bugs.
from BaseTimeLimit import *
from blog_utils import *
from news_hexun import HexunNews
from baidu import Baidu
from google_search import Google

class HexunBlog(BaseBBS):
    '''和讯博客  http://blog.hexun.com/—— 按博客搜索 属于blog故存入blog_posts表'''
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    def nextPage(self,keyword):


        url = 'http://news.search.hexun.com/cgi-bin/search/blog_search.cgi?f=0&key=%s&s=1&pg=1&t=0&rel=' % (keyword.str.encode('gbk'))

        content = urllib2.urlopen(url).read()

        soup = BeautifulSoup(content,fromEncoding='gbk')


        items = soup.find("div",{'class':'search_result'})
        if items == None:
            return []
        items = items.find('div',{"class":'list'})
        if items == None:
            return []
        items = items.ul.findAll('li',recursive=False)
        return items
    
    def itemProcess(self,item):
        ult = item.find('div',{'class':'ul_t'})
        a = ult.find('a')
        url  = a['href']
        title = a.text

        title = self.deleteTag(title)
        createdAt = self.convertTime(ult.h4.text)
        cont = item.find('div',{'class':'cont'}).contents
        content = cont[0]
        content = self.deleteTag(content)

        username = self.getUserName(item.find('div',{'class':'cont'}).find('a').text)
        
        #print url, username, title, content,createdAt
        store_blog_post(url, username, title, content,
                            self.INFO_SOURCE_ID,self.keywordId, createdAt, 0,0)



        
        
    def deleteTag(self,content):
        return BeautifulSoup(content).text
    def getUserName(self,name):
        return name[:name.find('-')].strip()
    def convertTime(self,strtime):
        now = datetime.now()
        pattern = re.compile(r"\d*")

        if strtime.find(u'分钟')>-1:
            m = pattern.search(strtime)
            m = m.group()        
            return now-timedelta(minutes=int(m))
        elif strtime.find(u'天')>-1:
            m = pattern.search(strtime)
            m = m.group()        
            return now-timedelta(days=int(m))
        elif strtime.find(u'小时')>-1:
            m = pattern.search(strtime)
            m = m.group()
            return now-timedelta(hours=int(m))
        else:
            return datetime.strptime(strtime.encode('utf8'),'%Y年%m月%d日 %H:%M')

    def main(self):
        #last_time = session.query(Job).filter(Job.info_source_id==self.INFO_SOURCE_ID).order_by(Job.id.desc()).first().previous_executed    
        # if not self.isCanRun():
        #     return False
        previous_real_count = session.query(News).filter(News.info_source_id==self.INFO_SOURCE_ID).count()
        count = 0
        sql_job = Job()
        sql_job.previous_executed = datetime.now()
        sql_job.info_source_id = self.INFO_SOURCE_ID
        
        count=self.searchWrapper(count)
        #print "count = ",count
        current_real_count = session.query(News).filter(News.info_source_id==self.INFO_SOURCE_ID).count()
        sql_job.fetched_info_count = count
        sql_job.real_fetched_info_count = current_real_count - previous_real_count
        #print "current_real_count = ",current_real_count, "previous_real_count = ",previous_real_count
        session.add(sql_job)
        session.flush()
        session.commit()
        return True

def main(id):
    try:
        obj = HexunBlog(id)
        obj.main()
    except Exception, e:
        store_error(id)
        blog_logger.exception(e)

    # try:
    #     obj = Baidu(id,'blog.hexun.com','blog')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     blog_logger.exception(e)

    # try:
    #     obj = Google(id,'blog.hexun.com','blog')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     blog_logger.exception(e)
        
if __name__=="__main__":
    main(HexunBlog_BLOG_INFO_SOURCE_ID)


