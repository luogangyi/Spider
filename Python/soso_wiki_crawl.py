#! /usr/bin/env python
#coding=utf-8

from config import *
from utils import baidu_date_str_to_datetime, wiki_logger, store_category, store_error


SOSO_WENWEN_INFO_SOURCE_ID = 13


def search_for_soso_wenwen_posts():
    previous_real_count = session.query(WikiPost).filter(WikiPost.info_source_id==SOSO_WENWEN_INFO_SOURCE_ID).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = SOSO_WENWEN_INFO_SOURCE_ID

    count = 0
    
    for st in [1,4]:
        for keyword in KEYWORDS :
            data = {'sp': 'S' + keyword.str.encode('utf8'),
                    'st': st,
                    'sci': 0,
                    'sti': 3
                   }
            
            url = "http://wenwen.soso.com/z/Search.e?" + urllib.urlencode(data)
            #print url

            headers = {
                'Host': 'wenwen.soso.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
            }
        
            req = urllib2.Request(url, headers = headers)  
            response = urllib2.urlopen(req)  
            content = response.read() 
        
            soup = BeautifulSoup(content)

            result_list_soup = soup.find('ol', attrs={'class': "result_list"})
            if result_list_soup == None:
                time.sleep(5)
                continue

            posts = result_list_soup.findAll('li')
            count = count + len(posts)

            for post in posts:
                origin_url = post.a['href']
                tail = origin_url.find('?w=')
                url = 'http://wenwen.soso.com' + origin_url[:tail]

                comment_count_str = post.find('span', attrs={'class':
                                              "solved_time"}).previous.previous.previous.strip()
                tail = comment_count_str.find(u'个回答')
                # print comment_count_str
                comment_count = int(comment_count_str[:tail])

                if st == 1:
                    answered = False
                else:
                    answered = True

                #print url
                #print comment_count

                store_by_wiki_url(url, comment_count, answered, keyword.id)

                
            time.sleep(5)



    current_real_count = session.query(WikiPost).filter(WikiPost.info_source_id==SOSO_WENWEN_INFO_SOURCE_ID).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()    


def store_by_wiki_url(url, comment_count, answered, keyword_id):
    sql_post = session.query(WikiPost).filter(WikiPost.url==url).first()
    if not sql_post:
       sql_post = WikiPost() 

    sql_post.url = url

    sql_post.keyword_id = keyword_id
    sql_post.info_source_id = SOSO_WENWEN_INFO_SOURCE_ID
    sql_post.comment_count = comment_count
    sql_post.answered = answered

    headers = {
        'Host': 'wenwen.soso.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
    }
    
    req = urllib2.Request(url, headers = headers)  
    response = urllib2.urlopen(req)  
    content = response.read() 
    
    soup = BeautifulSoup(content)
    
    wiki_user_screen_name = soup.find('a', attrs={'class':"user_name"})
    if wiki_user_screen_name == None:
        wiki_user_screen_name = u'匿名'
    else:
        wiki_user_screen_name = wiki_user_screen_name.text
    date_str = soup.find('span', attrs={'class':"question_time"}).text
    created_at = baidu_date_str_to_datetime(date_str)
    title = soup.find('h3', attrs={'id':"questionTitle"}).text
    content_div = soup.find('div', attrs={'class':"question_con"})
    if content_div is None:
        content = ""
    else:
        content = content_div.text

    sql_post.read_count = 0
    sql_post.wiki_user_screen_name = wiki_user_screen_name
    sql_post.title = title
    sql_post.content = content
    sql_post.created_at = created_at

    session.merge(sql_post) #merge

    session.flush()
    session.commit()

    sql_post = session.query(WikiPost).filter(WikiPost.url==url).first()
    if sql_post:
        #print "stored"
        store_category('wiki', str(sql_post.id))

    time.sleep(5)
    



def main():
    search_for_soso_wenwen_posts()
    try:
        start_time = datetime.now()
        search_for_soso_wenwen_posts()
        end_time = datetime.now()
        consume_time = end_time - start_time
        wiki_logger.info("soso wenwen consume time: " + str(consume_time))
    except Exception, e:
        store_error(SOSO_WENWEN_INFO_SOURCE_ID)
        wiki_logger.exception(e) 


if __name__ == '__main__':
    main()
