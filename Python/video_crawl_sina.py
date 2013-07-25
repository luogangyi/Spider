#! /usr/bin/env python
#coding=utf-8
##更新于2013.7.4，存储部分未测试
##有翻页
##有对关键词进行二次过滤
##若深入每个视频获取信息，有可能导致URL打开超时，故不再深入
import HTMLParser
import cookielib
from config import *
from utils import store_category, video_logger, recheck_title, store_error


SINA_VIDEO_INFO_SOURCE_ID = 18


def search_for_sina_video_posts():
    previous_real_count = session.query(VideoPost).filter(VideoPost.info_source_id==SINA_VIDEO_INFO_SOURCE_ID).count()

    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = SINA_VIDEO_INFO_SOURCE_ID

    for keyword in KEYWORDS :
        page = 1
        finished = False
        while(not finished and page <=10):
            url = "http://video.sina.com.cn/search/index.php?k="+urllib.quote_plus(keyword.str.encode('utf8'))+"&m1=a&m3=a2&page="+str(page)
            page = page + 1
            #print url

            headers = {
                'Host': 'video.sina.com.cn',
                'Referer': 'http://video.sina.com.cn/search/index.php?',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
            }
            

            req = urllib2.Request(url, headers = headers)  
            response = urllib2.urlopen(req)  
            content = response.read() 
            
            soup = BeautifulSoup(content)
            video_list = soup.find('div',id="contentH")
            if video_list == None:
                finished = True
                break
            divs = video_list.findAll('div')
            if len(divs) == 0 :
                finished = True
                break
            tr_arr = video_list.findAll('tr')
            temp_arr = []

            for i,tr in enumerate(tr_arr):
                try:  
                    if i%2 ==0 :
                        temp_arr = []
                        td_divs = tr.findAll('div', attrs={'class': "v_Info"})
                        for j,td_div in enumerate(td_divs):  
                            name_div = td_div.find('div',attrs={'class':'name'})
                            a_tag = name_div.findAll('a')[1]
                            video_url = a_tag['href']
                            video_title = a_tag['title']
                            temp_arr.append ({'video_url':video_url,'video_title':video_title})
                            #print video_url,video_title
                    else:
                        #print tr.prettify()            
                        td_divs = tr.findAll('div', attrs={'class': "v_Info"})
                        for j,td_div in enumerate(td_divs):  
                            li_arr = td_div.findAll('li')
                            try:
                                video_user = li_arr[0].a['title']
                            except:
                                video_user = li_arr[0].a.text
                            video_createAt = li_arr[1].text
                            created_at = convertTime(video_createAt)

                            video_url = temp_arr[j]['video_url']
                            video_title = temp_arr[j]['video_title']

                            

                            try:
                                play_count = li_arr[2].text
                                play_count = play_count[3:]
                                play_count = play_count.replace(',','')
                                play_count = int(play_count)
                            except:
                                play_count = 0
                            #print "###"+video_title
                            #二次过滤关键词和时间
                            if created_at != -1 and recheck_title(keyword,video_title) ==True:
                                #print video_title,video_url,video_user,created_at,play_count
                                store_by_sina_video_url(video_url, keyword.id,
                                                        video_title,
                                                        video_user, created_at, play_count)


                except Exception, e:
                    store_error(SINA_VIDEO_INFO_SOURCE_ID)
                    video_logger.exception(e)            
                    time.sleep(5)


            time.sleep(5)

    current_real_count = session.query(VideoPost).filter(VideoPost.info_source_id==SINA_VIDEO_INFO_SOURCE_ID).count()


    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()    


def convertTime(strtime):
    now = datetime.now()
    pattern = re.compile(r"(\d+-\d+-\d+)")
    m = pattern.search(strtime)
    if m != None :
        return m.group(1)
    #print m.group(1)
    pattern = re.compile(r"(\d+)")
    m = pattern.search(strtime)
    if m == None :
        return -1
    else:
        m = m.group(1)
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



def getPlayNum(content):
    #print content
    pattern = re.compile(r"\"count\":\"(\d+)\"")
    m = pattern.search(content)
    #m = m.group(1)
    #print m.group(1)
    return  m.group(1)

def getVid(content):
    print content
    pattern = re.compile(r"/(\d+)-(\d+)\.htm")
    m = pattern.search(content)
    #m = m.group(1)
    #print m.group(1)
    return  m.group(1)

def store_by_sina_video_url(url, keyword_id, title, video_user_screen_name,
                            created_at, play_count):
    sql_post = session.query(VideoPost).filter(VideoPost.url==url).first()
    if not sql_post:
       sql_post = VideoPost()

    sql_post.url = url
    sql_post.title = title
    sql_post.keyword_id = keyword_id
    sql_post.video_user_screen_name = video_user_screen_name
    sql_post.info_source_id = SINA_VIDEO_INFO_SOURCE_ID
    sql_post.source_name = u"新浪视频"
    sql_post.created_at = created_at
    sql_post.watch_count = play_count

    session.merge(sql_post) #merge

    session.flush()
    session.commit()

    sql_post = session.query(VideoPost).filter(VideoPost.url==url).first()
    
    if sql_post:
        store_category('video', str(sql_post.id))


def main():
    try:
        search_for_sina_video_posts()
    except Exception, e:
        store_error(SINA_VIDEO_INFO_SOURCE_ID)
        video_logger.exception(e)
    

if __name__ == '__main__':
    main()
