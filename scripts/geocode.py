import json, glob, os, re, sys, time, urllib.parse, urllib.request
R = sys.argv[1]  # research dir
cache_p = os.path.join(R, 'geocache.json')
cache = json.load(open(cache_p, encoding='utf-8')) if os.path.exists(cache_p) else {}
def q(s):
    if s in cache: return cache[s]
    url = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode({'q': s, 'format': 'json', 'limit': 1, 'countrycodes': 'es'})
    req = urllib.request.Request(url, headers={'User-Agent': 'psy-bcn-market-study/1.0 (personal research)'})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=20))
        cache[s] = [float(r[0]['lat']), float(r[0]['lon'])] if r else None
    except Exception as e:
        print('ERR', s, e); return None
    time.sleep(1.1)
    json.dump(cache, open(cache_p, 'w', encoding='utf-8'), ensure_ascii=False)
    return cache[s]
def clean(a):
    a = re.sub(r'\b(\d+)\s*[º°ª]?\s*[-,]?\s*\d*\s*[º°ª]\s*\d*[ªa]?\b', r'\1', a)  # floors
    a = re.sub(r'\b(planta|piso|pral\.?|principal|despacho|local|entresuelo|entlo\.?|1r|2n|3r|4t)\b.*?(,|$)', ',', a, flags=re.I)
    return a
for f in sorted(glob.glob(os.path.join(R, 'seg_*.json'))):
    for x in json.load(open(f, encoding='utf-8')):
        a = x.get('address')
        if not a: continue
        base = a if 'barcelona' in a.lower() else a + ', Barcelona'
        if q(clean(base)) is None:
            m = re.search(r'\b(08\d{3})\b', a)
            if m: q(m.group(1) + ' Barcelona')
print('cache size', len(cache), 'hits', sum(1 for v in cache.values() if v))
