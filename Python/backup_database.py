#! /usr/bin/env python
#coding=utf-8


import os
import sys
from datetime import *
import time


backup_path = '/home/tbs/database_bac/'

def validate_backup_path():
    if os.path.exists(backup_path) == False:
        print "I create a directory here: %s " % backup_path
        os.mkdir(backup_path)

def backup_databases():
    filename = "soya_%s.sql" % (datetime.utcfromtimestamp(time.time()))
    print "Backup %s" % (filename)
    os.system("mysqldump -umysql -p^12fg7 soya > '%s%s'" % (backup_path, filename))

def main():
    validate_backup_path()
    backup_databases()
    print "finish!!!"


if __name__ == '__main__':
    main()
