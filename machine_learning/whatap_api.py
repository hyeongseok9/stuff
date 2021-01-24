import requests, json, time, os

# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1



cookie=os.getenv('COOKIE', '_gcl_au=1.1.827900854.1607757609; _ga=GA1.2.1602347263.1607757609; _fbp=fb.1.1607757609151.454712246; _hjid=a8ed8cc8-ffc4-451c-aee4-43617a8e45ca; ch-veil-id=5e263e5d-7c4c-4d6f-9b9b-03b033b1bfab; global.skin=wh; lang=ko; JSESSIONID=YK6i43k4BF8vTDdQO2ugER-M5430bS5Z1Mn-gWtp; wa="qMYBot2UGvX9jMkAfilxvFWXnkg9URxfk6qAqmoH+S89SboQP2BiGw=="; ch-session-6280=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZXMiLCJrZXkiOiI2MjgwLTVmZDQ2ZjJiODc0MDc3YjYyNTM5IiwiaWF0IjoxNjExNDcxOTUyLCJleHAiOjE2MTQwNjM5NTJ9.V_T2GCtLN5Gue605JwGX9KcRydsTtFpKKKOdU5SotXg')

def requestProjectList(protocol=os.getenv('PROTOCOL', 'http'), host=os.getenv('HOST', 'dev.whatap.io:8080'), cookie=cookie):
    url = '{}://{}/account/api/v3/projects'.format(protocol, host)
    headers = {'Cookie': cookie, 'Content-Type': 'application/json'}

    page=1
    max=100
    for i in range(10):

        body = {"page":page,"max":max,"search":"","group":"","favorite":False,"onlyNoGroup":False}
        r = requests.post(url, headers=headers, data=json.dumps(body), verify=False)
        resp = r.json()
        if resp and 'projects' in resp and resp['projects']:
            for p in resp['projects']:
                yield p
        else:
            break
        page +=1     


def listServers(pcode = 0, stime=0, etime=0,protocol=os.getenv('PROTOCOL', 'http'), host=os.getenv('HOST', 'dev.whatap.io:8080')):
    url = '{}://{}/yard/api'.format(protocol, host)
    headers = {'Cookie': cookie, 'Content-Type': 'application/json'}
    params={'type':'sm', 'path':'/sm', 'pcode': pcode, 'params':'{{"stime": {} }}'.format(int(time.time()*1000))}
    r = requests.get(url, headers=headers, params=params, verify=False)
    resp = r.json()
    
    if resp and 'servers' in resp:
        for s in resp['servers']:
            yield s
    

def listProcess(pcode=0, oid=0, stime=0, etime=0,protocol=os.getenv('PROTOCOL', 'http'), host=os.getenv('HOST', 'dev.whatap.io:8080')):
    url = '{}://{}/yard/api'.format(protocol, host)
    headers = {'Cookie': cookie, 'Content-Type': 'application/json'}
    #type=sm&pcode=108&path=/oid/-1239179993/proc/groupex2&params={"item":"procgroup","stime":1610888288709,"etime":1610890088709,"orderby":"cpu,desc","limit":"10"}
    params={'type':'sm', 'path':'/oid/{}/proc/groupex2'.format(oid), 'pcode': pcode, 
        'params':'{{"item":"procgroup","stime":{},"etime":{},"orderby":"cpu,desc","limit":"9999"}}'.format(stime, etime)}
    
    r = requests.get(url, headers=headers, params=params, verify=False)
    resp = r.json()
    if resp and 'records' in resp:
        for p in resp['records']:
            yield p
    