#!/usr/bin/python
#-*-coding:utf-8-*-

from config import *
from bbs_utils import *
from utils import baidu_date_str_to_datetime, bbs_logger
#from CharacterToGbk import getGBKCode

YUCHENG_INFO_SOURCE_ID = 24
def search_yucheng_for_posts():
    previous_real_count = session.query(BBSPost).filter(Job.info_source_id==YUCHENG_INFO_SOURCE_ID).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = YUCHENG_INFO_SOURCE_ID

    for keyword in KEYWORDS:
        url = 'http://bbs.yaanren.net/search.php?mod=portal'
        headers = {'Host':'bbs.yaanren.net',
                   'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0'}
	print keyword.str.encode('utf-8')
#        kw = getGBKCode(keyword.str)
#        print keyword.str.encode('utf-8')
        kw = keyword.str.encode('gbk')
	data = {'formhash':'759e5b39',
		'srchtxt':kw,
		'searchsubmit':'yes'}
        postdata = urllib.urlencode(data)
        req = urllib2.Request(url,data = postdata,headers = headers)

        response = urllib2.urlopen(req)
        content = response.read()
#	print content
        soup = BeautifulSoup(content,fromEncoding='gbk')
        posts = soup.findAll('h3')
        count += len(posts)
	print len(posts)
        for post in posts:
            print post.a['href']
            store_by_bbs_url(post.a['href'], keyword.id)
	time.sleep(5)

    current_real_count = session.query(BBSPost).filter(Job.info_source_id==YUCHENG_INFO_SOURCE_ID).count()

    sql_job.fetched_into_count = count
    sql_job.real_fetched_into_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()

        
def store_by_bbs_url(url, keyword_id):
    headers = {'Host':'bbs.yaanren.net',
               'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0'}
    req = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    soup = BeautifulSoup(content,fromEncoding='gbk')
    # title
    t = soup.find('title')
    title = t.text
    title = title.encode('utf-8')
    # author
    t = soup.find('div', attrs={'class':'authi'})
    author = t.text
    author = author.encode('utf-8')
    # created_at
#    t = soup.findAll('em',attrs={'id':re.compile("authorposton$")})
    t = soup.findAll(text=re.compile(u'发表于'))
    # parse t[0]
    s = t[0]
    pos1 = s.find(" ")
    s = s[pos1:]
    created_at = s.strip()
    created_at = created_at.encode('utf-8')
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
    cotent = t.text
    content = content.replace("&nbsp;","")
#    print comment
    s1 = u'本帖最后由'
    s2 = u'编辑'
    pos1 = content.find(s1)
    pos2 = content.find(s2)
    print pos1, pos2
    if pos1>=0 and pos2>0:
        content = content[pos2+2:]
    content = content.encode('utf-8')
    store_bbs_post(url, author, title, content,
            YUCHENG_INFO_SOURCE_ID, keyword_id, created_at,read_count, comment_count)
    time.sleep(10)

def main():
    try:
        search_yucheng_for_posts()
    except Exception, e:
        print e
        bbs_logger.exception(e)

if __name__ == '__main__':
    print 'Starting searching yucheng club ....'
    main()
