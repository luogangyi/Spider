#! /usr/bin/env python
#coding=utf-8

from config import *
from utils import baidu_date_str_to_datetime, blog_logger, store_category, store_error
from blog_utils import *


def search_for_sina_blog_posts():
    last_time = session.query(Job).filter(Job.info_source_id==SINA_BLOG_INFO_SOURCE_ID).order_by(Job.id.desc()).first().previous_executed    

    previous_real_count = session.query(BlogPost).filter(BlogPost.info_source_id==SINA_BLOG_INFO_SOURCE_ID).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = SINA_BLOG_INFO_SOURCE_ID

    for keyword in KEYWORDS :
        finished = False
        page = 1

        while(not finished):
            data = {'q': keyword.str.encode('gbk'),
                    'c': 'blog',
                    'range': 'article',
                    'by': 'title',
                    'sort': 'time',
                    'page': page
                   }
            
            url = "http://search.sina.com.cn/?" + urllib.urlencode(data)

            headers = {
                'Host': 'search.sina.com.cn',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'
            }
    
            req = urllib2.Request(url, headers = headers)  
            response = urllib2.urlopen(req)  
            content = response.read() 
    
            soup = BeautifulSoup(content.decode('gbk', 'ignore'))
            
            posts = soup.findAll('div', attrs={'class': 'r-info r-info2'})
            count = count + len(posts)

            if len(posts) == 0:
                break

            for post in posts:
                url = post.a['href']
                title = post.a.text
                blog_user_screen_name = post.find('a', attrs={'class':
                                                             'fblue'}).text
                created_at = baidu_date_str_to_datetime(post.find('span',
                                                                  attrs={'class': 'fgreen time'}).text)
                content = post.p.text

                counts = get_count_from_url(url)
                read_count = counts['read_count']
                comment_count = counts['comment_count']


                if created_at < last_time:
                    finished = True
                    break

                store_blog_post(url, blog_user_screen_name, title, content,
                                SINA_BLOG_INFO_SOURCE_ID, keyword.id, created_at, read_count, comment_count)

                time.sleep(2)


            time.sleep(10)
            page = page + 1



    current_real_count = session.query(BlogPost).filter(BlogPost.info_source_id==SINA_BLOG_INFO_SOURCE_ID).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()   


def get_count_from_url(blog_url):
    headers = {
        'Host': 'blogtj.sinajs.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'
    }

    aids = blog_url[-6:]
    uid = blog_url[-16:-8]

    url = 'http://blogtj.sinajs.cn/api/num.php?uid=%s&aids=%s' % (uid, aids)
  
    req = urllib2.Request(url, headers = headers)  
    response = urllib2.urlopen(req)  
    content = response.read() 

    index_1 = content.find('"c":')
    index_2 = content.find(',"r":')
    index_3 = content.find(',"f":')

    comment_count = int(content[index_1+4:index_2])
    read_count = int(content[index_2+5:index_3])
    
    return {'read_count':read_count, 'comment_count':comment_count}


def main():
    try:
        search_for_sina_blog_posts()
    except Exception, e:
        store_error(SINA_BLOG_INFO_SOURCE_ID)
        blog_logger.exception(e) 


if __name__ == '__main__':
    main()
