import json, glob, os, re, sys, unicodedata, random, collections
sys.path.insert(0, os.path.dirname(__file__))
from geo2 import locate
R = 'research'
SEG = {'seg_expat': 'Anglophone / expats', 'seg_french': 'Francophone', 'seg_neuro': 'Neurodiversité',
       'seg_couples': 'Couples · LGBTQ+ · somatique', 'seg_general': 'Marché général',
       'seg_valles': 'Région · Vallès', 'seg_baix': 'Région · Baix Llobregat & côte', 'seg_nord': 'Région · Barcelonès nord & Maresme',
       'seg_quartiers': 'Barcelone · autres quartiers', 'seg_intl2': 'International (2e vague)'}

def norm(s):
    return re.sub(r'[^a-z ]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()).strip()

def key(x):
    n = norm(re.sub(r'\(.*?\)', '', x['name']))
    n = re.sub(r'\b(psicologia|centro|centre|centros|psicologico|de|la|clinica)\b', ' ', n)
    n = ' '.join(n.split())
    return ' '.join(n.split()[:2]) if x.get('type') == 'individual' else n

SPEC = [
    ('Anxiété & stress', r'anxi|stress|panic|phobi|ocd|toc|fear|worr|hypochond|burnout|\bgad\b'),
    ('Dépression & humeur', r'depress|mood|sadness|bipolar'),
    ('Trauma', r'trauma|ptsd|abuse|dissociat|emdr|violence|harass'),
    ('Couple', r'couple|marri|infidel|relationship|divorce|separation|jealous|pareja'),
    ('Sexualité', r'sex'),
    ('LGBTQ+', r'lgb|lgt|gay|queer|gender'),
    ('Non-monogamie', r'monogam|polyam|poliam'),
    ('TDAH', r'adhd|tdah'),
    ('Autisme', r'autis|asperger|\btea\b|\basd\b'),
    ('Haut potentiel', r'high abilit|gifted|\bhpi\b|high potential|altas capac|high intellectual'),
    ('Hypersensibilité', r'\bpas\b|highly sensitive|hypersens|alta sensib'),
    ('Diagnostic / bilan', r'diagnos|assessment|evaluation|neuropsych|wais|wisc'),
    ('Addictions', r'addict|alcohol|gambl|smoking|substance'),
    ('Dépendance affective', r'emotional depend|codepend|toxic rel'),
    ('Expatriation & interculturel', r'expat|cross-cult|intercult|cultur|relocat|bilingual'),
    ('Deuil & transitions', r'grief|loss|transition|life change|life cris|crises|existential|meaning'),
    ('Estime de soi', r'self-esteem|self-confid|self-crit|shame'),
    ('Enfants & ados', r'child|adolesc|teen|youth|school|learning|dyslex'),
    ('Famille', r'famil|parent'),
    ('Troubles alimentaires', r'eating'),
    ('Personnalité', r'personality|borderline|\bbpd\b'),
    ('Groupes', r'group|peer'),
    ('Corps & régulation', r'body|somat|regulat'),
]
APP = [
    ('TCC', r'\bcbt\b|cognitive|\btcc\b|rebt|behaviou?r'),
    ('3e vague (ACT, DBT, pleine conscience)', r'\bact\b|dbt|mindful|mbsr|mbct|compassion|\bcft\b|third-wave|\bfap\b|contextual'),
    ('EMDR & trauma', r'emdr|brainspot|lifespan integration|\bicv\b|stabiliz|trauma-focused|trauma-informed'),
    ('Psychodynamique / psychanalyse', r'psychodyn|psychoanal|lacan|winnicott|mentaliz|\bmbt\b|group anal'),
    ('Systémique', r'system|family therapy|strategic|nardone|minuchin|solution'),
    ('Humaniste / Gestalt', r'gestalt|humanist|person-cent|existential|transactional|transpersonal'),
    ('Émotions (EFT)', r'emotion-focused|emotionally focused|eft \(emotion|eft for couples|^eft$|\btfe\b'),
    ('Corps / somatique', r'somat|sensorimotor|body|bioenerg|\btre\b|polyvagal|dance|breath|yoga|leib|psychocorp|vittoz'),
    ('Hypnose', r'hypno'),
    ('IFS / parts', r'\bifs\b|parts work'),
    ('Créatif (art, drame, voix)', r'art therap|drama|psychodrama|creative|journal|play'),
    ('Intégrative', r'integrat|eclectic|holistic'),
    ('Couple (Gottman, Imago…)', r'gottman|imago|couple'),
    ('CNV', r'nonviolent|\bnvc\b|\bcnv\b'),
]
LANG = {'spanish': 'ES', 'castellano': 'ES', 'english': 'EN', 'catalan': 'CA', 'french': 'FR', 'italian': 'IT',
        'german': 'DE', 'swiss-german': 'DE', 'russian': 'RU', 'polish': 'PL', 'portuguese': 'PT', 'turkish': 'TR',
        'romanian': 'RO', 'dutch': 'NL', 'basque': 'EU', 'galician': 'GL', 'danish': 'DA', 'chinese': 'ZH',
        'afrikaans': 'AF', 'greek': 'EL', 'bulgarian': 'BG', 'swedish': 'SV', 'hungarian': 'HU', 'persian': 'FA',
        'valencian': 'CA'}

def tags(items, table):
    out = []
    for s in items or []:
        for lab, rx in table:
            if re.search(rx, s.lower()) and lab not in out:
                out.append(lab)
    return out

def status(x):
    c = ' '.join(x.get('credentials') or []).lower() + ' ' + (x.get('notable') or '').lower()
    if re.search(r'not (a )?licensed|non-psychologist|not listed as psycholog|complementary therapist|not a psychologist|counsell?or \(non|not a licensed|not (a )?registered|no copc|intern|registered (only )?in (italy|the uk|australia)|expired|gestalt therapist, not|medical doctor', c) \
            and not re.search(r'copc \d|general sanitari', c):
        return 'Non psychologue'
    if re.search(r'copc|col\.|colegiad|general sanitari|sanitari|licen[cs]e \d|\bpir\b|cop ', c):
        return 'Inscription visible'
    return 'Non affichée'

merged = {}
for f in sorted(glob.glob(os.path.join(R, 'seg_*.json'))):
    seg = SEG[os.path.basename(f)[:-5]]
    for x in json.load(open(f, encoding='utf-8')):
        k = key(x)
        if k in merged:
            m = merged[k]
            for fld, v in x.items():
                if isinstance(v, list):
                    m[fld] = list(dict.fromkeys((m.get(fld) or []) + v))
                elif v not in (None, '') and m.get(fld) in (None, ''):
                    m[fld] = v
            if seg not in m['segments']:
                m['segments'].append(seg)
        else:
            x['segments'] = [seg]
            merged[k] = x

DC = {'Eixample': (41.3888, 2.1620), 'Gràcia': (41.4036, 2.1546), 'Sarrià-Sant Gervasi': (41.4016, 2.1340),
      'Ciutat Vella': (41.3820, 2.1770), 'Les Corts': (41.3851, 2.1320), 'Sant Martí': (41.4040, 2.1990),
      'Sants-Montjuïc': (41.3730, 2.1490), 'Horta-Guinardó': (41.4180, 2.1670), 'Nou Barris': (41.4410, 2.1770),
      'Sant Andreu': (41.4350, 2.1900)}
random.seed(7)
out = []
for i, x in enumerate(merged.values()):
    d = x.get('district') or ''
    town = x.get('municipality') or ''
    if not town:
        a = (x.get('address') or '')
        town = 'Barcelona' if (d in DC or d in ('online only', '') or 'barcelona' in a.lower()) else d
    if town.lower().startswith('barcelona'):
        town = 'Barcelona'
    if town == 'Barcelona' and d not in DC:
        d = '' if d != 'online only' else d
    if town != 'Barcelona':
        d = ''
    v, prec = locate(x.get('address'), town)
    if v:
        import math
        from geo2 import nom
        c = [41.395, 2.165] if town == 'Barcelona' else nom({'q': town + ', Barcelona, Catalunya'})
        if c and math.hypot((v[0]-c[0])*111, (v[1]-c[1])*83) > (9 if town == 'Barcelona' else 6):
            v, prec = None, 'none'
    if not v and d in DC:
        v = [DC[d][0] + random.uniform(-.004, .004), DC[d][1] + random.uniform(-.004, .004)]
        prec = 'district'
    blob_s = (x.get('specialties') or []) + [p for p in (x.get('populations') or []) if re.search(r'lgb|lgt|expat|child|adolesc|neuro|autis|adhd', p.lower())]
    out.append({
        'id': i + 1, 'name': x['name'], 'type': x.get('type'), 'centre': x.get('centre'),
        'address': x.get('address'), 'municipality': town or None, 'district': d or None,
        'lat': round(v[0], 5) if v else None, 'lng': round(v[1], 5) if v else None, 'geo': prec,
        'langs': sorted(set(LANG[l.lower()] for l in x.get('languages') or [] if l.lower() in LANG)),
        'spec': tags(blob_s, SPEC), 'appr': tags(x.get('approaches'), APP),
        'specialties': x.get('specialties') or [], 'approaches': x.get('approaches') or [],
        'populations': x.get('populations') or [], 'education': x.get('education') or [],
        'credentials': x.get('credentials') or [], 'status': status(x),
        'years': x.get('years_experience'), 'formats': x.get('formats') or [], 'price': x.get('price_eur') or None,
        'rating': x.get('rating'), 'reviews': x.get('reviews_count'), 'review_platform': x.get('review_platform'),
        'website': x.get('website'), 'platforms': x.get('platforms') or [], 'media': x.get('publications_media') or [],
        'notable': x.get('notable'), 'sources': x.get('sources') or [], 'segments': x['segments']})
json.dump(out, open('data_merged.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('total', len(out), 'mapped', sum(1 for o in out if o['lat']), collections.Counter(o['geo'] for o in out))
print('status', collections.Counter(o['status'] for o in out))
print('types', collections.Counter(o['type'] for o in out))
print('multi-seg', [o['name'] for o in out if len(o['segments']) > 1])
print('no spec tag', [o['name'] for o in out if not o['spec']])
print('spec', collections.Counter(t for o in out for t in o['spec']).most_common())
print('appr', collections.Counter(t for o in out for t in o['appr']).most_common())
print('langs', collections.Counter(t for o in out for t in o['langs']).most_common())
p = sorted(o['price'] for o in out if isinstance(o['price'], (int, float)))
print('prices n', len(p), 'median', p[len(p)//2] if p else None, p)
print('reviews', sorted(((o['reviews'] or 0), o['name']) for o in out if o['reviews'])[-15:])
