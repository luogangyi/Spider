#! /usr/bin/env python
#coding=utf-8

from config import *
from bbs_utils import *
from utils import baidu_date_str_to_datetime, bbs_logger, store_error


def search_for_tianya_bbs_posts():
    previous_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==TIANYA_INFO_SOURCE_ID).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = TIANYA_INFO_SOURCE_ID

    count = 0

    for keyword in KEYWORDS :
        data = {'q': keyword.str.encode('utf8'),
                's': 4,
                'f': 3
               }
        
        url = "http://www.tianya.cn/search/bbs?" + urllib.urlencode(data)

        headers = {
            'Host': 'www.tianya.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
            'Referer': 'http://www.tianya.cn/search/bbs'            
        }
    
        req = urllib2.Request(url, headers = headers)  
        response = urllib2.urlopen(req)  
        content = response.read() 
    
        soup = BeautifulSoup(content)
        
        posts = soup.findAll('h3')
        count = count + len(posts)

        for post in posts:
            store_by_bbs_url(post.a['href'], keyword.id)

    current_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==TIANYA_INFO_SOURCE_ID).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()   


def search_for_tianya_bbs_315_posts():
    previous_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==TIANYA_INFO_SOURCE_ID).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.theme_id = 0
    sql_job.info_source_id = TIANYA_INFO_SOURCE_ID

    count = 0

    for keyword in KEYWORDS :
        data = {'k': keyword.str.encode('utf8'),
                'item': 837,
                'grade': 0,
                'order': 1,
                'su': 0
               }
        
        url = "http://bbs.tianya.cn/list.jsp?" + urllib.urlencode(data)

        headers = {
            'Host': 'bbs.tianya.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
            'Referer': 'http://bbs.tianya.cn/'            
        }
    
        req = urllib2.Request(url, headers = headers)  
        response = urllib2.urlopen(req)  
        content = response.read() 
    
        soup = BeautifulSoup(content)
        
        posts = soup.findAll('td', attrs={'class': "td-title "})
        count = count + len(posts)

        for post in posts:
            store_by_bbs_url("http://bbs.tianya.cn" + post.a['href'], keyword.id)
        
        time.sleep(5)

    current_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==TIANYA_INFO_SOURCE_ID).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()


def store_by_bbs_url(url, keyword_id):
    headers = {
            'Host': 'bbs.tianya.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
    }
    
    req = urllib2.Request(url, headers = headers)  
    response = urllib2.urlopen(req)  
    content = response.read()  

    soup = BeautifulSoup(content)

    title = soup.find('span', attrs={'class': "s_title"})
    title = title.span.text

    info_soup = soup.find('div', attrs={'class': "atl-info"})
    infos = info_soup.findAll('span')
    
    bbs_user_screen_name = infos[0].a.text
    if infos[1].a is None:
        created_at = baidu_date_str_to_datetime(infos[1].text[3:])
        read_count = int(infos[2].text[3:])
        comment_count = int(infos[3].text[3:])
    else:
        created_at = baidu_date_str_to_datetime(infos[2].text[3:])
        read_count = int(infos[3].text[3:])
        comment_count = int(infos[4].text[3:])

    content_div = soup.find('div', attrs={'class': "bbs-content clearfix"})
    content = content_div.text

    
    store_bbs_post(url, bbs_user_screen_name, title, content,
                   TIANYA_INFO_SOURCE_ID, keyword_id, created_at, read_count, comment_count)

    time.sleep(10)


def main():
    try:
        search_for_tianya_bbs_posts()
        search_for_tianya_bbs_315_posts()
    except Exception, e:
        store_error(TIANYA_INFO_SOURCE_ID)
        bbs_logger.exception(e) 



if __name__ == '__main__':
    main()
