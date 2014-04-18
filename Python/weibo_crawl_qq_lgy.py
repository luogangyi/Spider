#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  FileName    : example-user.py
#  Author      : Feather.et.ELF <andelf@gmail.com>
#  Created     : Fri Apr 08 16:53:09 2011 by Feather.et.ELF
#  Copyright   : andelf <andelf@gmail.com> (c) 2011
#  Description : example to show how to use user api
#  Time-stamp: <2011-06-04 11:39:06 andelf>


import sys
sys.path.insert(0, "..")
import webbrowser

from qqweibo import API
from qqweibo import OAuth2_0_Handler as AuthHandler


API_KEY = '801322882'
API_SECRET = '0f4b0f472813b31c23720623014e22e9'

if API_KEY.startswith('your'):
    print ('You must fill API_KEY and API_SECRET!')
    webbrowser.open("http://open.t.qq.com/apps_index.php")
    raise RuntimeError('You must set API_KEY and API_SECRET')

CALLBACK_URL = 'http://fledna.duapp.com/query'

auth = AuthHandler(API_KEY, API_SECRET, CALLBACK_URL)


#token = 'e9fc735b76ba4e75a6ebaefe61ee66fc'
token = 'd169abff38d747cfa8bdb21123577482'
#tokenSecret = 'ec07bda1b332156d1554470893b16b6d'
tokenSecret = '25d60b4c67c488a4d5291dcb9bd43fd8'

auth.setToken(token, tokenSecret)

# this time we use ModelParser()
api = API(auth)  # ModelParser is the default option


"""
Avaliable API:
Do to refer api.doc.rst
api.user.info
api.user.otherinfo
api.user.update
api.user.updatehead
api.user.userinfo
"""

me = api.user.info()

print (("Name: {0.name}\nNick: {0.nick}\nLocation {0.location}\n"
        "Email: {0.email}\nIntro: {0.introduction}").format(me))

print (me.self)                           # is this user myself?

me.introduction = 'modify from pyqqweibo!!!'
me.update()                             # update infomation

me = api.user.info()
print (me.introduction)

api.user.updatehead('/path/to/your/head/img.fmt')

ret = api.user.otherinfo('NBA')

print (ret.verifyinfo)

for t in ret.timeline(reqnum=3):
    print (t.text)