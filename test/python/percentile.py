import matplotlib.pyplot as plt
import requests
import time
from datetime import datetime
from pprint import pprint
etime = int(time.time()* 1000)
stime = etime-(24*60*60* 1000)

pcode = 108
oid = 2026957691
process_list = requests.get('http://192.168.1.102:7710/sm/pcode/{}/oid/{}/proc/groupex2?item=procgroup&stime={}&etime={}&limit=9999&orderby=cpu,desc'.format(pcode, oid, stime, etime)).json()
fig = plt.figure()
ax = fig.add_subplot(111)
group = '/data/whatap/lib/jdk/bin/java%p -jar /data/whatap/lib/whatap.server.yard-1.7.8.2804.jar'
for p in process_list['records']:
    if group in p['name']:
        clocks = [ datetime.fromtimestamp(float(c)/float(1000)) for c in p['clock']]
        cpu = p['cpu']
        ax.plot(clocks, cpu, label=p['name'])

args = dict(category='server_baseline', stime=stime, etime=etime, tags=dict(oid=oid, group=group), fields=["cpu50","cpu95"], max = 999999)

process_percentile = requests.post('http://192.168.1.102:7710/tagcount/pcode/{}/raws_min'.format(pcode, stime, etime), json=args).json()
fieldlookup = {}
fieldseries = {}
for kdict in process_percentile['fieldKeys']:
    fieldlookup[kdict['short']] = kdict['key']
    fieldseries[kdict['short']] = []

clocks =[]
for d in process_percentile['data']:
    clocks.append(datetime.fromtimestamp(d['time']/1000))
    for f, v in d['fields'].items():
        fieldseries[f].append(v)

for k, v in fieldseries.items():
    ax.plot(clocks, v, label=fieldlookup[k])

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
