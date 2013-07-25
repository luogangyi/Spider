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
    weibo_origin_id = Column(Integer, nullable=False)
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


class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True, autoincrement=True)
    str = Column(Unicode(32), nullable=False)


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

class InfoSource(Base):
    __tablename__ = 'info_sources'
    id = Column(Integer, primary_key=True, autoincrement=True)
    str = Column(Unicode(32), nullable=False)
    period = Column(Integer, nullable=False)
    info_source_type_id = Column(Integer, nullable=False)
    user_url = Column(Unicode(64), nullable=False)

"""
class HotUser(Base):
    __tablename__ = 'dosa_weibo_hot_user_pool'
    id = Column(Integer, primary_key=True)


class MonitoringStatus(Base):
    __tablename__ = 'dosa_weibo_monitoring_status'

    id = Column(Integer, primary_key=True)
    weibo_status_id = Column(Integer, ForeignKey('dosa_weibo_status.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    expiring_at = Column(DateTime, nullable=False)

    




class VideoPost(Base):
    __tablename__ = 'dosa_video_post'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Unicode(100), nullable=False)
    video_user_screen_name = Column(Unicode(32), nullable=False)
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
    __tablename__ = 'dosa_bbs_post'

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
    __tablename__ = 'dosa_news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Unicode(200), nullable=False)
    source_name = Column(Unicode(32), nullable=False)
    info_source_id = Column(Integer, nullable=False)
    keyword_id = Column(Integer, nullable=False)
    title = Column(Unicode(100), nullable=False)
    content = Column(Unicode(1000), nullable=False)
    created_at = Column(DateTime, nullable=False)


class BlogPost(Base):
    __tablename__ = 'dosa_blog_post'

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
    __tablename__ = 'dosa_opponent_keyword'
    id = Column(Integer, primary_key=True, autoincrement=True)
    str = Column(Unicode(32), nullable=False)


class OpponentNews(Base):
    __tablename__ = 'dosa_opponent_news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(Unicode(200), nullable=False)
    source_name = Column(Unicode(32), nullable=False)
    info_source_id = Column(Integer, nullable=False)
    opponent_keyword_id = Column(Integer, nullable=False)
    title = Column(Unicode(100), nullable=False)
    content = Column(Unicode(1000), nullable=False)
    created_at = Column(DateTime, nullable=False)
"""