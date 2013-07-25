#! /usr/bin/env python
#coding=utf-8
#ok
from BaseTimeLimit import *
from blog_utils import *
from news_hexun import HexunNews

class HexunBlog(HexunNews):
    '''和讯博客  http://blog.hexun.com/—— 按博客搜索 属于blog故存入blog_posts表'''
    def __init__(self,sourceId):
        BaseBBS.__init__(self,sourceId)
    
    def nextPage(self,keyword):
        try:

            url = 'http://news.search.hexun.com/cgi-bin/search/blog_search.cgi?f=0&key=%s&s=1&pg=1&t=0&rel=' % (keyword.str.encode('gbk'))
    #        print url
            content = urllib2.urlopen(url).read()
    #        print content
            soup = BeautifulSoup(content,fromEncoding='gbk')
        except:
            return []
#        print soup.find("div",{'class':'search_result'})
        try:
            items = soup.find("div",{'class':'search_result'}).find('div',{"class":'list'}).ul.findAll('li',recursive=False)
        except:# there is not any result,so return empty list
            return []
#        print len(items)
        return items
    
    def itemProcess(self,item):
        try:
            ult = item.find('div',{'class':'ul_t'})
            a = ult.find('a')
            url  = a['href']
            title = a.text
            print title
            title = self.deleteTag(title)
            createdAt = self.convertTime(ult.h4.text)
            cont = item.find('div',{'class':'cont'}).contents
            content = cont[0]
            content = self.deleteTag(content)
            
            
            username = self.getUserName(item.find('div',{'class':'cont'}).find('a').text)
            
            store_blog_post(url, username, title, content,
                                self.INFO_SOURCE_ID,self.keywordId, createdAt, 0,0)
        except Exception, e:
            print e


        
        
    def deleteTag(self,content):
        return BeautifulSoup(content).text
    def getUserName(self,name):
        return name[:name.find('-')].strip()
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
            return datetime.strptime(strtime.encode('utf8'),'%Y年%m月%d日 %H:%M')

def main(id):
    obj = HexunBlog(id)
    obj.main()
    
        
if __name__=="__main__":
    obj = HexunBlog(42)
    obj.main()


