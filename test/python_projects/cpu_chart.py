<<<<<<< HEAD
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
%load_ext autoreload
%autoreload 2
import time
import whatap_api
from datetime import datetime

pcode=11
oid=467937344
cookie = '_gcl_au=1.1.1814738303.1628249276; _ga=GA1.2.1522852724.1628249276; _hjid=fe61576c-3c08-4bd4-bdf7-090483203cd8; _fbp=fb.1.1628249276608.1551479776; ch-veil-id=a4f13b56-8690-41b0-a761-58d78524906a; experimentation_subject_id=IjlkODVmNTI0LWUzODEtNDQ0ZC04MzlhLWIzNjNlZDA1YTU5YiI%3D--47cd9de970e7c9ec122ffbeb42d369290540a163; JSESSIONID=9O-K2uC40DOJsWy-jGKq8IiaDaAgV_k1HeOcFCIN; lang=ko; global.skin=wh; wa=qMYBot2UGvX9jMkAfilxvBayTQzuiEz6NFs75C0P0FzmCoT0d/B7VA==; ch-session-6280=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZXMiLCJrZXkiOiI2MjgwLTVmNWYxMTU2MTBmYTRjOGI5OWY3IiwiaWF0IjoxNjI4NDExNDY5LCJleHAiOjE2MzEwMDM0Njl9.jQnRcqdW5Z3An9wWty2FxHMsZMh8TvSbWSDiwveBZzs'
cubeType=''
etime = int(time.time()*1000)
stime = etime - 1000*60*60*24
params={'stime':stime, 'etime':etime, 'item':'cpu'}
r = whatap_api.query(pcode=pcode, oid=oid,cubeType=cubeType, cookie=cookie, params=params)

clocks = []
cpuHistory = []

for (clock, idle) in r['idle']:
    clocks.append(datetime.fromtimestamp(int(clock/1000)))
    cpuHistory.append(100.0-idle)
import plotly.express as px

fig = px.scatter(x=clocks, y=cpuHistory)
fig.show()




