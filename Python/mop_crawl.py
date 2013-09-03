#!/usr/bin/python
#-*-coding:utf-8-*-

from config import *
from bbs_utils import *
from utils import baidu_data_str_to_datetime, bbs_logger

MOP_INFO_SOURCE_ID = 20
def search_dzh_mop():
    previous_real_count = session.query(BBSPost).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datatime.now()
    sql_job.info_source_id = MOP_INFO_SOURCE_ID
    
    url = 'http://dzh.mop.com/'
    headers = {'Host':'dzh.mop.com',
               'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0'}
    req = urllib2.Request(url,headers = headers)
    print url
    response = urllib2.urlopen(req)
    content = response.read()
#    print content
    soup = BeautifulSoup.BeautifulSoup(content)
    posts = soup.findAll('li', attrs={'onmouseover':'MOP.DZH.liHover(this)'})

    for keyword in KEYWORDS:
        count = 0
        for post in posts:
            text = post.text
            url = post.a['href']
            if text.find(k.str)>0:
                count += 1
                store_by_bbs_url(url,keyword.id)

        current_real_count = session.query(BBSPost).count()

        sql_job.fetched_into_count = count
        sql_job.real_fetched_into_count = current_real_count - previous_real_count

        session.add(sql_job)
        session.flush()
        session.commit()
    

def store_by_bbs_url(url, keyword_id):
    url = 'http://dzh.mop.com' + url
    headers = {'Host':'dzh.mop.com',
               'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0'}
    req = urllib2.Request(url,headers = headers)
    print url
    response = urllib2.urlopen(req)
    content = response.read()
#    print content
    soup = BeautifulSoup.BeautifulSoup(content)
    # title
    t = soup.find('meta', attrs={'name':'description'})
    title = t['content']
    print title
    # author
    t = soup.find('meta', attrs={'name':'author'})
    author = t['content']
    print author
    # created_at
    t = soup.find('li', attrs={'class':'tzrq'})
    created_at = t.text
    print created_at
    # read_count, comment_count
    t = soup.find('div',attrs={'class':'llhfP'})
    s = t.text
    pos = s.find("&nbsp;")
    s = s[:pos]
    s = s.strip()
    pos = s.find(u'回复数：')
    read_count = s[4:pos]
    comment_count = s[pos+4:]
    print read_count, comment_count
    # content
    t = soup.find('div',attrs={'class':'tznrP'})
    content = t.text
    content = content.replace("&nbsp;","")
    print content
    store_bbs_post(url, author, title, content,
            MOP_INFO_SOURCE_ID, keyword_id, created_at,read_count, comment_count)

def main():
    try:
        search_mala_for_posts()
    except Exception, e:
        bbs_logger.exception(e)

if __name__ == '__main__':
    main()
