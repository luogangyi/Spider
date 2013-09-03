#!/usr/bin/env python
#coding=utf8


from sqlalchemy.orm import relationship, backref
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'weibo_users'

    id = Column(Integer, primary_key=True)
    user_origin_id = Column(Unicode(20), nullable=False)
    info_source_id = Column(Integer, nullable=False)
    screen_name = Column(Unicode(32), nullable=False)
    profile_image_url = Column(Unicode(100), nullable=False)
    status_count = Column(Integer, nullable=False)
    follower_count = Column(Integer, nullable=False)
    following_count = Column(Integer, nullable=False)
    verified = Column(Boolean, nullable=False)
    gender = Column(Unicode(4), nullable=False)
    geo_info_city = Column(Unicode(32), nullable=True)
    geo_info_province = Column(Unicode(32), nullable=True)


    statuses = relationship('Status', backref='user')


class Status(Base):
    __tablename__ = 'weibo_statuses'

    id = Column(Integer, primary_key=True)
    url = Column(Unicode(100), nullable=False)
    weibo_origin_id = Column(Unicode(100), nullable=False)
    weibo_user_id = Column(Integer, ForeignKey('weibo_users.id'), nullable=False)
    weibo_user_screen_name = Column(Unicode(32), nullable=False)
    info_source_id = Column(Integer, nullable=False)
    keyword_id = Column(Integer, nullable=False)
    repost_count = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=False)
    retweeted = Column(Boolean, nullable=False)
    retweeted_status_id = Column(Unicode(32), nullable=True)
    with_picture = Column(Boolean, nullable=False)
    pic_address = Column(Unicode(100), nullable=True)
    geo_info_city = Column(Unicode(32), nullable=True)
    geo_info_province = Column(Unicode(32), nullable=True)
    text = Column(Unicode(300), nullable=False)
    created_at = Column(DateTime, nullable=False)

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    info_source_id = Column(Integer, nullable=False)
    fetched_info_count = Column(Integer, nullable=False)
    real_fetched_info_count = Column(Integer, nullable=False)
    previous_executed = Column(DateTime, nullable=False)


class JobError(Base):
    __tablename__ = 'job_errors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    info_source_id = Column(Integer, nullable=False)
    happened_at = Column(DateTime, nullable=False)


class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True, autoincrement=True)
    str = Column(Unicode(32), nullable=False)
    enable = Column(Boolean, nullable=False)


class WikiPost(Base):
    __tablename__ = 'wiki_posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Unicode(100), nullable=False)
    wiki_user_screen_name = Column(Unicode(32), nullable=False)
    keyword_id = Column(Integer, nullable=False)
    info_source_id = Column(Integer, nullable=False)
    title = Column(Unicode(100), nullable=False)
    content = Column(Unicode(300), nullable=False)
    created_at = Column(DateTime, nullable=False)
    read_count = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=False)
    answered = Column(Boolean, nullable=False)



class VideoPost(Base):
    __tablename__ = 'video_posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Unicode(100), nullable=False)
    video_user_screen_name = Column(Unicode(32), nullable=False)
    source_name = Column(Unicode(32), nullable=False)
    keyword_id = Column(Integer, nullable=False)
    info_source_id = Column(Integer, nullable=False)
    title = Column(Unicode(100), nullable=False)
    created_at = Column(DateTime, nullable=False)
    watch_count = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=False)
    up_count = Column(Integer, nullable=False)
    down_count = Column(Integer, nullable=False)
    repost_count = Column(Integer, nullable=False)


class BBSPost(Base):
    __tablename__ = 'bbs_posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Unicode(200), nullable=False)
    bbs_user_screen_name = Column(Unicode(32), nullable=False)
    info_source_id = Column(Integer, nullable=False)
    keyword_id = Column(Integer, nullable=False)
    title = Column(Unicode(100), nullable=False)
    content = Column(Unicode(2000), nullable=False)
    created_at = Column(DateTime, nullable=False)
    read_count = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=False)


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Unicode(200), nullable=False)
    source_name = Column(Unicode(32), nullable=False)
    info_source_id = Column(Integer, nullable=False)
    keyword_id = Column(Integer, nullable=False)
    title = Column(Unicode(100), nullable=False)
    content = Column(Unicode(1000), nullable=False)
    created_at = Column(DateTime, nullable=False)


class BlogPost(Base):
    __tablename__ = 'blog_posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Unicode(200), nullable=False)
    blog_user_screen_name = Column(Unicode(32), nullable=False)
    info_source_id = Column(Integer, nullable=False)
    keyword_id = Column(Integer, nullable=False)
    title = Column(Unicode(100), nullable=False)
    content = Column(Unicode(2000), nullable=False)
    created_at = Column(DateTime, nullable=False)
    read_count = Column(Integer, nullable=False)
    comment_count = Column(Integer, nullable=False)


class OpponentKeyword(Base):
    __tablename__ = 'opponent_keywords'
    id = Column(Integer, primary_key=True, autoincrement=True)
    str = Column(Unicode(32), nullable=False)


class OpponentNews(Base):
    __tablename__ = 'opponent_news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Unicode(200), nullable=False)
    source_name = Column(Unicode(32), nullable=False)
    info_source_id = Column(Integer, nullable=False)
    opponent_keyword_id = Column(Integer, nullable=False)
    title = Column(Unicode(100), nullable=False)
    content = Column(Unicode(1000), nullable=False)
    created_at = Column(DateTime, nullable=False)


class HotUser(Base):
    __tablename__ = 'weibo_hot_user_pool'
    id = Column(Integer, primary_key=True)


class MonitoringStatus(Base):
    __tablename__ = 'monitoring_weibo_statuses'

    id = Column(Integer, primary_key=True)
    weibo_status_id = Column(Integer, ForeignKey('weibo_statuses.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    expiring_at = Column(DateTime, nullable=False)

    


# Single weibo analyse

class SingleSourceStatus(Base):
    __tablename__ = 'single_source_statuses'

    id = Column(Integer, primary_key=True)
    url = Column(Unicode(100), nullable=False)
    origin_id = Column(Unicode(100), nullable=False)
    reposts_count = Column(Integer, nullable=False)
    comments_count = Column(Integer, nullable=False)
    attitudes_count = Column(Integer, nullable=False)
    text = Column(Unicode(300), nullable=False)
    source_app = Column(Unicode(300), nullable=False)
    pic = Column(Unicode(100), nullable=True)
    single_weibo_user_id= Column(Integer, ForeignKey('single_weibo_users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)

    single_repost_statuses = relationship('SingleRepostStatus', backref='single_source_status')
    single_comments = relationship('SingleComment', backref='single_source_status')
    

class SingleRepostStatus(Base):
    __tablename__ = 'single_repost_statuses'

    id = Column(Integer, primary_key=True)
    single_source_status_id = Column(Integer, ForeignKey('single_source_statuses.id'), nullable=False)
    url = Column(Unicode(100), nullable=False)
    origin_id = Column(Unicode(100), nullable=False)
    reposts_count = Column(Integer, nullable=False)
    comments_count = Column(Integer, nullable=False)
    attitudes_count = Column(Integer, nullable=False)
    text = Column(Unicode(300), nullable=False)
    source_app = Column(Unicode(300), nullable=False)
    pic = Column(Unicode(100), nullable=True)
    single_weibo_user_id= Column(Integer, ForeignKey('single_weibo_users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    repost_depth = Column(Integer, nullable=False)
    direct_reposts_count = Column(Integer, nullable=False)
    parent_origin_id = Column(Unicode(100), nullable=True)



class SingleComment(Base):
    __tablename__ = 'single_comments'

    id = Column(Integer, primary_key=True)
    single_source_status_id = Column(Integer, ForeignKey('single_source_statuses.id'), nullable=False)
    origin_id = Column(Unicode(100), nullable=False)
    text = Column(Unicode(300), nullable=False)
    source_app = Column(Unicode(300), nullable=False)
    single_weibo_user_id= Column(Integer, ForeignKey('single_weibo_users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)




class SingleWeiboUser(Base):
    __tablename__ = 'single_weibo_users'

    id = Column(Integer, primary_key=True)
    origin_id = Column(Unicode(20), nullable=False)
    screen_name = Column(Unicode(32), nullable=False)
    followers_count = Column(Integer, nullable=False)
    friends_count = Column(Integer, nullable=False)
    bi_followers_count = Column(Integer, nullable=False)
    description = Column(Unicode(100), nullable=False)
    profile_image_url = Column(Unicode(100), nullable=False)
    city = Column(Unicode(32), nullable=True)
    province = Column(Unicode(32), nullable=True)
    gender = Column(Unicode(4), nullable=False)
    created_at = Column(DateTime, nullable=False)
    statuses_count = Column(Integer, nullable=False)
    verified_type = Column(Unicode(32), nullable=False)

    single_repost_statuses = relationship('SingleRepostStatus', backref='single_weibo_user')
    single_source_statuses = relationship('SingleSourceStatus', backref='single_weibo_user')
    single_comments = relationship('SingleComment', backref='single_weibo_user')



