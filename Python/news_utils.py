#! /usr/bin/env python
#coding=utf-8
# modified at 2013.7.23

from config import *
from utils import store_category, recheck_title, baidu_date_str_to_datetime

BAIDU_NEWS_INFO_SOURCE_ID = 10
GOOGLE_NEWS_INFO_SOURCE_ID = 11


OPPONENT_BAIDU_NEWS_INFO_SOURCE_ID = 15
OPPONENT_GOOGLE_NEWS_INFO_SOURCE_ID = 16


OPPONENT_KEYWORDS = []
for row in session.query(OpponentKeyword): 
    OPPONENT_KEYWORDS.append(row)


def add_news_to_session(url, source_name, title, content, info_source_id, created_at, keyword):
    sql_news = session.query(News).filter(News.url==url,
                         News.info_source_id==info_source_id).first()
    if not sql_news:
        sql_news = News()
    else:
        return

    sql_news.url = url
    sql_news.source_name = source_name
    sql_news.title = title
    sql_news.content = content
    sql_news.info_source_id = info_source_id 
    sql_news.keyword_id = keyword.id
    sql_news.created_at = created_at

    session.merge(sql_news)

    session.flush()
    session.commit()


    sql_news = session.query(News).filter(News.url==url,
                         News.info_source_id==info_source_id).first()
    if sql_news:
        store_category('news', str(sql_news.id))



def add_opponent_news_to_session(url, source_name, title, content, info_source_id, created_at, keyword):
    if not recheck_title(keyword, title): # 过滤标题关键字
        return

    sql_news = session.query(OpponentNews).filter(OpponentNews.url==url).first()
    if not sql_news:
        sql_news = OpponentNews()
    else:
        return

    sql_news.url = url
    sql_news.source_name = source_name
    sql_news.title = title
    sql_news.content = content
    sql_news.info_source_id = info_source_id 
    sql_news.opponent_keyword_id = keyword.id
    sql_news.created_at = created_at

    session.merge(sql_news) #merge

    session.flush()
    session.commit()


def google_date_str_to_datetime(date_str):
    if date_str[-3:] == u'分钟前':
        num = int(date_str.split()[0])
        return datetime.now() - timedelta(minutes=num)
    elif date_str[-3:] == u'小时前':
        num = int(date_str.split()[0])
        return datetime.now() - timedelta(hours=num)
    else:
        return datetime(*(time.strptime(date_str, u'%Y年%m月%d日')[0:6]))
  


def search_for_google_news_posts(using_keywords, info_source_id):
    last_time = session.query(Job).filter(Job.info_source_id==info_source_id).order_by(Job.id.desc()).first().previous_executed    

    previous_real_count = session.query(OpponentNews).count()


    if info_source_id == GOOGLE_NEWS_INFO_SOURCE_ID:
        previous_real_count = session.query(News).filter(News.info_source_id==info_source_id).count()
    else:
        previous_real_count = session.query(OpponentNews).filter(OpponentNews.info_source_id==info_source_id).count()

    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = info_source_id


    cookie_jar = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17')]
    urllib2.install_opener(opener)

    # get cookie
    cookie_url = '''http://www.google.com.hk?hl=zh-CN'''
    opener.open(cookie_url)

    for keyword in using_keywords :
        page = 0
        finished = False
        while(not finished):
            data = {'q': keyword.str.encode('utf8'),
                    'tbm': 'nws',
                    'hl': 'zh-CN',
                    'start': page
                   }
            
            url = "http://www.google.com.hk/search?tbs=sbd:1&" + urllib.urlencode(data)

            headers = {
                'Host': 'www.google.com.hk',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'
            }
    
            req = urllib2.Request(url, headers = headers)  
            response = opener.open(req)
            content = response.read() 
    
            soup = BeautifulSoup(content)

            news_tables = soup.findAll('td', attrs={'class': 'tsw'})
            count = count + len(news_tables)
            if len(news_tables) == 0:
                break

            for news_table in news_tables:
                url = news_table.a['href']
                title = news_table.a.text
                source_name = news_table.find('span', attrs={'class': 'news-source'}).text
                date_str = news_table.find('span', attrs={'class': 'f nsa'}).text
                created_at = google_date_str_to_datetime(date_str)
                content = news_table.find('div', attrs={'class': 'st'}).text

                if created_at < last_time:
                    finished = True
                    break

                if info_source_id == GOOGLE_NEWS_INFO_SOURCE_ID:
                    add_news_to_session(url, source_name, title, content,
                                    info_source_id, created_at, keyword)
                else:
                    add_opponent_news_to_session(url, source_name, title, content,
                                    info_source_id, created_at, keyword)

            if len(news_tables) < 10:
                break

            time.sleep(60)
            page = page + 10

    
    if info_source_id == GOOGLE_NEWS_INFO_SOURCE_ID:
        current_real_count = session.query(News).filter(News.info_source_id==info_source_id).count()
    else:
        current_real_count = session.query(OpponentNews).filter(OpponentNews.info_source_id==info_source_id).count()
    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()





def search_for_baidu_news_posts(using_keywords, info_source_id):
    last_time = session.query(Job).filter(Job.info_source_id==info_source_id).order_by(Job.id.desc()).first().previous_executed    

    if info_source_id == BAIDU_NEWS_INFO_SOURCE_ID:
        previous_real_count = session.query(News).filter(News.info_source_id==info_source_id).count()
    else:
        previous_real_count = session.query(OpponentNews).filter(OpponentNews.info_source_id==info_source_id).count()

    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = info_source_id


    for keyword in using_keywords :
        page = 0
        finished = False
        while(not finished):
            data = {'word': keyword.str.encode('gb2312'),
                    'tn': 'news',
                    'ie': 'gb2312',
                    'sr': 0,
                    'cl': 2,
                    'rn': 20,
                    'ct': 0,
                    'clk': 'sortbytime',
                    'pn': page
                   }
            
            url = "http://news.baidu.com/ns?" + urllib.urlencode(data)

            headers = {
                'Host': 'news.baidu.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'
            }
    
            req = urllib2.Request(url, headers = headers)  
            response = urllib2.urlopen(req)  
            content = response.read() 
    
            soup = BeautifulSoup(content, fromEncoding="gbk")
            
            news_tables = soup.findAll('table', attrs={'cellspacing': '0', 'cellpadding':
                                                   '2'})
            count = count + len(news_tables)

            if len(news_tables) == 0:
                break

            for news_table in news_tables:
                url = news_table.tr.td.a['href']
                title = news_table.tr.td.a.text
                source_and_date = news_table.find('font', attrs={'color':
                                                                 '#666666'}).text.split()
                content = news_table.find('font', attrs={'size': '-1'}).text

                source_name = source_and_date[0]
                if len(source_and_date) == 3:
                    date = source_and_date[1] + ' ' + source_and_date[2]
                else:
                    continue

                created_at = baidu_date_str_to_datetime(date)
                
                # 新闻展开
                morelink_a = news_table.find('a',attrs={'class':'more_link'})
                if morelink_a != None:
                    url = 'http://news.baidu.com'+morelink_a['href']
                    #print morelink_a['href']+morelink_a.text
                    count = inner_search_for_baidu_news_posts(url,count,last_time,keyword,info_source_id)
                    # 展开新闻，则在本次循环中不保存
                    continue

                if info_source_id == BAIDU_NEWS_INFO_SOURCE_ID:
                    add_news_to_session(url, source_name, title, content,
                                        info_source_id, created_at, keyword)
                else:
                    add_opponent_news_to_session(url, source_name, title, content,
                                        info_source_id, created_at, keyword)


            time.sleep(5)
            page = page + 20

        
    if info_source_id == BAIDU_NEWS_INFO_SOURCE_ID:
        current_real_count = session.query(News).filter(News.info_source_id==info_source_id).count()
    else:
        current_real_count = session.query(OpponentNews).filter(OpponentNews.info_source_id==info_source_id).count()

    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()


#根据url，递归搜索信息
def inner_search_for_baidu_news_posts(inner_url,count,last_time,keyword,info_source_id):
    finished = False
    next_url = inner_url
    while(not finished):
        
        #print next_url

        headers = {
            'Host': 'news.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17'
        }

        req = urllib2.Request(next_url, headers = headers)  
        response = urllib2.urlopen(req)  
        content = response.read() 

        soup = BeautifulSoup(content, fromEncoding="gbk")

        news_tables = soup.findAll('table', attrs={'cellspacing': '0', 'cellpadding':
                                               '2'})
        count = count + len(news_tables)

        if len(news_tables) == 0:
            break

        for news_table in news_tables:
            url = news_table.tr.td.a['href']
            title = news_table.tr.td.a.text
            source_and_date = news_table.find('font', attrs={'color':
                                                             '#666666'}).text.split()
            content = news_table.find('font', attrs={'size': '-1'}).text

            source_name = source_and_date[0]

            if len(source_and_date) == 3:
                date = source_and_date[1] + ' ' + source_and_date[2]
            else:
                continue

            created_at = baidu_date_str_to_datetime(date)

            if info_source_id == BAIDU_NEWS_INFO_SOURCE_ID:
                add_news_to_session(url, source_name, title, content,
                                    info_source_id, created_at, keyword)
            else:
                add_opponent_news_to_session(url, source_name, title, content,
                                    info_source_id, created_at, keyword)


        time.sleep(5)
        page_nav = soup.find('div',attrs={'class':'page-nav'})

        # 没有下一页，则结束
        if page_nav == None:
            #print 'no page nav'
            finished = True
            break
        next_url_a = page_nav.find('a',attrs={'class':'next'})
        if next_url_a == None:
            #print page_nav.prettify()
            finished = True
            break
        else:
            next_url = 'http://news.baidu.com' + next_url_a['href'] 

    return count
