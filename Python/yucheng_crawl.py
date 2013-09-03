#!/usr/bin/python
#-*-coding:utf-8-*-

from config import *
from bbs_utils import *
from utils import baidu_data_str_to_datetime, bbs_logger
from CharacterToGbk import getGBKCode

YUCHENG_INFO_SOURCE_ID = 24
def search_yucheng_for_posts():
    previous_real_count = session.query(BBSPost).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datatime.now()
    sql_job.info_source_id = YUCHENG_INFO_SOURCE_ID

    for keyword in KEYWORDS:
        url = 'http://bbs.yaanren.net/search.php?mod=portal'
        headers = {'Host':'bbs.yaanren.net',
                   'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0'}
        kw = getGBKCode(keyword.str)
        postdata = 'formhash=759e5b39&srchtxt=' + kw + '&searchsubmit=yes'
        req = urllib2.Request(url,data = postdata,headers = headers)

        response = urllib2.urlopen(req)
        content = response.read()

        soup = BeautifulSoup.BeautifulSoup(content)
        posts = soup.findAll('h3')
        count = len(posts)
        for post in posts:
            store_by_bbs_url(post.a['href'], keyword.id)

        current_real_count = session.query(BBSPost).count()

        sql_job.fetched_into_count = count
        sql_job.real_fetched_into_count = current_real_count - previous_real_count

        session.add(sql_job)
        session.flush()
        session.commit()

        
def store_by_bbs_url(url, keyword.id):
    headers = {'Host':'bbs.yaanren.net',
               'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0'}
    req = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    soup = BeautifulSoup.BeautifulSoup(content)
    # title
    t = soup.find('title')
    title = t.text
    print title
    # author
    t = soup.find('div', attrs={'class':'authi'})
    author = t.text
    print author
    # created_at
#    t = soup.findAll('em',attrs={'id':re.compile("authorposton$")})
    t = soup.findAll(text=re.compile(u'发表于'))
    # parse t[0]
    s = t[0]
    pos1 = s.find(" ")
    s = s[pos1:]
    created_at = s.strip()
    print created_at
    # read_count, comment_count
    ts = soup.findAll('span',attrs={'class':'xi1'})
    c = 0
    read_count = 0
    comment_count = 0
    for t in ts:
        if c == 0:
            read_count = t.text
            c = 1
        else:
            comment_count = t.text
    print read_count, comment_count

    # content
    t = soup.find('div', attrs={'class':"t_fsz"})
    comment = t.text
    comment = comment.replace("&nbsp;","")
#    print comment
    s1 = u'本帖最后由'
    s2 = u'编辑'
    pos1 = comment.find(s1)
    pos2 = comment.find(s2)
    print pos1, pos2
    if pos1>=0 and pos2>0:
        comment = comment[pos2+2:]
    print comment
    store_bbs_post(url, author, title, content,
            YUCHENG_INFO_SOURCE_ID, keyword_id, created_at,read_count, comment_count)

def main():
    try:
        search_yucheng_for_posts()
    except Exception, e:
        bbs_logger.exception(e)

if __name__ == '__main__':
    main()
