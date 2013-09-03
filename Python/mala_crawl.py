#!/usr/bin/python
#-*-coding:utf-8-*-

from config import *
from bbs_utils import *
from utils import baidu_data_str_to_datetime, bbs_logger
from CharacterToGbk import getGBKCode

MALA_CLUB_SOURCE_ID = 21

def search_mala_for_posts():
    previous_real_count = session.query(BBSPost).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datatime.now()
    sql_job.info_source_id = MALA_CLUB_SOURCE_ID
    
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    # login
    url = 'http://www.mala.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
    data = {'username':'tbsinfo',
            'password':'tbs2013',
            'quickforward':'yes',
            'handlekey':'1s'}
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    response = opener.open(req, data)
    content = response.read()
    
    for keyword in KEYWORDS:
        srchtxt = getGBKCode(keyword.str)
        postdata = {'mod':'forum',
                    'formhash':'30cf49f1',
                    'srchtype':'title',
                    'srhfid':"",
                    'srhlocality':'forum%3A%3Aindex',
                    'srchtxt':srchtxt,
                    'searchsubmit':'true'}
        url = 'http://www.mala.cn/search.php?searchsubmit=yes'
        headers = {'Host':'www.mala.cn',
                   'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0',
                   'Referer':'http://www.mala.cn/forum.php'}
        postdata = 'mod=forum&formhash=ef0f28a5&srchtype=title&srhfid=&srhlocality=forum%3A%3Aindex&'
        postdata += 'srchtxt=' + srchtext
        postdata += '&searchsubmit=true'
        req = urllib2.Request(url,data = postdata,headers = headers)

        response = urllib2.urlopen(req)
        content = response.read()

        soup = BeautifulSoup.BeautifulSoup(content)
        posts = soup.findAll('h3', attrs={'class':'xs3'})
        count = len(posts)
        for post in posts:
            store_by_bbs_url(post.a['href'], keyword.id)
#            print post.a['href']
        current_real_count = session.query(BBSPost).count()

        sql_job.fetched_into_count = count
        sql_job.real_fetched_into_count = current_real_count - previous_real_count

        session.add(sql_job)
        session.flush()
        session.commit()

def store_by_bbs_url(url, keyword_id):
    headers = {'Host':'www.mala.cn',
               'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0',
               'Referer':'http://www.mala.cn/forum.php'}
    req = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
#    print content
    soup = BeautifulSoup(content)
    # title
    t = soup.find('h1', attrs={'class':'ts'})
    title = t.text
    print title
    # author
    t = soup.find('div', attrs={'class':'authi'})
    author = t.text
    author = author.replace('&nbsp;',"")
    print author
    # created_at
    t = soup.findAll(text=re.compile(u'发表于'))
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
    print comment
    store_bbs_post(url, author, title, content,
            MALA_CLUB_SOURCE_ID, keyword_id, created_at,read_count, comment_count)

def main():
    try:
        search_mala_for_posts()
    except Exception, e:
        bbs_logger.exception(e)

if __name__ == '__main__':
    main()
