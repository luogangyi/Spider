#! /usr/bin/env python
#coding=utf-8

from config import *
from utils import baidu_date_str_to_datetime, wiki_logger, store_category, store_error

BAIDU_ZHIDAO_INFO_SOURCE_ID = 2


def search_for_baidu_zhidao_posts():
    previous_real_count = session.query(WikiPost).filter(WikiPost.info_source_id==BAIDU_ZHIDAO_INFO_SOURCE_ID).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = BAIDU_ZHIDAO_INFO_SOURCE_ID

    count = 0

    last_count = 0
    for keyword in KEYWORDS :
        data = {'word': keyword.str.encode('utf8'),
                'ie': 'utf-8',
                'sort': 1,
                'lm': 0,
                'date':2,
                'oa':0,
                'sites':-1,
               }
        
        url = "http://zhidao.baidu.com/search?" + urllib.urlencode(data)
        # print url

        headers = {
            'Host': 'zhidao.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
        }
    
        req = urllib2.Request(url, headers = headers)  
        response = urllib2.urlopen(req)  
        content = response.read() 
    
        soup = BeautifulSoup(content)


        posts = soup.findAll('dl', attrs={'class': "dl"})
        count = count + len(posts)

        #print count

        for post in posts:
            try:
                url = post.dt.a['href']
                comment_count = 0
                if post.find('a', attrs={'log': "pos:ans"}):
                    comment_count_str = post.find('a', attrs={'log': "pos:ans"}).text
                    tail = comment_count_str.find(u'个回答')
                    comment_count = int(comment_count_str[:tail])

                store_by_wiki_url(url, comment_count, keyword.id)
            except Exception, e:
                store_error(BAIDU_ZHIDAO_INFO_SOURCE_ID)
                wiki_logger.exception(e) 


        if count - last_count > 30:
            time.sleep(1800)
            last_count = count

    current_real_count = session.query(WikiPost).filter(WikiPost.info_source_id==BAIDU_ZHIDAO_INFO_SOURCE_ID).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()    


def store_by_wiki_url(url, comment_count, keyword_id):
    #print url
    sql_post = session.query(WikiPost).filter(WikiPost.url==url).first()
    if not sql_post:
       sql_post = WikiPost() 

    sql_post.url = url

    sql_post.keyword_id = keyword_id
    sql_post.info_source_id = BAIDU_ZHIDAO_INFO_SOURCE_ID

    headers = {
        'Host': 'zhidao.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
    }
    
    req = urllib2.Request(url, headers = headers)  
    response = urllib2.urlopen(req)  
    content = response.read()  

    soup = BeautifulSoup(content)

    title = soup.find('span', attrs={'class': "ask-title"})
    if title is None:
        wiki_logger.error("open baidu zhidao url: " + url + " error. can't find title")
        time.sleep(600)
        return

    sql_post.title = title.text 

    asker_soup = soup.find('div', attrs={'id': "ask-info"})
    asker = asker_soup.find('a', attrs={'class': "user-name"})
    if asker == None:
        sql_post.wiki_user_screen_name = u'匿名'
    else:
        sql_post.wiki_user_screen_name = asker.text
    

    address = url[25:]
    start = address.find('/')
    end = address.find('.html')
    idstr = address[start+1:end]
    read_count_url = "http://cp.zhidao.baidu.com/v.php?q=" + idstr + "&callback=bd__cbs__onzolk" 
    headers = {
        'Host': 'cp.zhidao.baidu.com',
        'Referer': 'http://zhidao.baidu.com/question/523194115.html',       
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
    }

    req = urllib2.Request(read_count_url, headers = headers)  
    response = urllib2.urlopen(req)  
    read_count = response.read()
    start = read_count.find("(")
    end = read_count.find(")")
    sql_post.read_count = int(read_count[start+1:end])


    ask_time = soup.find('span', attrs={'class': "grid-r ask-time"})
    sql_post.created_at = wiki_date_str_to_datetime(ask_time.text)


    content = soup.find('pre', attrs={'accuse': "qContent"})
    if content is None:
        sql_post.content = ""
    else:
        sql_post.content = content.renderContents()


    editor = soup.find('span', attrs={'class': "answer-title h2 grid"})
    if editor is None:
        sql_post.answered = False
    else:
        sql_post.answered = True

    sql_post.comment_count = comment_count

    session.merge(sql_post) #merge

    session.flush()
    session.commit()

    sql_post = session.query(WikiPost).filter(WikiPost.url==url).first()
    if sql_post:
        store_category('wiki', str(sql_post.id))

    time.sleep(10)


def do_login(username,password):
    cookie_jar = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17')]
    urllib2.install_opener(opener)

    # get cookie
    cookie_url = '''https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=false'''
    opener.open(cookie_url)

    # get token
    token_url = '''https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=false'''
    response = opener.open(token_url)

    for line in response.readlines():
        if line.find('login_token') > 0:
            start = line.find("='")
            end = line.find("';")
            token = line[start+2:end]

    post_data = urllib.urlencode({'username':username,
                                  'password':password,
                                  'token':token,
                                  'charset':'UTF-8',
                                  'callback':'parent.bd12Pass.api.login._postCallback',
                                  'index':'0',
                                  'isPhone':'false',
                                  'mem_pass':'on',
                                  'loginType':'1',
                                  'safeflg':'0',
                                  'staticpage':'https://passport.baidu.com/v2Jump.html',
                                  'tpl':'mn',
                                  'u':'http://www.baidu.com/',
                                  'verifycode':'',
                                })
    url = 'http://passport.baidu.com/v2/api/?login'

    headers = {"Accept": "image/gif, */*",
               "Referer": "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F",
               "Accept-Language": "zh-cn",
               "Content-Type": "application/x-www-form-urlencoded",
               "Accept-Encoding": "gzip, deflate",
               "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
               "Host": "passport.baidu.com",
               "Connection": "Keep-Alive",
               "Cache-Control": "no-cache"
              }

    req = urllib2.Request(url,post_data,headers=headers)
    opener.open(req)


def wiki_date_str_to_datetime(date_str):
    if date_str[0:2] == u'今天':
        date_str = datetime.today().strftime('%Y-%m-%d') + date_str[2:]

    return baidu_date_str_to_datetime(date_str)
        


def main():
    try:
        start_time = datetime.now()
        do_login('yoyo_worms', 'bI9eK4NF')
        search_for_baidu_zhidao_posts()
        end_time = datetime.now()
        consume_time = end_time - start_time
        wiki_logger.info("baidu zhidao consume time: " + str(consume_time))
    except Exception, e:
        store_error(BAIDU_ZHIDAO_INFO_SOURCE_ID)
        wiki_logger.exception(e) 


if __name__ == '__main__':
    main()
