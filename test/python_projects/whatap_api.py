import requests, json


import requests
import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


curlcmdlines = """curl '{hostprefix}/yard/api?type=sm&pcode={pcode}&path=%2Foid%2F{oid}%2Fcube{cubeType}&params={json_params}' 
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
  -H 'Cookie: cookie' 
"""

def query(hostprefix='https://self.whatap.io', pcode=0, oid=0, cubeType='', cookie='', params={}):
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
                k, v = fields
                if k.lower() == 'cookie':
                    v = cookie
                headers[k] = v
    json_params = json.dumps(params)
    url = url.format(hostprefix = hostprefix, pcode = pcode, oid= oid, cubeType=cubeType, json_params= json_params)
    r = requests.get(url, headers = headers, verify= False)
    
    if r.status_code < 300:
        return r.json()
    raise Exception(r.status_code, r.text)
