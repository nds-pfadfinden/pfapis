from __future__ import print_function

import logging
import pathlib
import re

import pandas as pd
from decouple import config
from datetime import datetime

from pfapis.bdp_mv import Nami
from pfapis.confuence import Confluence

def berechne_alter(geburtsdatum_str):
    geburtsdatum = datetime.strptime(geburtsdatum_str, '%Y-%m-%d %H:%M:%S')
    heute = datetime.now()
    alter = heute.year - geburtsdatum.year
    if (heute.month, heute.day) < (geburtsdatum.month, geburtsdatum.day):
        alter -= 1
    return alter

def make_pretty_entry(raw_table):
    
    pretty = {}
    pretty['id'] = raw_table['entries_id']
    pretty['Vorname'] = raw_table['entries_vorname']
    pretty['Nachname'] = raw_table['entries_nachname']
    pretty['Spitznamen'] = raw_table['entries_spitzname']
    pretty['email'] = raw_table['entries_email']
    pretty['Stamm'] = re.sub(r'[0-9]', '', raw_table['entries_gruppierung'])
    pretty['telefon_1'] = raw_table['entries_telefon1']
    pretty['telefon_2'] = raw_table['entries_telefon2']
    pretty['mobil'] = raw_table['entries_telefon3']
    pretty['Alter'] = int(berechne_alter(raw_table['entries_geburtsDatum']))
    abg, lfd = get_sorted_taetigkeiten(raw_table['entries_id'])
    pretty['AbgeschlosseneTaetigkeiten'] = str(abg).lstrip('[').rstrip(']')
    pretty['LaufendeTaetigkeiten'] = str(lfd).lstrip('[').rstrip(']')
    return pretty

def get_sorted_taetigkeiten(mitgliedsid:int):
    taetigkeiten = mv.taetigkeit(mitgliedsid)
    abgeschlossen = []
    laufend = []
    for taetigkeit in taetigkeiten:
        if not taetigkeit['entries_aktivBis']:
            laufend.append(taetigkeit['entries_taetigkeit'])
            continue

        date = datetime.strptime(taetigkeit['entries_aktivBis'], "%Y-%m-%d %H:%M:%S")
        today = datetime.now()
        if date > today:
            laufend.append(taetigkeit['entries_taetigkeit'])
        else:
            abgeschlossen.append(taetigkeit['entries_taetigkeit'])
    return abgeschlossen, laufend

logging.basicConfig(level=logging.INFO)
# variables
path = str(pathlib.Path(__file__).parent.resolve())
mv_username = config("MV_USER")
mv_password = config("MV_PASSWORD")

nds_meinbdp = Confluence(
        url='https://nds.meinbdp.de:443',
        username=config("NDS_CONF_USER"),
        password=config("NDS_CONF_PASSWORD")
    )



config = []
mv = Nami(config)

rc = mv.auth(mv_username, mv_password)
id_ordentliche_mitglieder=1
results = mv.search({"gruppierung6Id": "07", "taetigkeitId": id_ordentliche_mitglieder}, limit=99999)
return_results = []
print(f"Get {len(results)} results") 
for idx, result in enumerate(results):
    print(f"({idx}/{len(results)})")
    return_results.append(make_pretty_entry(result))

gesamt_liste= pd.DataFrame(return_results)
print(gesamt_liste)
gesamt_liste_filtered = gesamt_liste[(gesamt_liste['Alter'] >= 21) & (gesamt_liste['Alter'] <= 24)]
gesamt_liste_filtered = gesamt_liste_filtered[~gesamt_liste_filtered['LaufendeTaetigkeiten'].str.contains('Stammesführer')]
gesamt_liste_filtered = gesamt_liste_filtered[~gesamt_liste_filtered['LaufendeTaetigkeiten'].str.contains('Landesvor')]
gesamt_liste_filtered = gesamt_liste_filtered[~gesamt_liste_filtered['AbgeschlosseneTaetigkeiten'].str.contains('Landesvor')]

print(gesamt_liste_filtered)
gesamt_liste_filtered.to_excel('./output.xlsx')
nds_meinbdp.uplaod_data_to_page(page_id=367198500, parent_id=365199453, title="MV Export 24", upload_file=True,
                               content=gesamt_liste_filtered,
                               header="<h3>Export aus der MV/h3>",
                               note="Diese Seite wurde mit der MV Generiert")
