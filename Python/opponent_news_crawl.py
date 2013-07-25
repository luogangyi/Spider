#! /usr/bin/env python
#coding=utf-8

from config import *
from utils import store_category, news_logger, baidu_date_str_to_datetime



def search_for_baidu_news_posts():
    last_time = session.query(Job).filter(Job.info_source_id==OPPONENT_BAIDU_NEWS_INFO_SOURCE_ID).order_by(Job.id.desc()).first().previous_executed    

    previous_real_count = session.query(OpponentNews).count()
    count = 0
    sql_job = Job()
    sql_job.previous_executed = datetime.now()
    sql_job.info_source_id = OPPONENT_BAIDU_NEWS_INFO_SOURCE_ID


    for keyword in OPPONENT_KEYWORDS :
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

                if created_at < last_time:
                    finished = True
                    break

                if title.find(keyword.str)>0:
                    add_news_to_session(url, source_name, title, content,
                                    OPPONENT_BAIDU_NEWS_INFO_SOURCE_ID, created_at, keyword.id)


            time.sleep(5)
            page = page + 20

        
    current_real_count = session.query(OpponentNews).count()
    sql_job.fetched_info_count = count
    sql_job.real_fetched_info_count = current_real_count - previous_real_count

    session.add(sql_job)
    session.flush()
    session.commit()






