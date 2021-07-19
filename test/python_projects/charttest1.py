#https://github.com/d3/d3-3.x-api-reference/blob/master/Formatting.md#d3_format
#!pip install chart_studio plotly

import pandas as pd
import requests 
curlcmdlines = """curl 'https://self.whatap.io/yard/api?type=sm&pcode=11&path=%2Foid%2F800278634%2Fproc%2Fgroup%2F-440650772&params=%7B%22stime%22%3A1621660935927%2C%22etime%22%3A1621662735927%2C%22proc_limit%22%3A10%7D'
  -H 'Connection: keep-alive'
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"' 
  -H 'pragma: no-cache' 
  -H 'cache-control: no-cache' 
  -H 'sec-ch-ua-mobile: ?0' 
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66' 
  -H 'Accept: */*' 
  -H 'Sec-Fetch-Site: same-origin' 
  -H 'Sec-Fetch-Mode: cors' 
  -H 'Sec-Fetch-Dest: empty' 
  -H 'Referer: https://self.whatap.io/v2/project/sms/11/server_detail?oid=800278634' 
  -H 'Accept-Language: ko,en;q=0.9,en-US;q=0.8' 
  -H 'Cookie: _gcl_au=1.1.867332439.1621328905; _fbp=fb.1.1621328904731.1928817789; _ga=GA1.2.73872690.1621328905; _hjid=41b92274-ed03-409a-92bf-f48240176e63; ch-veil-id=227033ad-fd7b-4466-8240-0b2c6d55b8e5; JSESSIONID=as1g1s8D0XByq02HM5ZFAzJsMVOeIJbvQSV1hkcK; wa=qMYBot2UGvX9jMkAfilxvKtvO7PXFfyAux/KPyY16DoMOIpE4PN+lw==; lang=ko; global.skin=wh; ch-session-6280=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZXMiLCJrZXkiOiI2MjgwLTYwYTM4NDBkMTRiZTE5N2UyNjg2IiwiaWF0IjoxNjIxNjYyNjI2LCJleHAiOjE2MjQyNTQ2MjZ9.yhQvHunoufQ5Uxk2CIqWe3UU1mvlm0bVCjcoFwcvWpI' 
"""

url = ""
headers = {}
for (i, l) in enumerate(curlcmdlines.split('\n')):
    l = l.strip()
    print(i, l)
    if i == 0 and len(l):
        fields = l.strip().split()
        url = fields[1].strip("''")
    elif len(l):
        fields = l.strip().split("'")[1].split(': ')
        if len(fields) == 2:
            headers[fields[0]] = fields[1]
r = requests.get(url, headers = headers, verify= False).json()
from datetime import datetime
clocks = [datetime.fromtimestamp(int(x/1000)) for x in r['clock']]
for nonseries in ['name','user','alert','proc.limit','net', 'file', 'proc', 'clock']:
    if nonseries in r:
        del r[nonseries]
yarddf = pd.DataFrame(r, index=clocks)
import plotly
print("plotly version :", plotly.__version__)
import chart_studio
chart_studio.tools.set_credentials_file(username='namhs9', api_key='3GqSrcrigctgFK9F9QHA')

import plotly.figure_factory as ff
import chart_studio.plotly as py
import plotly.graph_objs as go

pd.options.plotting.backend = "plotly"



fig = yarddf['cpu'].plot(title="Yard Perf CPU", template="simple_white")
fig.show()

fig = yarddf['memory'].plot(title="Yard Perf CPU", template="simple_white")
fig.show()

fig = yarddf['rss'].plot(title="Yard Perf CPU", template="simple_white")
fig.update_layout(yaxis_tickformat=".3s")
fig.show()


r = requests.get(url, headers = headers, verify= False).json()
yardnetdf = pd.DataFrame(r['net'], index=clocks)
fig = yardnetdf.plot(title="Yard Perf Net", template="simple_white")
fig.show()

