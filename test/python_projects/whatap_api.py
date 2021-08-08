import pandas as pd
from  urllib import parse
import requests 
import json


curlcmdlines = """curl '{site}/yard/api?type=sm&pcode={pcode}&path=%2Foid%2F{oid}%2Fcube{cubeType}&params={json_params}' 
  -H 'Connection: keep-alive' 
  -H 'sec-ch-ua: " Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"' 
  -H 'pragma: no-cache' 
  -H 'cache-control: no-cache' 
  -H 'sec-ch-ua-mobile: ?0' 
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48' 
  -H 'Accept: */*' 
  -H 'Sec-Fetch-Site: same-origin' 
  -H 'Sec-Fetch-Mode: cors' 
  -H 'Sec-Fetch-Dest: empty' 
  -H 'Referer: https://self.whatap.io/v2/project/sms/11/server_detail?oid=1138109075' 
  -H 'Accept-Language: ko,en;q=0.9,en-US;q=0.8' 
  -H 'Cookie: {cookie}' 
"""

def query(site='https://self.whatap.io', pcode=0, oid=0, cubeType='',cookie='cookie is required',  params={}):

    url = ""
    headers = {}
    for (i, l) in enumerate(curlcmdlines.split('\n')):
        l = l.strip()
        if i == 0 and len(l):
            fields = l.strip().split()
            url = fields[1].strip("''")
        elif len(l):
            fields = l.strip().split("'")[1].split(': ')
            if len(fields) == 2:
                if fields[0].lower() == 'cookie':
                    headers[fields[0]] = cookie
                else:
                    headers[fields[0]] = fields[1]
    url = url.format(site=site, pcode=pcode, oid=oid, cubeType=cubeType, json_params=json.dumps(params))
    r = requests.get(url, headers = headers, verify= False)
    
    if r.status_code < 300:
        return r.json()
    else:
        raise Exception((r.status_code, r.text))
