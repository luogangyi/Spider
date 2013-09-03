#! /usr/bin/python
#-*-coding:utf-8-*-

#import urllib2
#import urllib
#import BeautifulSoup

from config import *
from bbs_utils import *
from utils import baidu_date_str_to_datetime, bbs_logger

PHENIX_INFO_SOURCE_ID = 17

def search_phenix_for_posts():
    previous_real_count = session.query(BBSPost).filter(Job.info_source_id == PHENIX_INFO_SOURCE_ID).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = PHENIX_INFO_SOURCE_ID
#    print KEYWORDS
    i = 0
    for keyword in KEYWORDS:
        i += 1
	print i
        data = {'c':5,
                'q':keyword.str.encode('utf8')}
	print keyword.str
        url = 'http://bbs.ifeng.com/search.php?' + urllib.urlencode(data)
        print url
	headers = {'Host':'www.ifeng.com',
               'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
               'Referer':'http://bbs.ifeng.com/search.php'}

        req = urllib2.Request(url, headers = headers)
#	print 'search: req = Request'
        response = urllib2.urlopen(req)
#	print 'search: response = urlopen'
        content = response.read()
#	print 'search: content...'
        soup = BeautifulSoup(content,fromEncoding='gbk')
#	print 'search: soup'
        posts = soup.findAll('th')
#        count = count + len(posts)
        valid_count = 0;
        for post in posts:
            s = str(post)
            if s.find('href') != -1:
                if isUrlValid(post.a['href']):
		    print post.a['href']
                    valid_count = valid_count + 1
		    print 'store url'
                    store_by_bbs_url(post.a['href'], keyword.id)

        count = count + valid_count
	time.sleep(5)
#    print 'count', count
    current_real_count = session.query(BBSPost).filter(Job.info_source_id==PHENIX_INFO_SOURCE_ID).count()
#    print 'current_real_count', current_real_count
    sql_job.fetched_into_count = count
    sql_job.real_fetched_into_count = current_real_count - previous_real_count

    session.add(sql_job)
#    print 'session.add(sql_job)'
    session.flush()
#    print 'session.flush()'
    session.commit()
#    print 'session.commit()'

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
    print url
    req = urllib2.Request(url, headers = headers)
#    print 'req = urllib2.Request'
    response = urllib2.urlopen(req)
#    print 'response = urlib2.urlopen'
    content = response.read()
#    print 'content = response.read()'

    soup = BeautifulSoup(content,fromEncoding='gbk')
#    print 'soup'
    print 'start parsing soup ...'
    t = soup.find('a',attrs={'class':'ltx2'})
    title = t.text
    title = title.encode('utf-8')
    print title
    usr = soup.find('span',attrs={'class':"fb"})
    author = usr.a.text
    author = author.encode('utf-8')
    print author
    info = soup.findAll('li', attrs={'class':"ltx3"})
    created_at = info[0].span.text
    created_at = created_at.encode('utf-8')
    print created_at
    read_count = info[1].span.text
    comment_count = info[2].span.text
    print read_count, comment_count
    text = soup.find('div', attrs={'class':"para1"})
    content = text.text
    content = content.encode('utf-8')
    print 'store_bbs_post begin ...'
    store_bbs_post(url, author, title, content,
                   PHENIX_INFO_SOURCE_ID, keyword_id, created_at,read_count, comment_count)
    print 'store_bbs_post finished ..'
    time.sleep(10)


    
def main():
    try:
	print 'Start searching phenix ...'
        search_phenix_for_posts()
    except Exception,e :
	print e
        bbs_logger.exception(e)

if __name__ == '__main__':
    main()
