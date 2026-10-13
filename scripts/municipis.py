"""Fetch municipality boundaries (OpenStreetMap / Nominatim) for the towns present in the data,
simplify them and write data/municipis.json (used by the vector map of the claude.ai version)."""
import json, os, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from simplify_geo import geom, rewind_d3  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'data', 'raw', 'municipis_cache.json')
cache = json.load(open(CACHE, encoding='utf-8')) if os.path.exists(CACHE) else {}

def fetch(name):
    if name in cache:
        return cache[name]
    q = {'q': name + ', Barcelona, Catalunya', 'format': 'json', 'limit': 1, 'polygon_geojson': 1,
         'countrycodes': 'es', 'featureType': 'settlement'}
    req = urllib.request.Request('https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode(q),
                                 headers={'User-Agent': 'psy-bcn-market-study/1.0 (personal research)'})
    r = json.load(urllib.request.urlopen(req, timeout=30))
    time.sleep(1.1)
    g = r[0]['geojson'] if r and r[0].get('geojson', {}).get('type') in ('Polygon', 'MultiPolygon') else None
    cache[name] = g
    json.dump(cache, open(CACHE, 'w', encoding='utf-8'))
    return g

if __name__ == '__main__':
    data = json.load(open(os.path.join(ROOT, 'data', 'psychologues.json'), encoding='utf-8'))
    towns = sorted({o['municipality'] for o in data if o.get('municipality') and o['municipality'] != 'Barcelona'})
    feats = []
    for t in towns:
        g = fetch(t)
        print(('ok  ' if g else 'MISS'), t)
        if g:
            feats.append({'type': 'Feature', 'properties': {'n': t}, 'geometry': rewind_d3(geom(g, 0.0004))})
    json.dump({'type': 'FeatureCollection', 'features': feats},
              open(os.path.join(ROOT, 'data', 'municipis.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(len(feats), 'municipalities')
