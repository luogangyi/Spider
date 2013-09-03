#!/usr/bin/python
#-*-coding:utf-8-*-

from config import *
from bbs_utils import *
from utils import baidu_date_str_to_datetime, bbs_logger
#from CharacterToGbk import getGBKCode

KAIDI_INFO_SOURCE_ID = 19
def search_kaidi_for_posts():
    #print 'search_kaidi_for_posts'
    previous_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==KAIDI_INFO_SOURCE_ID).count()
    #previous_real_count = session.query(BBSPost).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = KAIDI_INFO_SOURCE_ID

    for keyword in KEYWORDS:
        #print keyword.str.encode('utf-8')

        data = {'q':keyword.str.encode('gbk'),
                'sa':''} # 'sa':'%CB%D1%CB%F7'
        url = 'http://search.kdnet.net/?' + urllib.urlencode(data)


        headers = {'Host':'search.kdnet.net',
               	'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0',
               	'Referer': 'http://search.kdnet.net'}
        req = urllib2.Request(url,headers = headers)
        response = urllib2.urlopen(req)
        content = response.read()

        soup = BeautifulSoup(content,fromEncoding='gbk')
        posts = soup.findAll('h2')
        count += len(posts)
        for post in posts:
            s = str(post)
            pos1 = s.rfind("href")
            pos2 = s.rfind("target")
            s = s[pos1:pos2]
            s = s.strip()
            s = s[6:len(s)-1]
            s = s.replace("amp;","")
            store_by_bbs_url(s, keyword.id)
        time.sleep(1)



    current_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==KAIDI_INFO_SOURCE_ID).count()
    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()

def store_by_bbs_url(url, keyword_id):
    #print url
    headers = {'Host':'club.kdnet.net',
               'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0'}

    req = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
#    print content
    soup = BeautifulSoup(content,fromEncoding='gbk')

    # title
    t = soup.find('div', attrs={'class':'posts-title'})
    title = t.text
    title = title.encode('utf-8')
    # author
    t = soup.find('span', attrs={'class':'name c-main'})
    author = t.text
    author = author.encode('utf-8')
    # created_at
    t = soup.find('div', attrs={'class':'posts-posted'})
    s = t.text
    pos1 = s.find(u'于')
    pos2 = s.find(u'发布在')
    s = s[pos1+1:pos2-1]
    created_at = s.strip()
    created_at = created_at.replace('/','-')
    created_at = created_at.encode('utf-8')
    # print created_at
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

    read_count = int(read_count)
    comment_count = int(comment_count)
    # content, 
    t = soup.find('div', attrs={'class':'posts-cont'})
    s = t.text
    s = s.replace('&nbsp;',"")
    s = s.strip()
    s1 = '<600))||(!(this.width<100)&&!(this.height<100)))window.open'
    s2 = 'if(this.width>=600){this.height=parseInt(this.height*600/this.width);this.width=600;}">'
    pos1 = s.find(s1)
    pos2 = s.rfind(s2)
#    print pos1, pos2
    s3 = s[pos1:pos2+len(s2)] 
    
    content = s.replace(s3,"")
    content = content.encode('utf-8')
    #print content
#	url.encode('utf-8')
    url.encode('utf-8')
    print url, author, title, content,created_at
    store_bbs_post(url, author, title, content,
            KAIDI_INFO_SOURCE_ID, keyword_id, created_at,read_count, comment_count)
    #time.sleep(10)
#    print 'done saving data to db .......'

def main():
    try:
        search_kaidi_for_posts()
    except Exception, e:
        print e
        bbs_logger.exception(e)

if __name__ == '__main__':
    print 'Program started ...'
    main()
