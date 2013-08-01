#! /usr/bin/env python
#coding=utf8
#update by lgy ,2013.08.01

from BaseBBS import *
from bbs_utils import *
from google_search import Google

if __name__=="__main__":
    try:
        obj = Google(A028_INFO_SOURCE_ID,'www.tg280.com','bbs')
        obj.main()
    except Exception, e:
        store_error(A028_INFO_SOURCE_ID)
        bbs_logger.exception(e)  

    try:
        obj = Google(CDLJL_INFO_SOURCE_ID,'www.cd090.com','bbs')
        obj.main()
    except Exception, e:
        store_error(CDLJL_INFO_SOURCE_ID)
        bbs_logger.exception(e) 

    try:
        obj = Google(CDQSS_INFO_SOURCE_ID,'bbs.chengdu.cn','bbs')
        obj.main()
    except Exception, e:
        store_error(CDQSS_INFO_SOURCE_ID)
        bbs_logger.exception(e) 

    try:
        obj = Google(CDZX_INFO_SOURCE_ID,'www.cd.ccoo.cn','bbs')
        obj.main()
    except Exception, e:
        store_error(CDZX_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Google(CQKX_INFO_SOURCE_ID,'bbs.cqkx.com','bbs')
        obj.main()
    except Exception, e:
        store_error(CQKX_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Google(DSCSQ_INFO_SOURCE_ID,'91town.com','bbs')
        obj.main()
    except Exception, e:
        store_error(DSCSQ_INFO_SOURCE_ID)
        bbs_logger.exception(e) 

    try:
        obj = Google(DZ19_INFO_SOURCE_ID,'dz19.net','bbs')
        obj.main()
    except Exception, e:
        store_error(DZ19_INFO_SOURCE_ID)
        bbs_logger.exception(e) 

    try:
        obj = Google(FuFengL_INFO_SOURCE_ID,'bbs.fuling.com','bbs')
        obj.main()
    except Exception, e:
        store_error(FuFengL_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Google(GogoPZH_INFO_SOURCE_ID,'www.gogopzh.com','bbs')
        obj.main()
    except Exception, e:
        store_error(GogoPZH_INFO_SOURCE_ID)
        bbs_logger.exception(e)


    try:
        obj = Google(MSLT_INFO_SOURCE_ID,'bbs.qx818.com','bbs')
        obj.main()
    except Exception, e:
        store_error(MSLT_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Google(MSR_INFO_SOURCE_ID,'bbs.meishanren.com','bbs')
        obj.main()
    except Exception, e:
        store_error(MSR_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Google(SNW_INFO_SOURCE_ID,'suiningwang.com','bbs')
        obj.main()
    except Exception, e:
        store_error(SNW_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Google(TianFu_INFO_SOURCE_ID,'www.scol.cn','bbs')
        obj.main()
    except Exception, e:
        store_error(TianFu_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Google(WOJUBLBBSL_INFO_SOURCE_ID,'www.wojubl.com','bbs')
        obj.main()
    except Exception, e:
        store_error(WOJUBLBBSL_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Google(WYSQ_INFO_SOURCE_ID,'bbs.163.com','bbs')
        obj.main()
    except Exception, e:
        store_error(WYSQ_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Google(YZLT_INFO_SOURCE_ID,'soufun.com','bbs')
        obj.main()
    except Exception, e:
        store_error(YZLT_INFO_SOURCE_ID)
        bbs_logger.exception(e)

    try:
        obj = Google(ZCD_INFO_SOURCE_ID,'www.chengtu.com','bbs')
        obj.main()
    except Exception, e:
        store_error(ZCD_INFO_SOURCE_ID)
        bbs_logger.exception(e)



        



