#! /usr/bin/env python
#coding=utf-8
## 更新与2013.7.2日,获取全网数据
## 过滤了优酷、土豆、新浪的视频，过滤了关键词，因此结果较少
## 写数据库部分未测试！！
from config import *
import HTMLParser
from utils import store_category, video_logger, recheck_title, store_error

ALL_VIDEO_INFO_SOURCE_ID = 19

def search_for_youku_global_video_posts():
    previous_real_count = session.query(VideoPost).filter(VideoPost.info_source_id==ALL_VIDEO_INFO_SOURCE_ID).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = ALL_VIDEO_INFO_SOURCE_ID
    html_parser = HTMLParser.HTMLParser()

    for keyword in KEYWORDS :
        page = 1
        finished = False
        while(not finished):
            url = "http://www.soku.com/v?keyword="+urllib.quote_plus(keyword.str.encode('utf8')) +"&orderfield=1&time_length=0&limit_date=7&hd=0&ext=2&curpage="+str(page)
            page = page + 1

            headers = {
                'Host': 'www.soku.com',
                'Referer': 'http://www.soku.com/search_video/',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
            }

            # print keyword.str,url,page
            req = urllib2.Request(url, headers = headers)  
            response = urllib2.urlopen(req)  
            content = response.read() 
            
            soup = BeautifulSoup(content)
            #items = soup.findAll('div', attrs={'class': 'items'})

            posts = soup.findAll('div', attrs={'class': "v"})
            count = count + len(posts)

            if len(posts)==0:
                finished = True
                break
            # print "page" + str(page) +"\n"
            for post in posts:
                # 站名，要过滤来自优酷、土豆、新浪的视频
                source_name = post.find('span', attrs={'class': "siteurl"}).text
                v_meta_title =  post.find('div', attrs={'class': "v-meta-title"})
                title = v_meta_title.a['title']
                title = html_parser.unescape(title)
                url = v_meta_title.a['href']

                if source_name.find(u"优酷")>=0:
                    continue
                if source_name.find(u"土豆")>=0:
                    continue
                if source_name.find(u"新浪")>=0:
                    continue
                if not recheck_title(keyword,title):
                    continue

                #print source_name,title,url

                store_by_video_url(url, keyword.id, title, source_name)

            time.sleep(5)


    current_real_count = session.query(VideoPost).filter(VideoPost.info_source_id==ALL_VIDEO_INFO_SOURCE_ID).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()    


def convertURL(url):
    now = datetime.now()
    pattern = re.compile(r".*url=(.*)")
    m = pattern.match(url)
    return m.group(1)

def convertTime(strtime):
    now = datetime.now()
    pattern = re.compile(r"\d*")

    if strtime.find(u'天')>-1:
        m = pattern.search(strtime)
        m = m.group()    
        # print m
        return now-timedelta(days=int(m))
    elif strtime.find(u'小时')>-1:
        m = pattern.search(strtime)
        m = m.group()
        return now-timedelta(hours=int(m))
    else:
        return now


def store_by_video_url(url, keyword_id, title, source_name):
    sql_post = session.query(VideoPost).filter(VideoPost.url==url).first()
    if not sql_post:
       sql_post = VideoPost()

    sql_post.url = url
    sql_post.title = title
    sql_post.keyword_id = keyword_id
    sql_post.created_at = datetime.now()
    sql_post.info_source_id = ALL_VIDEO_INFO_SOURCE_ID
    sql_post.source_name = source_name


    session.merge(sql_post) #merge

    session.flush()
    session.commit()

    sql_post = session.query(VideoPost).filter(VideoPost.url==url).first()
    if sql_post:
        store_category('video', str(sql_post.id))


def main():
    try:
        search_for_youku_global_video_posts()
    except Exception, e:
        store_error(ALL_VIDEO_INFO_SOURCE_ID)
        video_logger.exception(e)
    

if __name__ == '__main__':
    main()
