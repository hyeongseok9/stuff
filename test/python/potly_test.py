import plotly.express as px
import pandas as pd
from datetime import datetime

series = []

import requests
import time
from datetime import datetime
from pprint import pprint
etime = int(time.time()* 1000)
stime = etime-(2*24*60*60* 1000)

pcode = 108
oid = 2026957691
process_list = requests.get('http://192.168.1.102:7710/sm/pcode/{}/oid/{}/proc/groupex2?item=procgroup&stime={}&etime={}&limit=9999&orderby=cpu,desc'.format(pcode, oid, stime, etime)).json()
group = '/data/whatap/lib/jdk/bin/java%p -jar /data/whatap/lib/whatap.server.yard-1.7.8.2804.jar'
groupid=None
for p in process_list['records']:
    if group in p['name']:
        groupid= p['groupKey']
        clocks = [ datetime.fromtimestamp(float(c)/float(1000)) for c in p['clock']]
        cpu = p['cpu']
        for i in range(len(clocks)):
            series.append((p['name'], clocks[i], cpu[i],))

args = dict(category='server_baseline', stime=stime, etime=etime, tags=dict(oid=oid, group=group), fields=["cpu50","cpu95"], max = 999999)

process_percentile = requests.post('http://192.168.1.102:7710/tagcount/pcode/{}/raws_min'.format(pcode, stime, etime), json=args).json()
fieldlookup = {}
fieldseries = {}
for kdict in process_percentile['fieldKeys']:
    fieldlookup[kdict['short']] = kdict['key']
    fieldseries[kdict['short']] = []

for d in process_percentile['data']:
    for f, v in d['fields'].items():
        series.append((fieldlookup[f], datetime.fromtimestamp(d['time']/1000), v))


process_cube = requests.get('http://192.168.1.102:7710/sm/pcode/{}/oid/{}/proc/group/{}/cube?stime={}&etime={}'.format(pcode,oid, groupid, stime, etime)).json()
from pprint import pprint

#pprint(process_cube)
clocks = [ datetime.fromtimestamp(float(c)/float(1000)) for c in process_cube['clock']]
cpu = process_cube['cpu']
for i in range(len(clocks)):
    series.append(('cube_', clocks[i], cpu[i],))

fig = px.line(pd.DataFrame(data=series, columns=('name', 'clock','value')), x="clock", y="value",color='name')
fig.show()
