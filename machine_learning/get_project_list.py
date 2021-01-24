import logging
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, filename='./get_project_list.log', level=logging.DEBUG)


requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


logger = logging.getLogger('history_crawler')

MINUTE_30=1000*60*30

import whatap_api, time, persist, sys
from pprint import pprint
def listProjects():
    etime = int(time.time()*1000)
    stime = etime - 1000*60*60 * 24 * 14
    for proj in whatap_api.requestProjectList():
        logger.debug(proj)
        if proj['productType'] != 'SMS':
            continue
        
        pcode = proj['pcode']
        try:
            logger.debug('pcode:', pcode)
            servers = whatap_api.listServers(pcode = pcode)
            logger.debug('servers:', servers)
            for s in servers:
                oid = s['oid']
                try:
                    etime_thistime = stime + MINUTE_30
                    while etime_thistime < etime:
                        stime_thistime = etime_thistime - MINUTE_30
                        processes = whatap_api.listProcess(pcode=pcode, oid=oid, stime=stime_thistime, etime=etime_thistime)
                        for p in processes:
                            try:
                                persist.store_process(pcode, oid , p)
                            except Exception as e:
                                logger.debug("store ",e)
                                logger.exception(e)
                        etime_thistime += MINUTE_30
                except Exception as e:
                    logger.debug('list process',e)
                    logger.exception(e)

        except Exception as e:
            logger.debug('list servers', e)
            logger.exception(e)


if __name__ == '__main__':
    listProjects()