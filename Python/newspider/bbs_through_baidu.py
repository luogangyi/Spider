#! /usr/bin/env python
#coding=utf8

from BaseBBS import *
from bbs_utils import *
from baidu import Baidu

if __name__=="__main__":
    try:
        obj = Baidu(A028_INFO_SOURCE_ID,'www.tg280.com','bbs')
        obj.main()
    except Exception, e:
        store_error(A028_INFO_SOURCE_ID)
        bbs_logger.exception(e)  

    try:
        obj = Baidu(CDLJL_INFO_SOURCE_ID,'www.cd090.com','bbs')
        obj.main()
    except Exception, e:
        store_error(CDLJL_INFO_SOURCE_ID)
        bbs_logger.exception(e) 

    try:
        obj = Baidu(CDQSS_INFO_SOURCE_ID,'bbs.chengdu.cn','bbs')
        obj.main()
    except Exception, e:
        store_error(CDQSS_INFO_SOURCE_ID)
        bbs_logger.exception(e) 

    try:
        obj = Baidu(CDZX_INFO_SOURCE_ID,'www.cd.ccoo.cn','bbs')
        obj.main()
    except Exception, e:
        store_error(CDZX_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Baidu(CQKX_INFO_SOURCE_ID,'bbs.cqkx.com','bbs')
        obj.main()
    except Exception, e:
        store_error(CQKX_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Baidu(DSCSQ_INFO_SOURCE_ID,'91town.com','bbs')
        obj.main()
    except Exception, e:
        store_error(DSCSQ_INFO_SOURCE_ID)
        bbs_logger.exception(e) 

    try:
        obj = Baidu(DZ19_INFO_SOURCE_ID,'dz19.net','bbs')
        obj.main()
    except Exception, e:
        store_error(DZ19_INFO_SOURCE_ID)
        bbs_logger.exception(e) 

    try:
        obj = Baidu(FuFengL_INFO_SOURCE_ID,'bbs.fuling.com','bbs')
        obj.main()
    except Exception, e:
        store_error(FuFengL_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Baidu(GogoPZH_INFO_SOURCE_ID,'www.gogopzh.com','bbs')
        obj.main()
    except Exception, e:
        store_error(GogoPZH_INFO_SOURCE_ID)
        bbs_logger.exception(e)


    try:
        obj = Baidu(MSLT_INFO_SOURCE_ID,'bbs.qx818.com','bbs')
        obj.main()
    except Exception, e:
        store_error(MSLT_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Baidu(MSR_INFO_SOURCE_ID,'bbs.meishanren.com','bbs')
        obj.main()
    except Exception, e:
        store_error(MSR_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Baidu(SNW_INFO_SOURCE_ID,'suiningwang.com','bbs')
        obj.main()
    except Exception, e:
        store_error(SNW_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Baidu(TianFu_INFO_SOURCE_ID,'www.scol.cn','bbs')
        obj.main()
    except Exception, e:
        store_error(TianFu_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Baidu(WOJUBLBBSL_INFO_SOURCE_ID,'www.wojubl.com','bbs')
        obj.main()
    except Exception, e:
        store_error(WOJUBLBBSL_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Baidu(WYSQ_INFO_SOURCE_ID,'bbs.163.com','bbs')
        obj.main()
    except Exception, e:
        store_error(WYSQ_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Baidu(YZLT_INFO_SOURCE_ID,'soufun.com','bbs')
        obj.main()
    except Exception, e:
        store_error(YZLT_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Baidu(ZCD_INFO_SOURCE_ID,'www.chengtu.com','bbs')
        obj.main()
    except Exception, e:
        store_error(ZCD_INFO_SOURCE_ID)
        bbs_logger.exception(e)



        



