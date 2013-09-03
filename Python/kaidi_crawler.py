#!/usr/bin/python
#-*-coding:utf-8-*-

from config import *
from bbs_utils import *
from utils import baidu_data_str_to_datetime, bbs_logger
from CharacterToGbk import getGBKCode

KAIDI_INFO_SOURCE_ID = 19
def search_kaidi_for_posts():
    previous_real_count = session.query(BBSPost).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datatime.now()
    sql_job.info_source_id = KAIDI_INFO_SOURCE_ID

    for keyword in KEYWORDS:
        kw = getGBKCode(keyword.str)
        data = {'q':kw,
                'sa':'%CB%D1%CB%F7'}
        url = 'http://search.kdnet.net/?' + urllib.urlencode(data)
        headers = {'Host':'search.kdnet.net',
               'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
               'Referer': 'http://search.kdnet.net'}
        req = urllib2.Request(url,headers = headers)
        response = urllib2.urlopen(req)
        content = response.read()
        soup = BeautifulSoup.BeautifulSoup(content)
        posts = soup.findAll('h2')
        count = len(posts)
        for post in posts:
            s = str(post)
            pos1 = s.rfind("href")
            pos2 = s.rfind("target")
            s = s[pos1:pos2]
            s = s.strip()
            s = s[6:len(s)-1]
            s = s.replace("amp;","")
            store_by_bbs_url(s, keyword.id)

        current_real_count = session.query(BBSPost).count()

        sql_job.fetched_into_count = count
        sql_job.real_fetched_into_count = current_real_count - previous_real_count

        session.add(sql_job)
        session.flush()
        session.commit()

def store_by_bbs_url(url, keyword_id):
    headers = {'Host':'search.kdnet.net',
               'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
               'Referer': 'http://search.kdnet.net'}
    req = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
#    print content
    soup = BeautifulSoup(content)

    # title
    t = soup.find('div', attrs={'class':'posts-title'})
    title = t.text

    # author
    t = soup.find('span', attrs={'class':'name c-main'})
    author = t.text
    # created_at
    t = soup.find('div', attrs={'class':'posts-posted'})
    s = t.text
    pos1 = s.find(u'于')
    pos2 = s.find(u'发布在')
    s = s[pos1+1:pos2-1]
    created_at = s.strip()

    # comment count, read count
    ts = soup.findAll('span', attrs={'class':'f10px fB c-alarm'})
    i = 0
    read_count = 0
    comment_count = 0
    for t in ts:
        if i == 0:
            read_count = t.text
            i += 1
        else:
            comment_count = t.text

    # content, 
    t = soup.find('div', attrs={'class':'posts-cont'})
    s = t.text
    s = s.replace('&nbsp;',"")
    s = s.strip()
    img = '''<600))||(!(this.width<100)&&!(this.height<100)))window.open('http://club.kdnet.net/atlas/index.asp?id=9372065&pic;='+escape(this.src.replace('.cat898.com/','.kdnet.net/').replace('/UploadSmall/','/Upload/')));"  class="img-src"   onload="javascript:if (this.width>=600 || (this.width>=100 && this.height>=100)){this.style.cursor='pointer';}if(this.width>=600){this.height=parseInt(this.height*600/this.width);this.width=600;}">'''
    content = s.replace(img,"")

    store_bbs_post(url, author, title, content,
            KAIDI_INFO_SOURCE_ID, keyword_id, created_at,read_count, comment_count)

def main():
    try:
        search_kaidi_for_posts()
    except Exception, e:
        bbs_logger.exception(e)

if __name__ == '__main__':
    main()
