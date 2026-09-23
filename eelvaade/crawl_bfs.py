import json, re, urllib.request, concurrent.futures as cf, time
H='http://localhost:8080'
seen=set(json.load(open('urls.json'))); seen.add('/')
queue=list(seen); res={}; bad=[]
def get(u):
    for i in range(3):
        try:
            r=urllib.request.urlopen(H+u, timeout=90); return u, r.status, r.read().decode()
        except urllib.error.HTTPError as e: return u, e.code, ''
        except Exception: time.sleep(1)
    return u, 0, ''
t=time.time()
with cf.ThreadPoolExecutor(8) as ex:
    while queue:
        batch, queue = queue, []
        for u, st, h in ex.map(get, batch):
            if st!=200: bad.append((u,st)); continue
            res[u]=h
            m=h[h.find('<main'):] if '<main' in h else h
            for href in re.findall(r'href="(?:http://localhost:8080)?(/[^"#?]*)', h):
                if href.startswith(('/wp-','/feed','/xmlrpc')) or re.search(r'\.(css|js|png|jpg|svg|xml|ico|woff2?)$', href): continue
                if href not in seen: seen.add(href); queue.append(href)
        print(len(res), 'lehte,', len(queue), 'järjekorras', round(time.time()-t),'s', flush=True)
json.dump(res,open('crawl/pages.json','w'))
json.dump(sorted(res), open('urls.json','w'))
print(len(res),'ok',len(bad),'bad',bad[:10], sum(len(v) for v in res.values())//1024,'KB')
