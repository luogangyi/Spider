#! /usr/bin/env python
#coding=utf-8
#update by lgy 2013.7.29 ,add baidu search
# update by lgy, 2013.7.30, add google search
# update by lgy, 2013.8.4, fix bugs.
from BaseTimeLimit import *
from blog_utils import *
from news_eastmoney import EastMoneyNews
from baidu import Baidu
from google_search import Google

class EastMoneyBlog(EastMoneyNews):
    '''东方财富博客   http://blog.eastmoney.com/ —— 按博客搜索 属于blog故存入blog_posts表'''
    def __init__(self,sourceId):
        EastMoneyNews.__init__(self,sourceId)
    
    def nextPage(self,keyword):

        url = 'http://so.eastmoney.com/Search.ashx?qw=%s&qt=3&sf=0&st=1&cpn=1&pn=10&f=0&p=0' % (keyword.str.encode('utf8'))
        
        content = urllib2.urlopen(url).read()
        import json
        js = json.loads(content[content.find('{'):-1])
#        print content
        try:
            items = js['DataResult']
        except:# there is not any result,so return empty list
            return []
      
        return items

    def itemProcess(self,item):
        
    
        content = BeautifulSoup(item['Description']).text
        title = BeautifulSoup(item['Title']).text
        #print item['Url'], item['Author'], title, content, item['ShowTime']
        store_blog_post(item['Url'], item['Author'], title, content,
                            self.INFO_SOURCE_ID,self.keywordId, item['ShowTime'],0,0 )

        
        
        
    def convertTime(self,createdAt):
        return datetime.strptime(createdAt,'%Y-%m-%d')

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
        obj = EastMoneyBlog(id)
        obj.main()
    except Exception, e:
        store_error(id)
        blog_logger.exception(e)

    # try:
    #     obj = Baidu(id,'blog.eastmoney.com','blog')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     blog_logger.exception(e)
        
    # try:
    #     obj = Google(id,'blog.eastmoney.com','blog')
    #     obj.main()
    # except Exception, e:
    #     store_error(id)
    #     blog_logger.exception(e)
    
   

if __name__=="__main__":
    main(EastMoney_Blog_BLOG_INFO_SOURCE_ID)

