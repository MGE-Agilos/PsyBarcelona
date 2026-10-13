# Atlas Psy Barcelona

Cartographie de ~155 psychologues et centres de Barcelone (échantillon des acteurs visibles en ligne, octobre 2026) et analyse de positionnement de Nicolas Ruzette.

- `index.html` : page autonome publiée (générée)
- `src/template.html` : gabarit du dashboard
- `data/` : données consolidées (`psychologues.json`), fonds de carte (districts/quartiers, Open Data BCN), recherches brutes (`raw/`)
- `scripts/` : `merge.py` (fusion + géocodage OpenStreetMap), `build.py` (assemble `index.html`)

Reconstruire : `python scripts/merge.py data/raw` puis `python scripts/build.py`.
