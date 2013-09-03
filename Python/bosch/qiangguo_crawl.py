#!/usr/bin/python
#-*-coding:utf-8-*-

from config import *
from bbs_utils import *
from utils import baidu_date_str_to_datetime, bbs_logger

QIANGGUO_INFO_SOURCE_ID = 22

def search_qiangguo_for_posts():
    previous_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==QIANGGUO_INFO_SOURCE_ID).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = QIANGGUO_INFO_SOURCE_ID

    for keyword in KEYWORDS:
#	print keyword.str
#        print keyword.str.encode('utf-8')
#	kw = keyword.str.encode('gbk')
        kw = keyword.str.encode('utf-8') # keyword 可以为中文
	kw = kw.strip()
	kw = kw.replace(" ",'+')
        print kw
        url = 'http://bbs.people.com.cn/quickSearch.do?threadtype=1&field=title&op=in&content='
        url += kw + '&mysrc.x=42&mysrc.y=8'
        print url
        headers = {'Host':'bbs.people.com.cn',
                   'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0'}
        req = urllib2.Request(url,headers = headers)
	print 'search: req = Request ...'
        response = urllib2.urlopen(req)
	print 'search: response ...'
        content = response.read()
	print 'search: content'
#       print content
        soup = BeautifulSoup(content,fromEncoding='gbk')
        posts = soup.findAll('td', attrs={'class':'f14'})
        count += len(posts)
        for post in posts:
	    print post.a['href']
            store_by_bbs_url(post.a['href'], keyword.id)
	time.sleep(5)
            
    current_real_count = session.query(BBSPost).filter(BBSPost.info_source_id==QIANGGUO_INFO_SOURCE_ID).count()

    sql_job.fetched_into_count = count
    sql_job.real_fetched_into_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()
    
def store_by_bbs_url(url,keyword_id):
    print 'store_by_bbs_url,,,, program begins ..'
    headers = {'Host':'bbs1.people.com.cn',
               'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:22.0) Gecko/20100101 Firefox/22.0'}
    req = urllib2.Request(url,headers = headers)
    print 'store_by_bbs_url line 3'
    response = urllib2.urlopen(req)
    content = response.read()
    print 'reading content'
    soup = BeautifulSoup(content,fromEncoding='gbk')
    # title
    title = soup.title.text
#    print title
    title =  title.encode('utf-8')
    print title
    # author
    t = soup.find('p', attrs={'class':'red'})
    author = t.text
    author = author.encode('utf-8')
    print author
    # created_at
    t = soup.find('div', attrs={'class':'posts_tools clearfix'})
    s = t.text
    s = s.replace('&nbsp;',"")
    s = s.strip()
    created_at = s[3:]   
    created_at = created_at.encode('utf-8')
    print created_at
    # read_count, comment_count
    t = soup.find('strong', attrs={'style':'text-align:right;'})
    s = t.text
    s = s.replace('&nbsp;',"")
    pos1 = s.find(u'人气')
    comment_count = s[3:pos1]
    read_count = s[pos1+3:]
    comment_count = comment_count.encode('utf-8')
    read_count = read_count.encode('utf-8')
    print comment_count, read_count
    # content
    content = ""
    t = soup.find('div', attrs={'class':'posts_content clearfix BSHARE_POP'})
    s = str(t)
    if s.find('content_path')>-1:
        url = t['content_path']
        print url
#    url = 'http://bbs1.people.com.cn/posts/06/CE/2F/1F/content_html.txt'
        req = urllib2.Request(url,headers = headers)
        print 'get content: url ...'
        response = urllib2.urlopen(req)
        print 'get content: response ...'
        text = response.read()
#        print text
        print 'get content: text ...'
        s = str(text)
	pos1 = s.find('<')
	pos2 = s.find('>')
	while(pos1>-1 and pos2>-1):
	    s1 = s[pos1:pos2+1]
	    s = s.replace(s1,"")
	    pos1 = s.find('<')
	    pos2 = s.find('>')
	content = s
#        soup = BeautifulSoup(text,fromEncoding='utf-8')
#        print 'get content: building soup ...'
#        ts = soup.findAll('p')
#        content = ""
#        for t in ts:
#            content += t.text
        print 'get content: building content'
#	content = content.decode('gbk')
#        content = content.encode('utf-8')
        print 'building utf-8 content ...'
        print content
    store_bbs_post(url, author, title, content,
            QIANGGUO_INFO_SOURCE_ID, keyword_id, created_at,read_count, comment_count)
    time.sleep(10)


def main():
    try:
        search_qiangguo_for_posts()
    except Exception, e:
	print e
        bbs_logger.exception(e)

if __name__ == '__main__':
    print 'Start searching qiangguo club ...'
    main()
    
