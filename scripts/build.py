"""Assemble index.html from src/template.html + data/*.json (single self-contained page)."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)
load = lambda p: json.load(open(D(p), encoding='utf-8'))

data = load('data/psychologues.json')
nm = load('data/raw/nicolas_market.json')['market']

FOOTPRINT = [
    ['psychologue-bcn.com (FR)', 'ok', 'actif', 'Site principal, complet. Logos COPC et Commission belge sans numéros. Livres non mentionnés.'],
    ['expatpsychotherapy.com (EN)', 'mid', 'figé', 'Blog arrêté en avril 2020, texte de modèle oublié, images qui renvoient à Bruxelles.'],
    ['therapiedecouplebruxelles.be', 'mid', 'ambigu', 'Le présente comme thérapeute de couple à Bruxelles, avec un numéro espagnol.'],
    ['psicologobruselas.be (ES)', 'no', 'mort', 'Le domaine ne répond plus, mais il est encore lié depuis le site anglais. Il n\'a donc plus de site en espagnol.'],
    ['therapiedecouplebarcelone.com', 'no', 'mort', 'Le domaine ne répond plus, mais il est encore indexé par Google.'],
    ['Doctoralia', 'no', 'absent', 'Aucun profil, alors que c\'est le canal n°1 de prise de rendez-vous en Espagne.'],
    ['Psychology Today / TherapyRoute / TopDoctors', 'no', 'absent', 'Introuvable sur les annuaires qu\'utilisent les expats.'],
    ['Google Business / avis Google', 'mid', 'à vérifier', 'Aucun avis n\'est remonté dans les recherches. À contrôler à la main.'],
    ['psico.org', 'no', 'obsolète', 'Ancienne adresse Hestia (Diagonal 343), prix d\'environ 40 €, 0 avis.'],
    ['MundoPsicologos · Expat.com', 'no', 'obsolète', 'Adresse Ronda Sant Antoni 80 et ancien associé. 0 avis, une recommandation.'],
    ['Vivre à Barcelone', 'ok', 'actif', 'Inscrit dans l\'annuaire francophone de référence (32 thérapeutes).'],
    ['Instagram @psychologue_bcn · Facebook · LinkedIn', 'mid', 'à vérifier', 'Les comptes existent. Activité et nombre d\'abonnés non lisibles automatiquement.'],
    ['YouTube « Hablamos Barcelona »', 'mid', '2014', '4 épisodes de 4 à 6 min (500-800 vues chacun) : format conversation en extérieur, ton léger.'],
    ['Biological Psychology (2011)', 'ok', 'publié', 'Co-auteur d\'un article sur l\'ocytocine et l\'alexithymie. Il ne l\'exploite nulle part.'],
    ['Livres « Kang » et « Guide pratique pour souffrir »', 'no', 'introuvables', 'Absents d\'Amazon, de Google Books et de ses propres sites en ligne.'],
]
FR_PRICE = {
    'Private psychologist session Barcelona (general range)': 'Séance psy privée Barcelone (fourchette annuaire)',
    'Individual adult session Barcelona (directory average)': 'Séance adulte individuelle (moyenne annuaire)',
    'Couple session Barcelona (directory average)': 'Séance de couple (moyenne annuaire)',
    'Online session Barcelona (directory)': 'Séance en ligne (annuaire)',
    'Psychology Today/Psicologia Hoy Barcelona average': 'Moyenne Psychology Today à Barcelone',
    'Spanish-speaking psychologist Barcelona': 'Psychologue hispanophone',
    'English-speaking therapist Barcelona': 'Thérapeute anglophone',
    'Couples therapy Barcelona (expat market)': 'Thérapie de couple, marché expat',
    'Online therapy English-language': 'Thérapie en ligne en anglais',
    'Therapy in Barcelona (English-speaking centre)': 'Therapy in Barcelona (centre anglophone)',
    'Ifeel (platform)': 'Ifeel (plateforme)',
    'TherapyChat (platform)': 'TherapyChat (plateforme)',
    'Nicolas Ruzette (for comparison)': 'Nicolas Ruzette',
}
prices = [{'item': FR_PRICE[p['item']], 'value': p['value'].replace('EUR', '€'), 'source': p['source']}
          for p in nm['prices'] if p['item'] in FR_PRICE]
TRENDS = [
    {'trend': 'Plus de gens consultent', 'detail': "Baromètre sanitaire 2025 : 2 Espagnols sur 10 ont eu besoin de soins en santé mentale dans l'année, et environ un tiers d'entre eux ont payé un professionnel privé."},
    {'trend': 'Un public saturé', 'detail': "Environ 6 psychologues publics pour 100 000 habitants (moyenne UE : ~18). 40 % des patients attendent 1 à 3 mois pour voir un spécialiste."},
    {'trend': 'TDAH et autisme adultes', 'detail': "Les diagnostics adultes « explosent ». Les centres privés de bilan se multiplient. DKV couvre la psychothérapie TSA/TDAH en 2026. Listes d'attente associatives jusqu'à 6 mois."},
    {'trend': 'La thérapie en ligne devient normale', 'detail': "38 % des patients consultent au moins en partie en ligne. Les plateformes (Unobravo, ifeel, TherapyChat) cassent les prix à 45-60 €."},
    {'trend': 'Plus de psychologues', 'detail': "47 396 psychologues sanitaires inscrits en Espagne en 2025 (+8,6 %), et environ 8 500 diplômés par an."},
    {'trend': 'Des expats en nombre record', 'detail': "26,6 % des habitants de Barcelone sont étrangers (460 409 au 1er janvier 2026). Les Européens forment le premier groupe. La séance en anglais se vend 15 à 40 € plus cher."},
]
LEGAL = [
    "« Psychologue » est un titre protégé, et l'inscription au collège régional (COPC en Catalogne) est obligatoire pour exercer.",
    "Soigner des patients en libéral est réservé aux Psicólogos Generales Sanitarios (master officiel PGS) et aux psychologues cliniciens issus du PIR (4 ans d'internat hospitalier).",
    "Une habilitation catalane transitoire existait pour ceux qui travaillaient dans un centre sanitaire autorisé avant le 6 octobre 2014.",
    "Avec un diplôme belge ou européen, il faut demander la reconnaissance comme PGS au Ministerio de Sanidad (directive 2005/36, gratuite, au cas par cas). Le diplôme belge et l'inscription à la Commission des Psychologues ne suffisent pas à eux seuls.",
    "Le praticien doit être inscrit au REPS (registre national des professionnels de santé), et le cabinet autorisé au Registre sanitaire de la Generalitat (Décret 151/2017, procédure simplifiée sous 100 m²).",
]
CH_FR = {
    'Doctoralia': "Place de marché n°1 en Espagne. Abonnement d'environ 89 à 129 € par mois, classement selon les avis, les disponibilités et la formule.",
    'Google Business Profile + local SEO': "Nom, adresse et téléphone doivent être identiques partout : chaque annuaire avec une ancienne adresse dilue le référencement.",
    'Psychology Today (Psicologia Hoy)': "171 profils à Barcelone, prix moyen affiché de 60 €. Très utilisé par les expats anglophones.",
    'Expat/English directories': "TherapyRoute, Expat Therapy 4U, Expat.com. Côté francophone : Vivre à Barcelone (32 fiches), Le Petit Journal, Equinox.",
}
channels = [{'channel': c['channel'].replace('Google Business Profile + local SEO', 'Google Business + référencement local')
             .replace('Expat/English directories', 'Annuaires expat'), 'detail': CH_FR.get(c['channel'], c['detail'])}
            for c in nm['acquisition_channels'] if c['channel'] in CH_FR]
channels.append({'channel': 'Assurances', 'detail': "Les assureurs espagnols (Sanitas, Adeslas, DKV) couvrent 15 à 20 séances par an mais paient peu. Les assureurs expat (Cigna, Allianz Care) remboursent les patients sur facture détaillée mentionnant le diagnostic et le titre du thérapeute."})
market = {'footprint': FOOTPRINT, 'prices': prices, 'trends': TRENDS, 'legal': LEGAL, 'channels': channels}

def js(o):  # safe inside <script type="application/json">
    return json.dumps(o, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

html = open(D('src/template.html'), encoding='utf-8').read()
html = (html.replace('__DATA__', js(data)).replace('__BARRIS__', js(load('data/barris.json')))
        .replace('__DISTRICTS__', js(load('data/districts.json'))).replace('__MARKET__', js(market))
        .replace('__N__', str(len(data))))
HEAD = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script>window.MAP_MODE = "osm";</script>
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
"""
open(D('artifact.html'), 'w', encoding='utf-8').write(html)  # claude.ai artifact: skeleton added at publish
style_end = html.index('</style>') + len('</style>')
html = HEAD + html[:style_end] + '\n</head>\n<body>\n' + html[style_end:] + '\n</body>\n</html>\n'
open(D('index.html'), 'w', encoding='utf-8').write(html)
print('index.html', round(len(html.encode()) / 1024), 'KB,', len(data), 'profils')
