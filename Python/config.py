#! /usr/bin/env python
#coding=utf-8


import urllib
import urllib2
import httplib
import httplib2
import string
import time
import socket
import cookielib
import re
import math

from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta

from sqlalchemy.orm import mapper, sessionmaker
from datetime import datetime, timedelta
from sqlalchemy import *

from model import *

import socket 
socket.setdefaulttimeout(90)


MYSQL_ADDR = 'localhost:3306/soya-yc?charset=utf8'

MYSQL_USER = 'root'
#MYSQL_PASSWORD = '^12fg7'
MYSQL_PASSWORD = '123456'

mysql_connection = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@' + MYSQL_ADDR

engine = create_engine(mysql_connection,
                        encoding="utf-8", convert_unicode=True, echo=False)   
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


KEYWORDS = []
for row in session.query(Keyword).filter(Keyword.enable==True): 
    KEYWORDS.append(row)


PYTHON_DIR = '/home/lgy/git_code/soya/Python/'
