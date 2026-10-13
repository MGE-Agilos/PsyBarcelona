import json, re, sys, time, urllib.parse, urllib.request, os
R=sys.argv[1]; cp=os.path.join(R,'geocache2.json')
cache=json.load(open(cp,encoding='utf-8')) if os.path.exists(cp) else {}
def nom(params):
    key=json.dumps(params,sort_keys=True,ensure_ascii=False)
    if key in cache: return cache[key]
    p=dict(params, format='json', limit=1, countrycodes='es')
    req=urllib.request.Request('https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode(p),headers={'User-Agent':'psy-bcn-market-study/1.0 (personal research)'})
    try: r=json.load(urllib.request.urlopen(req,timeout=20))
    except Exception as e: print('ERR',e); return None
    time.sleep(1.1)
    v=[float(r[0]['lat']),float(r[0]['lon'])] if r else None
    if v and not (41.1<v[0]<41.8 and 1.6<v[1]<2.7): v=None
    cache[key]=v; json.dump(cache,open(cp,'w',encoding='utf-8'),ensure_ascii=False); return v
def parse(a):
    a=re.split(r';|\(| also | and |previously',a)[0]
    pc=re.search(r'\b(08\d{3})\b',a); pc=pc.group(1) if pc else None
    a=re.sub(r'\b08\d{3}\b','',a)
    a=re.sub(r'\bC/\s*|\bC\.\s+|\bCalle\b|\bc/','Carrer ',a)
    a=a.replace('Av.','Avinguda').replace('Pza.','Plaça').replace('Plaza','Plaça')
    m=re.match(r'\s*([^,\d]+?)[\s,]+(\d+)',a)
    if not m: return None,None,pc
    return m.group(1).strip(' ,'), m.group(2), pc
def locate(addr, town='Barcelona'):
    town = town or 'Barcelona'
    if not addr:
        if town != 'Barcelona':
            v=nom({'q':f'{town}, Barcelona, Catalunya'})
            if v: return v,'town'
        return None,'none'
    st,num,pc=parse(addr)
    if st:
        v=nom({'street':f'{num} {st}','city':town})
        if v: return v,'address'
        st2=re.sub(r'^(Carrer|Avinguda|Plaça|Passeig|Ronda|Rambla|Via|Travessera|Gran Via)\s+(de la |de les |del |de |d\'|dels )?','',st,flags=re.I)
        v=nom({'q':f'{st2} {num}, {town}'})
        if v: return v,'address'
    if pc:
        v=nom({'postalcode':pc,'city':town})
        if v: return v,'postcode'
    if town != 'Barcelona':
        v=nom({'q':f'{town}, Barcelona, Catalunya'})
        if v: return v,'town'
    return None,'none'
if __name__=='__main__':
    import glob
    ok={}
    for f in sorted(glob.glob(os.path.join(R,'seg_*.json'))):
        for x in json.load(open(f,encoding='utf-8')):
            v,prec=locate(x.get('address')); ok[prec]=ok.get(prec,0)+1
            if prec!='address' and x.get('address'): print(prec,'|',x['address'])
    print(ok)
