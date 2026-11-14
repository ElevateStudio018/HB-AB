#!/bin/bash
# lh.sh URL namn [desktop]
pre=""; [ "$3" = desktop ] && pre="--preset=desktop"
CHROME_PATH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome npx lighthouse "$1" $pre --quiet --chrome-flags="--headless=new --no-sandbox" --output=json --output-path="./$2.json" >/dev/null 2>&1
python3 - "$2" <<'PY'
import json,sys
d=json.load(open(f'./{sys.argv[1]}.json'))
c=d['categories']; print(sys.argv[1], {k:round(v['score']*100) for k,v in c.items()})
for k,cat in c.items():
  for r in cat['auditRefs']:
    a=d['audits'][r['id']]
    if a['score'] is not None and a['score']<0.9 and a['scoreDisplayMode'] not in ('manual','notApplicable','informative'):
      print('  ',k,r['id'],a.get('displayValue',''))
PY
