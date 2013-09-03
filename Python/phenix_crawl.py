#! /usr/bin/python
#-*-coding:utf-8-*-

#import urllib2
#import urllib
#import BeautifulSoup

from config import *
from bbs_utils import *
from utils import baidu_data_str_to_datetime, bbs_logger

PHENIX_INFO_SOURCE_ID = 17

def search_phenix_for_posts():
    previous_real_count = session.query(BBSPost).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = PHENIX_INFO_SOURCE_ID

    for keyword in KEYWORDS:
        data = {'c':5,
                'q':keyword.str} # keyword可以为中文

        url = 'http://bbs.ifeng.com/search.php?' + urllib.urlencode(data)
        headers = {'Host':'www.ifeng.com',
               'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
               'Referer':'http://bbs.ifeng.com/search.php'}

        req = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(req)
        content = response.read()

        soup = BeautifulSoup(content)

        posts = soup.findAll('th')
#        count = count + len(posts)
        valid_count = 0;
        for post in posts:
            s = str(post)
            if s.find('href') != -1:
                if isUrlValid(post.a['href']):
                    valid_count = valid_count + 1
                    store_by_bbs_url(post.a['href'], keyword.id)

        count = count + valid_count
        
        current_real_count = session.query(BBSPost).count()

        sql_job.fetched_into_count = count
        sql_job.real_fetched_into_count = current_real_count - previous_real_count

        session.add(sql_job)
        session.flush()
        session.commit()

def isUrlValid(url):
    if url.find('tid=&') != -1:
        return False
    else:
        return True
    
def store_by_bbs_url(url, keyword_id):
    url = 'http://bbs.ifeng.com/' + url 
    headers = {
            'Host': 'www.ifeng.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
        }
    req = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()

    soup = BeautifulSoup(content)

    title = soup.find('title')
    title = title.text

    usr = soup.find('span',attrs={'class':"fb"})
    author = usr.a.text
    
    info = soup.findAll('li', attrs={'class':"ltx3"})
    created_at = info[0].span.text
    read_count = info[1].span.text
    comment_count = info[2].span.text

    text = soup.find('div', attrs={'class':"para1"})
    content = text.text

    store_bbs_post(url, author, title, content,
                   PHENIX_INFO_SOURCE_ID, keyword_id, created_at,read_count, comment_count)
    time.sleep(10)

    
def main():
    try:
        search_phenix_for_posts()
    except Exception,e :
        bbs_logger.exception(e)

if __name__ == '__main__':
    main()
