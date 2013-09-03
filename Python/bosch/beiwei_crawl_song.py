#!/usr/bin/python
#-*-coding:utf-8-*-

from config import *
from bbs_utils import *
from utils import bbs_logger
#from CharacterToGbk import getGBKCode
from datetime import date

BEIWEI_INFO_SOURCE_ID = 23

def search_beiwei_for_posts():
#    last_time = session.query(Job).filter(Job.info_source_id==BEIWEI_INFO_SOURCE_ID).order_by(Job.id.desc()).first().previous_executed    

    previous_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==BEIWEI_INFO_SOURCE_ID).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = BEIWEI_INFO_SOURCE_ID

    for keyword in KEYWORDS:
#        print keyword.str.encode('utf-8')
#        url = 'http://bbs.beiww.com/search.php?mod=forum&searchid=18&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw='+keyword.str.encode('gbk')
        url = 'http://bbs.beiww.com/search.php?mod=forum'
        headers = {'Host':'bbs.beiww.com',
                   'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0'}
        #kw = getGBKCode(keyword.str)
#        postdata = 'formhash=9acf9d1c&srchtxt=' +  keyword.str.encode('gbk') + '&searchsubmit=yes'
	data = {'formhash':'9acf9d1c',
		'srchtxt':keyword.str.encode('gbk'),
		'searchsubmit':'yes'}
	postdata = urllib.urlencode(data)
#        postdata = 'formhash=9acf9d1c&srchtxt='+ '%BB%AA%CE%AA' + '&searchsubmit=yes'
        req = urllib2.Request(url,data = postdata, headers = headers)
	print postdata
        response = urllib2.urlopen(req)
        content = response.read()
        soup = BeautifulSoup(content,fromEncoding='gbk')
        posts = soup.findAll('h3')
        count += len(posts)
	print len(posts)
        for post in posts:
	    print post.a['href']
            store_by_bbs_url('http://bbs.beiww.com/'+post.a['href'], keyword.id)
	time.sleep(5)
    current_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==BEIWEI_INFO_SOURCE_ID).count()

    sql_job.fetched_info_count = count
    print 'count:', count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count
    print 'real_fetched_into_count:', current_real_count - previous_real_count
    session.add(sql_job)
    session.flush()
    session.commit()

def store_by_bbs_url(url, keyword_id):
    print 'store_by_bbs_url:', url
    headers = {'Host':'bbs.beiww.com',
               'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0'}
    req = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    soup = BeautifulSoup(content)
    # title
    t = soup.find('h1',attrs={'class':'ts'})
    title = t.text
    title = title.replace(u'[复制链接]',"")
    title = title.encode('utf-8')
    print title
    # author
    t = soup.find('div', attrs={'class':'authi'})
    author = t.text
    author = author.encode('utf-8')
    print author
    # created_at
    t = soup.findAll(text=re.compile(u'发表于'))
    s = t[0]
    pos1 = s.find(" ")
    s = s[pos1:]
    created_at = s.strip()
    print created_at.encode('utf-8')
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
    # comment
    t = soup.find('div', attrs={'class':"t_fsz"})
    content = t.text
    content = content.replace("&nbsp;","")
#    print comment
    s1 = u'本帖最后由'
    s2 = u'编辑'
    pos1 = content.find(s1)
    pos2 = content.find(s2)
#    print pos1, pos2
    if pos1>=0 and pos2>0:
        content = content[pos2+2:]
    content = content.encode('utf-8')
    print content
    print 'Now, save results to database ...'
    store_bbs_post(url, author, title, content,
             BEIWEI_INFO_SOURCE_ID, keyword_id, created_at,read_count, comment_count)
    print 'results saved to database .... sleep 10 seconds .... '
    time.sleep(10)

def main():
    try:
        search_beiwei_for_posts()
    except Exception, e:
	print e
        bbs_logger.exception(e)

if __name__ == '__main__':
    print 'Start searching beiwei club ......'
    main()
