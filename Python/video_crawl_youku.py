#! /usr/bin/env python
#coding=utf-8
## 更新与2013.7.4日,只获取优酷站内数据
## 搜索时间限制 1周内
## 有翻页
## 有对关键词进行二次过滤
## 写数据库部分未测试！！
from config import *
import HTMLParser
from utils import store_category, video_logger, recheck_title, store_error

YOUKU_INFO_SOURCE_ID = 3

def search_for_youku_video_posts():
    previous_real_count = session.query(VideoPost).filter(VideoPost.info_source_id==YOUKU_INFO_SOURCE_ID).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = YOUKU_INFO_SOURCE_ID
    html_parser = HTMLParser.HTMLParser()

    for keyword in KEYWORDS :
        page = 1
        finished = False
        while(not finished and page <=10):
            url = "http://www.soku.com/search_video/q_" + urllib.quote_plus(keyword.str.encode('utf8')) + '_limitdate_7_orderby_2_pagesize_20_page_'+str(page)
            page = page + 1
            # print url
            headers = {
                'Host': 'www.soku.com',
                'Referer': 'http://www.soku.com/search_video/',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
            }

            req = urllib2.Request(url, headers = headers)  
            response = urllib2.urlopen(req)  
            content = response.read() 
            
            soup = BeautifulSoup(content)

            posts = soup.findAll('div', attrs={'class': "v"})
            count = count + len(posts)
            if len(posts)==0:
                finished = True
                break

            for post in posts:
                try:
                    video_user_screen_name = post.find('span', attrs={'class': "username"}).text
                    deltatime = post.find('span', attrs={'class': "pub"}).text
                    v_meta_title =  post.find('div', attrs={'class': "v-meta-title"})
                    title = v_meta_title.a['title']
                    title = html_parser.unescape(title)
                    url = v_meta_title.a['href']

                    try:
                        v_meta_entry = post.find('div',attrs={'class':"v-meta-entry"})
                        v_meta_datas = v_meta_entry.findAll('div',attrs={'class':"v-meta-data"})
                        playcount = v_meta_datas[1].text
                        playcount = playcount[playcount.find(":")+1:]
                        playcount = playcount.replace(',','')
                        playcount = int(playcount)
                    except:
                        playcount = 0
                    # 对关键词进行重新过滤
                    if not recheck_title(keyword,title):
                        continue
                   
                    try:
                        created_at = convertTime(deltatime)
                    except:
                        created_at = datetime.now()

                    #print video_user_screen_name,created_at,title,url,playcount
                    store_by_video_url(url, keyword.id, title,
                                       video_user_screen_name, created_at)
                    time.sleep(5)


                except Exception, e:
                    store_error(YOUKU_INFO_SOURCE_ID)
                    video_logger.exception(e)            
                    time.sleep(5)

            time.sleep(5)
            

    current_real_count = session.query(VideoPost).filter(VideoPost.info_source_id==YOUKU_INFO_SOURCE_ID).count()


    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()    


def convertTime(strtime):
    now = datetime.now()
    pattern = re.compile(r".*(\d+).*")
    m = pattern.match(strtime)
    m = m.group(1)
    #print m.group(1)
    time = -1
    #print strtime
    if strtime.find(u'年')>-1:  
        return -1
    elif strtime.find(u'月')>-1:
        time = now-timedelta(days=(int(m)*30))
    elif strtime.find(u'天')>-1: 
        time =  now-timedelta(days=int(m))
    elif strtime.find(u'小时')>-1:
        time =  now-timedelta(hours=int(m))
    else:
        time = now
    return time.strftime("%Y-%m-%d")


def store_by_video_url(url, keyword_id, title, video_user_screen_name,
                       created_at):
    sql_post = session.query(VideoPost).filter(VideoPost.url==url).first()
    if not sql_post:
       sql_post = VideoPost()

    sql_post.url = url
    sql_post.title = title
    sql_post.keyword_id = keyword_id
    sql_post.video_user_screen_name = video_user_screen_name
    sql_post.created_at = created_at
    sql_post.info_source_id = YOUKU_INFO_SOURCE_ID
    sql_post.source_name = u"优酷"
    #sql_post.watch_count = watch_count

    headers = {
        'Host': 'v.youku.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
    }

    req = urllib2.Request(url, headers = headers)  
    response = urllib2.urlopen(req)  
     
    video_id = ''
    for line in response.readlines():
        if line.find('videoId') > 0:
            start = line.find("= '")
            end = line.find("';")
            video_id = line[start+3:end]
            break

    if video_id == '':
        return

    stat_url = "http://v.youku.com/v_vpactionInfo/id/" + video_id + "/pm/1?__rt=1&__ro=info_stat"
    
    req = urllib2.Request(stat_url, headers = headers)  
    response = urllib2.urlopen(req)
    content = response.read() 
        
    soup = BeautifulSoup(content)

    nums = soup.findAll('span', attrs={'class': "num"})
    sql_post.watch_count = int(nums[0].text.replace(',',''))

    up_down = nums[1].text.replace(',','').split(' / ')
    sql_post.up_count = int(up_down[0])
    sql_post.down_count = int(up_down[1])

    sql_post.comment_count = int(nums[3].text.replace(',',''))

    try:
        sql_post.repost_count = int(nums[4].text.replace(',',''))
    except:
        sql_post.repost_count = 0

    #print sql_post.watch_count, sql_post.up_count, sql_post.down_count, sql_post.comment_count
    session.merge(sql_post) #merge

    session.flush()
    session.commit()

    sql_post = session.query(VideoPost).filter(VideoPost.url==url).first()
    if sql_post:
        store_category('video', str(sql_post.id))



def main():
    try:
        search_for_youku_video_posts()
    except Exception, e:
        store_error(YOUKU_INFO_SOURCE_ID)
        video_logger.exception(e)
    

if __name__ == '__main__':
    main()
