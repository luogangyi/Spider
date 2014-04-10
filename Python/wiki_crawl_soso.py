#! /usr/bin/env python
#coding=utf-8
# update by lgy,2013.9.12

from config import *
from utils import baidu_date_str_to_datetime, wiki_logger, store_category, store_error,recheck_title
from newspider import baidu

SOSO_WENWEN_INFO_SOURCE_ID = 13


def search_for_soso_wenwen_posts():
    previous_real_count = session.query(WikiPost).filter(WikiPost.info_source_id==SOSO_WENWEN_INFO_SOURCE_ID).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = SOSO_WENWEN_INFO_SOURCE_ID

    count = 0
    cookie_jar = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    opener.addheaders = [('User-Agent','Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36'),
                         ('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
                         ('Accept-Language','zh-CN,zh;q=0.8'),
                         ('Connection','keep-alive'),
                         ('Host', 'wenwen.sogou.com'),
                         ]
    urllib2.install_opener(opener)

    # get cookie
    cookie_url = '''http://wenwen.sogou.com/'''

    response = opener.open(cookie_url) 
    #print cookie_jar


    # content = response.read() 
    # soup = BeautifulSoup(content)
    # search_url = soup.find('input',attrs={'name': "url_search"})['value']
    # print search_url
    # icfa,sid,g_ut = getPara(search_url)

    # print icfa,sid,g_ut

    for keyword in KEYWORDS :
        print keyword.str
        data = {
                'sp':'S'+keyword.str.encode('utf8'),
                'ch':'w.search.sb',
                'w':keyword.str.encode('utf8'),
                'search':'搜索答案'
                #'pid':'w.search.sjsx'
               }

        newCookie = cookielib.Cookie(version = 0,name='ww_search_tips',value='nulln',port=None,port_specified=False, domain='wenwen.sogou.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        cookie_jar.set_cookie(newCookie)
        newCookie = cookielib.Cookie(version = 0,name='ww_sTitle',value=keyword.str.encode('utf8'),port=None,port_specified=False, domain='wenwen.sogou.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        cookie_jar.set_cookie(newCookie)
        print cookie_jar
        url = "http://wenwen.sogou.com/s/?" + urllib.urlencode(data)
        print url

        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            #'Accept-Encoding':'gzip,deflate,sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Host': 'wenwen.sogou.com',
            'Referer':'http://wenwen.sogou.com/',
            'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36'
            #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
        }
    
        req = urllib2.Request(url, headers = headers)  
        response = opener.open(req)  
        content = response.read() 
    
        soup = BeautifulSoup(content)
        print soup.prettify()

        result_list_soup = soup.find('ol', attrs={'class': "result_list"})
        if result_list_soup == None:
            time.sleep(5)
            continue

        posts = result_list_soup.findAll('li')
        count = count + len(posts)

        for post in posts:
            origin_url = post.a['href']
            #tail = origin_url.find('?w=')
            #url = 'http://wenwen.soso.com' + origin_url[:tail]
            url = origin_url
            comment_count_str = post.find('div', attrs={'class':
                                          "info"}).strip()
            tail = comment_count_str.find(u'个回答')
            # print comment_count_str
            comment_count = int(comment_count_str[:tail])

            if st == 1:
                answered = False
            else:
                answered = True

            print url, comment_count, answered, keyword.id,keyword
            store_by_wiki_url(url, comment_count, answered, keyword.id,keyword)

            
        time.sleep(5)



    current_real_count = session.query(WikiPost).filter(WikiPost.info_source_id==SOSO_WENWEN_INFO_SOURCE_ID).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()    


def store_by_wiki_url(url, comment_count, answered, keyword_id,keyword):
    sql_post = session.query(WikiPost).filter(WikiPost.url==url).first()
    if not sql_post:
       sql_post = WikiPost() 

    sql_post.url = url

    sql_post.keyword_id = keyword_id
    sql_post.info_source_id = SOSO_WENWEN_INFO_SOURCE_ID
    sql_post.comment_count = comment_count
    sql_post.answered = answered

    headers = {
        'Host': 'wenwen.soso.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
    }
    
    req = urllib2.Request(url, headers = headers)  
    response = urllib2.urlopen(req)  
    content = response.read() 
    
    soup = BeautifulSoup(content)
    
    wiki_user_screen_name = soup.find('a', attrs={'class':"user_name"})
    if wiki_user_screen_name == None:
        wiki_user_screen_name = u'匿名'
    else:
        wiki_user_screen_name = wiki_user_screen_name.text
    try:
        date_str = soup.find('span', attrs={'class':"question_time"}).text
        created_at = baidu_date_str_to_datetime(date_str)
    except:
        created_at = datetime.now()
    try:
        title = soup.find('h3', attrs={'id':"questionTitle"}).text
    except:
        time.sleep(5)
        return

    content_div = soup.find('div', attrs={'class':"question_con"})
    if content_div is None:
        content = ""
    else:
        content = content_div.text

    #print "before",title,created_at
    if not recheck_title(keyword, title):
        time.sleep(5)
        return

    sql_post.read_count = 0
    sql_post.wiki_user_screen_name = wiki_user_screen_name
    sql_post.title = title
    sql_post.content = content
    sql_post.created_at = created_at

    #print "after",title,created_at

    session.merge(sql_post) #merge

    session.flush()
    session.commit()

    sql_post = session.query(WikiPost).filter(WikiPost.url==url).first()
    if sql_post:
        #print "stored"
        store_category('wiki', str(sql_post.id))

    time.sleep(5)
    
def getPara(search_url):
    pattern = re.compile(r"icfa=(\w+)&sid=(\w+)&g_ut=(\d+)")

    m = pattern.search(search_url)
    return m.group(1),m.group(2),m.group(3)


def main():
    try:
        start_time = datetime.now()
        obj = baidu.Baidu(id,'scwx.newssc.org','news','四川外宣网')
        obj.main()
        # search_for_soso_wenwen_posts()
        end_time = datetime.now()
        consume_time = end_time - start_time
        wiki_logger.info("soso wenwen consume time: " + str(consume_time))
    except Exception, e:
        store_error(SOSO_WENWEN_INFO_SOURCE_ID)
        wiki_logger.exception(e) 


if __name__ == '__main__':
    main()
