#! /usr/bin/env python
#coding=utf-8

import time

RUNLIST=['bbs_dz19','bbs_cqkx','bbs_gogopzh','bbs_zcd','bbs_dscsq','bbs_msr',
          'bbs_mslt','bbs_snw','bbs_cdqss','bbs_wysq','bbs_tianfu','bbs_a028',
          'bbs_fufeng','bbs_wojubl','bbs_cdljl','bbs_yzlt','news_scpeople',
          'news_sctv','news_sc3n','news_scxww','news_sczx','news_sc_china',
          'news_echengdu','news_stocksc','blog_163','blog_hexun','blog_cnfol','blog_eastmoney',
          'bbs_cdzx','news_scrb','news_tfzb','news_cnfol','news_eastmoney','news_sinasc','news_xinhua_sc',
          'news_scwmw','news_cdwb','news_chinawestnews','news_scwxw','news_hxdsb','news_xnsb']
STARTID = 17
#print RUNLIST.index('bbs_gogopzh')+STARTID
#print RUNLIST.index('bbs_mslt')+STARTID
#print RUNLIST.index('news_sczx')+STARTID
#print RUNLIST[35-17]
#print len(RUNLIST)
def main():
#    while True:
        for id,item in enumerate(RUNLIST):
            module = __import__(item)
            print "starting to run %s.py" % (item)
            print id+STARTID
            try:
                flag = module.main(id+STARTID)
            except Exception as e:
                print "there is exception in %s.py" % (item)
                print e
#                return
                continue
            if not flag:
                print "%s.py go to sleep" % (item)
            else:
                print "%s.py run over" % (item)
 #       time.sleep(5)



if __name__ == "__main__":
    main()
    pass
