#! /usr/bin/env python
#coding=utf-8
# 更新于 2013.07.18
from config import *
from bbs_utils import *
from utils import baidu_date_str_to_datetime, bbs_logger, store_error


def search_for_baidu_tieba_posts():
    last_time = session.query(Job).filter(Job.info_source_id==BAIDU_TIEBA_INFO_SOURCE_ID).order_by(Job.id.desc()).first().previous_executed    

    previous_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==BAIDU_TIEBA_INFO_SOURCE_ID).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = BAIDU_TIEBA_INFO_SOURCE_ID

    for keyword in KEYWORDS :
        finished = False
        page = 1

        while(not finished):
            data = {'qw': keyword.str.encode('gbk'),
                    'isnew': 1,
                    'rn': 20,
                    'sm': 1,
                    'pn': page
                   }
            
            url = "http://tieba.baidu.com/f/search/res?" + urllib.urlencode(data)
            #print url,keyword.str
            headers = {
                'Host': 'tieba.baidu.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'
            }
    
            req = urllib2.Request(url, headers = headers)  
            response = urllib2.urlopen(req)  
            content = response.read() 
    
            soup = BeautifulSoup(content.decode('gbk', 'ignore'))
            
            posts = soup.findAll('div', attrs={'class': 's_post'})
            count = count + len(posts)
            # print count


            for post in posts:
                temp_url = post.a['href']
                url = 'http://tieba.baidu.com'+ temp_url#[:tail-1]
                title = post.a.text
                #print title
                content = post.find('div', attrs={'class': 'p_content'}).text
                bbs_a_tags = post.findAll('a')
                bbs_user_screen_name = bbs_a_tags[-1].text
                created_at_str = post.findAll('font', attrs={'class': 'p_green'})[-1].text
                created_at = baidu_date_str_to_datetime(created_at_str)


                if created_at < last_time:
                    finished = True
                    break

                if title[0:3] == u'回复:':
                    continue

                comment_count = get_comment_count(url)
                read_count = 0
                #print url,title,bbs_user_screen_name,created_at,comment_count
                store_bbs_post(url, bbs_user_screen_name, title, content,
                               BAIDU_TIEBA_INFO_SOURCE_ID, keyword.id, created_at, read_count, comment_count)

                time.sleep(5)


            time.sleep(10)
            page = page + 1

            if len(posts) == 0:
                break


    current_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==BAIDU_TIEBA_INFO_SOURCE_ID).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()   


def get_comment_count(url):
    headers = {
            'Host': 'tieba.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'
        }
    
    req = urllib2.Request(url, headers = headers)  
    response = urllib2.urlopen(req)  
    content = response.read()  

    soup = BeautifulSoup(content)

    span = soup.find('span', attrs={'class': "red", 'style': "margin-right:3px"})

    if span != None:
        return int(span.text)
    else:
        return 0


def main():
    try:
        start_time = datetime.now()
        search_for_baidu_tieba_posts()
        end_time = datetime.now()
        consume_time = end_time - start_time
        bbs_logger.info("baidu tieba consume time: " + str(consume_time))
    except Exception, e:
        store_error(BAIDU_TIEBA_INFO_SOURCE_ID)
        bbs_logger.exception(e) 


if __name__ == '__main__':
    main()
