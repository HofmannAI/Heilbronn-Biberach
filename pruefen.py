#!/usr/bin/env python3
"""Strukturelle Prüfung der erzeugten GLB; ergänzt keinen Planfreigabenachweis."""
from pathlib import Path
import json,struct,math
import numpy as np
from shapely.geometry import Polygon
ROOT=Path(__file__).resolve().parent
raw=(ROOT/'Finkenberg_Projekt.glb').read_bytes()
assert raw[:4]==b'glTF' and struct.unpack('<I',raw[4:8])[0]==2
assert struct.unpack('<I',raw[8:12])[0]==len(raw)
j=json.loads(raw[20:20+struct.unpack('<I',raw[12:16])[0]])
assert len(j['scenes'])==1 and j['scene']==0
assert j['scenes'][0]['name']=='Finkenberg_Hauptszene'
assert all('uri' not in b for b in j['buffers'])
assert not j.get('images') and not j.get('extensionsRequired')
visited=set()
def walk(i):
 assert i not in visited,'Node ist doppelt referenziert oder zyklisch'
 visited.add(i)
 for child in j['nodes'][i].get('children',[]):walk(child)
for i in j['scenes'][0]['nodes']:walk(i)
meshes=[j['nodes'][i]['mesh'] for i in visited if 'mesh' in j['nodes'][i]]
assert set(meshes)==set(range(len(j['meshes'])))
c=json.loads((ROOT/'daten/gebaeude_parameter.json').read_text());ps={}
for k,b in c.items():
 r=json.loads((ROOT/'daten'/b['register']).read_text());ang=r['angle'];R=np.array([[math.cos(ang),math.sin(ang)],[math.sin(ang),-math.cos(ang)]])
 st=b['stories']['EG'];ps[k]=Polygon((np.array(st['outline'])+st['shift'])@R.T*r['scale']+r['translation']).buffer(b['insulation'],join_style=2)
ids=[r['id'] for r in json.loads((ROOT/'daten/gml_auszug.json').read_text())];assert len(ids)==len(set(ids))
width12=(529.7831-179.4332)*25.4/720+.44
width14=(1000.552-165.466)*25.4/720+.44
assert abs(width12-12.80)<.01 and abs(width14-29.90)<.01
checks=dict(WA12_width_m=width12,WA14_width_m=width14,minimum_EG_facade_distance_m=ps['WA12'].distance(ps['WA14']),all_exported_meshes_reachable_in_main_scene=True,node_reuse_between_scenes=False,external_buffers_or_images=False,compression_decoder_required=False,source_building_ids_unique=True,WA12_OG_recess_depth_m=(529.7831-494.35)*25.4/720,WA14_OG_left_recess_depth_m=(215.07-165.466)*25.4/720)
a=json.loads((ROOT/'pruefwerte.json').read_text());a['geometric_checks']=checks;(ROOT/'pruefwerte.json').write_text(json.dumps(a,ensure_ascii=False,indent=2))
sizes=[dict(file=str(p.relative_to(ROOT)),bytes=p.stat().st_size) for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name!='dateigroessen.json']
assert all(p['bytes']<25_000_000 for p in sizes)
(ROOT/'dateigroessen.json').write_text(json.dumps(sizes,ensure_ascii=False,indent=2))
print(json.dumps(checks,indent=2));print('Alle Einzeldateien kleiner als 25.000.000 Byte.')
