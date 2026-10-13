#!/usr/bin/env python3
"""Finkenberg: planbasierte, transparente Modellrekonstruktion.
python -m pip install numpy scipy shapely trimesh mapbox-earcut
python erzeugen.py
Die editierbaren Quellenableitungen liegen in daten/. Keine Netzwerkzugriffe.
Alle Koordinaten in Metern; Plan-XY ist in PDF-Punkten bei 1:100 gespeichert.
"""
from pathlib import Path
import json,math,struct
import numpy as np
import trimesh
from scipy.spatial import Delaunay,cKDTree
from scipy.interpolate import LinearNDInterpolator,NearestNDInterpolator
from shapely.geometry import Polygon,LineString,Point,box
from shapely.ops import unary_union,transform,nearest_points
from shapely.geometry.polygon import orient
from shapely.strtree import STRtree

HERE=Path(__file__).resolve().parent; DATA=HERE/'daten'
def read(n):return json.loads((DATA/n).read_text())
def write(n,v): (HERE/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
ORIGIN=np.array([510395.,5449110.,171.5]); S=25.4/720
STORY=2.90;SLAB=.24;ATTIKA=.35;HEAD=2.25;SILL=.90;RAIL=1.05
scene=trimesh.Scene(base_frame='Finkenberg_Hauptszene')
audit={'assumptions':{'floor_to_floor':STORY,'slab':SLAB,'roof_parapet':ATTIKA,'window_head':HEAD,'normal_sill':SILL,'railing':RAIL},'buildings':{},'removed_existing':[],'window_openings':[]}
colors={'Bestand':[184,185,180,255],'Putz':[224,214,195,255],'Penthaus':[210,201,184,255],'Bestandsdach':[159,157,149,255],'Gelaender':[178,170,151,255],'WA12_Platzhalter':[224,214,195,255],'Sockel':[171,175,167,255],'Dach':[119,124,117,255],'Metall':[77,73,67,255],'Glas':[126,150,153,255],'Belag':[193,181,158,255],'Rasen':[143,163,117,255],'Gelaende':[158,173,139,255],'Umgebungsgelaende':[193,197,178,255],'Asphalt':[133,137,134,255],'Bord':[199,199,185,255],'Wasser':[71,143,174,255],'Holz':[136,111,81,255],'Laub':[88,128,85,255]}
materials={k:trimesh.visual.material.PBRMaterial(name=k+('_angenommen' if k not in ['Bestand','Wasser'] else ''),baseColorFactor=v,metallicFactor=.28 if k=='Metall' else .1 if k=='Glas' else 0,roughnessFactor=.2 if k=='Glas' else .9,doubleSided=k in ['Bestand','Wasser','Gelaende','Umgebungsgelaende']) for k,v in colors.items()}
def local(v):
 a=np.asarray(v,dtype=float)-ORIGIN;return np.column_stack((a[:,0],a[:,2],-a[:,1]))
def add(mesh,name,mat,parent='Finkenberg_Hauptszene',metadata=None):
 if mesh is None or len(mesh.faces)==0:return
 mesh.visual=trimesh.visual.TextureVisuals(material=materials[mat]);mesh.metadata=metadata or {}
 scene.add_geometry(mesh,node_name=name,geom_name=name,parent_node_name=parent,metadata=mesh.metadata)
def group(name,parent='Finkenberg_Hauptszene'):scene.graph.update(frame_to=name,frame_from=parent,matrix=np.eye(4))
def polygons(g):
 if g.is_empty:return []
 if g.geom_type=='Polygon':return [g]
 return [p for p in getattr(g,'geoms',[]) if p.geom_type=='Polygon']
def solid(poly,bottom,top):
 out=[]
 for p in polygons(poly.buffer(0)):
  if p.area<.00001:continue
  # Work near zero to preserve triangulation precision.
  q=transform(lambda x,y:(np.asarray(x)-ORIGIN[0],np.asarray(y)-ORIGIN[1]),p)
  m=trimesh.creation.extrude_polygon(q,top-bottom,engine='earcut')
  a=m.vertices.copy();m.vertices=np.column_stack((a[:,0],a[:,2]+bottom-ORIGIN[2],-a[:,1]));out.append(m)
 return trimesh.util.concatenate(out) if out else None
def bar(a,b,width,bottom,top):return solid(LineString([a,b]).buffer(width/2,cap_style=2),bottom,top)
def combine(ms):return trimesh.util.concatenate([m for m in ms if m is not None]) if any(m is not None for m in ms) else None
def tube(a,b,r=.018):
 aa=local([a,b]);return trimesh.creation.cylinder(radius=r,segment=aa,sections=8)

conf=read('gebaeude_parameter.json');site={k:Polygon(v) for k,v in read('lageplan.json').items()};plots=unary_union([site['WA12'],site['WA14']]);regs={k:read(c['register']) for k,c in conf.items()}
def xy(k,s,points):
 r=regs[k];a=r['angle'];R=np.array([[math.cos(a),math.sin(a)],[math.sin(a),-math.cos(a)]])
 return (np.array(points)+conf[k]['stories'][s]['shift'])@R.T*S+r['translation']
def poly(k,s,p):return Polygon(xy(k,s,p)).buffer(0)
footprints={(k,s):poly(k,s,t['outline']).buffer(c['insulation'],join_style=2) for k,c in conf.items() for s,t in c['stories'].items()}
grading={}
for k in conf:
 base=footprints[(k,'EG')];patches=[base.buffer(.7)]
 for pp in read('belagsflaechen_pdf.json')[k+'_EG']:
  q=poly(k,'EG',pp)
  if 1.7<q.area<100 and q.distance(base)<.8 and q.intersection(base).area/q.area<.2:patches.append(q.buffer(.08))
 grading[k]=unary_union(patches)
group('Bestandsumgebung_LoD2')
rows=read('gml_auszug.json');ground=[];retained=[]
def gmlmesh(p):
 p=np.array(p,float)
 if np.linalg.norm(p[0]-p[-1])<1e-6:p=p[:-1]
 d=p-p[0];n=np.sum(np.cross(d,np.roll(d,-1,axis=0)),axis=0)
 if np.linalg.norm(n)<1e-7:return None
 n/=np.linalg.norm(n);u=p[1]-p[0];u/=np.linalg.norm(u);v=np.cross(n,u)
 q=Polygon(np.column_stack(((p-p[0])@u,(p-p[0])@v))).buffer(0)
 if q.geom_type!='Polygon':return None
 vv,ff=trimesh.creation.triangulate_polygon(q,engine='earcut');vv=p[0]+vv[:,0,None]*u+vv[:,1,None]*v
 if np.dot(np.cross(vv[ff[0,1]]-vv[ff[0,0]],vv[ff[0,2]]-vv[ff[0,0]]),n)<0:ff=ff[:,::-1]
 return trimesh.Trimesh(local(vv),ff,process=False)
for b in rows:
 rings=[np.array(p) for p in b['polygons']];v=np.concatenate(rings);h=min(v[:,2]);base=unary_union([Polygon(p[:,:2]).buffer(0) for p in rings if np.ptp(p[:,2])<.05 and abs(np.mean(p[:,2])-h)<.1])
 ground.extend(v[np.abs(v[:,2]-h)<.02].tolist())
 if not base.is_empty and (plots.covers(base.representative_point()) or base.intersection(plots).area/max(base.area,.01)>.65):
  audit['removed_existing'].append({k:b[k] for k in ['id','address','source']});continue
 retained.append(b['id']);name=(b['address'].replace(' ','_') or 'Nebengebaeude')+'__'+b['id'];group(name,'Bestandsumgebung_LoD2')
 for typ,mat in [('GroundSurface','Bestand'),('WallSurface','Bestand'),('RoofSurface','Bestandsdach')]:
  add(combine([gmlmesh(p) for p,t in zip(rings,b['surface_types']) if t==typ]),name+'_'+typ,mat,name,{'citygml_id':b['id'],'address':b['address'],'source':b['source'],'surface_type':typ})
# Preserve the previously established terrain exactly; LoD2 only replaces buildings.
ground=read('umgebung_bodenpunkte_lod1.json')


# Height field: measured points + surveyed lines; outside their hull use LoD1 base elevations.
survey=read('vermessung.json');surveypts=np.array(survey['points']);lines={d['handle']:d for d in survey['lines']}
pts=np.vstack([surveypts]+[np.array(d['points']) for d in survey['lines'] if d['layer']!=2181]);u,ix=np.unique(np.round(pts[:,:2],3),axis=0,return_index=True);pts=pts[ix]
interp=LinearNDInterpolator(pts[:,:2]-ORIGIN[:2],pts[:,2]);allpts=np.vstack([pts,np.array(ground)]);_,ii=np.unique(np.round(allpts[:,:2],2),axis=0,return_index=True);allpts=allpts[ii]
outside=LinearNDInterpolator(allpts[:,:2]-ORIGIN[:2],allpts[:,2]);nearest=NearestNDInterpolator(allpts[:,:2]-ORIGIN[:2],allpts[:,2]);survey_hull=Polygon(pts[Delaunay(pts[:,:2]).convex_hull.ravel(),:2]).convex_hull
def height(points,grade=True):
 p=np.asarray(points);h=interp(p-ORIGIN[:2]);h=np.where(np.isnan(h),outside(p-ORIGIN[:2]),h);h=np.where(np.isnan(h),nearest(p-ORIGIN[:2]),h)
 if grade:
  for k in conf:
   platform=grading[k]
   for i,pp in enumerate(p):
    dist=platform.distance(Point(pp))
    if dist<2.0:
     w=max(0,1-dist/2);h[i]=h[i]*(1-w)+(conf[k]['ffb']-.19)*w
 return h
def surface(g,offset=0,z=None):
 ms=[]
 for p in polygons(g):
  if p.area<.001:continue
  q=transform(lambda x,y:(np.asarray(x)-ORIGIN[0],np.asarray(y)-ORIGIN[1]),p.segmentize(1.5))
  vv,ff=trimesh.creation.triangulate_polygon(q,engine='earcut');en=vv+ORIGIN[:2];zz=height(en)+offset if z is None else np.full(len(vv),z)
  if len(ff) and np.cross(vv[ff[0,1]]-vv[ff[0,0]],vv[ff[0,2]]-vv[ff[0,0]])<0:ff=ff[:,::-1]
  ms.append(trimesh.Trimesh(local(np.column_stack((en,zz))),ff,process=False))
 return combine(ms)
group('Gelaende_und_Gewaesser');extent=box(510300,5449020,510495,5449220)
road_cut=Polygon([p[:2] for p in lines[3733]['points']]+[p[:2] for p in lines[3771]['points'][1:]][::-1]).buffer(0)
# Dense TIN assembled from grid + survey; triangle water intersections are clipped.
grid=np.array([(x,y) for x in np.arange(510300,510496,3) for y in np.arange(5449020,5449221,3)])
nodes=np.vstack([grid,pts[:,:2]]);nodes=np.unique(nodes.round(4),axis=0);tri=Delaunay(nodes-ORIGIN[:2]);ms1=[];ms2=[];terrain_cells=[]
for f in tri.simplices:
 t=Polygon(nodes[f]).intersection(extent).difference(site['water']).difference(road_cut)
 if t.is_empty:continue
 terrain_cells.append(t)
 (ms1 if survey_hull.covers(t.representative_point()) else ms2).append(surface(t))
add(combine(ms1),'Gelaende_TIN_Vermessung_interpoliert','Gelaende','Gelaende_und_Gewaesser')
add(combine(ms2),'Umgebung_Bodenhoehen_LoD1_schematisch','Umgebungsgelaende','Gelaende_und_Gewaesser')
terrain_index=STRtree(terrain_cells)
def drape(g,offset=.07):
 return combine([surface(g.intersection(terrain_cells[int(i)]),offset) for i in terrain_index.query(g,predicate='intersects')])
add(surface(site['water'],z=169.55),'Gewaesser_Umriss_WBF_Wasserstand_angenommen','Wasser','Gelaende_und_Gewaesser')
# River banks connect the mapped water area to the surrounding surveyed elevations.
bank=[];ring=np.array(site['water'].exterior.coords)
for a,b in zip(ring[:-1],ring[1:]):
 h=height([a,b]);vv=local([[a[0],a[1],169.5],[b[0],b[1],169.5],[b[0],b[1],h[1]],[a[0],a[1],h[0]]]);bank.append(trimesh.Trimesh(vv,[[0,1,2],[0,2,3]],process=False))
add(combine(bank),'Ufer_Boeschung_interpoliert','Gelaende','Gelaende_und_Gewaesser')
group('Finkenbergstrasse')
a=np.array(lines[3733]['points']);b=np.array(lines[3771]['points']);b=b[1:]
# Match the measured curb traces by arc length; the street spans the water as a bridge.
def sample_line(v,n=80):
 ds=np.r_[0,np.cumsum(np.linalg.norm(np.diff(v[:,:2],axis=0),axis=1))];t=np.linspace(0,ds[-1],n);return np.column_stack([np.interp(t,ds,v[:,i]) for i in range(3)])
aa=sample_line(a);bb=sample_line(b);vs=[];fs=[]
for i in range(len(aa)):
 vs.extend([aa[i]+[0,0,.025],bb[i]+[0,0,.025]])
 if i:
  j=2*i;fs.extend([[j-2,j-1,j+1],[j-2,j+1,j]])
add(trimesh.Trimesh(local(vs),np.array(fs),process=False),'Fahrbahn_Vermessene_Raender','Asphalt','Finkenbergstrasse')
curbs=[]
for points in [aa,bb]:
 for p,q in zip(points[:-1],points[1:]):curbs.append(tube(p+[0,0,.07],q+[0,0,.07],.07))
add(combine(curbs),'Bordkanten_Vermessung','Bord','Finkenbergstrasse')
road=Polygon(np.vstack([aa[:,:2],bb[::-1,:2]])).buffer(0)

surfdata=read('belagsflaechen_pdf.json')
def railing(g,h,name,parent,omit=None):
 ms=[]
 for p in polygons(g):
  cs=np.array(p.exterior.coords)
  for a,b in zip(cs[:-1],cs[1:]):
   seg=LineString([a,b]);mid=seg.interpolate(.5,normalized=True)
   if omit is not None and omit.distance(mid)<.12:continue
   ms.append(tube([*a,h+RAIL],[*b,h+RAIL],.022))
   ms.append(tube([*a,h+.16],[*b,h+.16],.014))
   n=max(1,math.ceil(seg.length/.9))
   for t in np.linspace(0,1,n+1):
    v=a+(b-a)*t;ms.append(tube([*v,h],[*v,h+RAIL],.021))
   for t in np.linspace(0,1,max(2,math.ceil(seg.length/.13))+1)[1:-1]:
    v=a+(b-a)*t;ms.append(tube([*v,h+.16],[*v,h+RAIL],.009))
 add(combine(ms),name,'Gelaender',parent,{'height_assumed_m':RAIL})

for k,c in conf.items():
 group(k);audit['buildings'][k]={'ffb':c['ffb'],'ffb_assumed':k=='WA12','registration':regs[k],'stories':{}}
 for si,(sn,st) in enumerate(c['stories'].items()):
  parent=k+'_'+sn;group(parent,k);h=c['ffb']+si*STORY
  source_poly=orient(Polygon(st['outline']),sign=1);base=footprints[(k,sn)];inner=poly(k,sn,st['outline']).buffer(-.20,join_style=2);shell=base.difference(inner)
  audit['buildings'][k]['stories'][sn]={'area_exterior_m2':base.area,'floor_elevation':h,'outline_pdf':st['outline'],'inside_site_percent':base.intersection(site[k]).area/base.area*100}
  floor=base
  if k=='WA12' and sn=='EG':floor=unary_union([base,poly(k,sn,[[290.56,599.5],[490.3977,599.5],[490.3977,958.3551],[290.56,958.3551]])])
  add(solid(floor,h-SLAB,h),parent+'_Decke_Boden','Sockel',parent)
  gaps=[]
  if k=='WA14':
   black=unary_union([Polygon(p).buffer(0) for p in read(parent+'_walls.json')]);ring=np.array(source_poly.exterior.coords)
   for edge,(ap,bp) in enumerate(zip(ring[:-1],ring[1:])):
    delta=bp-ap;L=np.linalg.norm(delta);u=delta/L;ni=np.array([-u[1],u[0]])
    # A line inside the 20 cm load-bearing wall detects the plan's real opening gaps.
    line=LineString([ap+ni*2.6,bp+ni*2.6]);empty=line.difference(black.buffer(.12));pieces=list(empty.geoms) if hasattr(empty,'geoms') else [empty]
    for g in pieces:
     if g.geom_type!='LineString' or g.length*S<.42:continue
     p1=np.array(g.coords[0]);p2=np.array(g.coords[-1]);t1=np.clip(np.dot(p1-ap,u),0,L);t2=np.clip(np.dot(p2-ap,u),0,L);lo,hi=sorted([t1,t2]);width=(hi-lo)*S
     if width>5.0 or lo<.5 or hi>L-.5:continue
     a0=xy(k,sn,[ap+u*lo])[0];b0=xy(k,sn,[ap+u*hi])[0]
     cut=LineString([a0,b0]).buffer(.65,cap_style=2)
     # Full-height access assumed on wide glazing facing terraces and the entry recess.
     sill=0 if width>2.2 or sn=='OG' and edge==17 or sn=='EG' and edge==2 and width>1.1 else SILL
     gaps.append((cut,sill,a0,b0,width,edge))
  if k=='WA12' and sn=='EG':
   # The entrance is actually drawn; remaining exterior windows are not supplied.
   a0,b0=xy(k,sn,[[426.62,542.0],[426.62,585.0]])
   gaps.append((LineString([a0,b0]).buffer(.65,cap_style=2),0,a0,b0,np.linalg.norm(b0-a0),3))
  walls=[]
  for z0,z1 in zip([0,SILL,HEAD],[SILL,HEAD,STORY-SLAB]):
   active=[g[0] for g in gaps if g[1]<=z0+.001];part=shell.difference(unary_union(active)) if active else shell;walls.append(solid(part,h+z0,h+z1))
  add(combine(walls),parent+'_Aussenwaende_mit_Rezessen','Penthaus' if sn=='PH' else 'Putz' if k=='WA14' else 'WA12_Platzhalter',parent,{'source':'Grundriss','window_layout':'planabgeleitet' if k=='WA14' else 'fehlend; geschlossene Platzhalterfassaden'})
  for i,(_,sill,a0,b0,width,edge) in enumerate(gaps):
   u=(b0-a0)/width;frame=[]
   a1=a0+u*.035;b1=b0-u*.035
   frame.extend([bar(a1,b1,.10,h+sill,h+sill+.065),bar(a1,b1,.10,h+HEAD-.065,h+HEAD)])
   for p in [a1,b1]:frame.append(solid(Point(p).buffer(.055,cap_style=3),h+sill,h+HEAD))
   if width>1.4:frame.append(solid(Point((a1+b1)/2).buffer(.026,cap_style=3),h+sill,h+HEAD))
   name=f'{parent}_Oeffnung_{i+1:02d}';add(combine(frame),name+'_Rahmen','Metall',parent)
   add(bar(a1,b1,.025,h+sill+.06,h+HEAD-.06),name+'_Glas','Glas',parent)
   audit['window_openings'].append({'building':k,'story':sn,'name':name,'edge':edge,'width_m':width,'sill_assumed_m':sill,'head_assumed_m':HEAD,'ends_EN':[a0.tolist(),b0.tolist()]})
  # Plan-colored exterior paving areas are filtered against each floor interior.
  terrace=[]
  for p in surfdata[parent]:
   pp=poly(k,sn,p)
   if pp.area<1.7:continue
   if pp.intersection(base).area/pp.area>.2:continue
   if sn!='EG' and pp.distance(base)>.65:continue
   if sn=='EG' and k=='WA14' and pp.area>100:continue
   if sn=='EG' and k=='WA12' and pp.distance(base)>1:continue
   terrace.append(pp)
  if terrace:
   for i,pp in enumerate(terrace):
    if sn=='EG':
     if pp.distance(base)<.8:add(solid(pp,h-.19,h-.015),f'{parent}_Terrasse_{i+1}','Belag',parent)
    else:
     # Close narrow insulation offsets to the wall, so slab and guardrails attach.
     slab=pp.buffer(.12,join_style=2).union(pp.buffer(.4,join_style=2).intersection(base.buffer(.025)))
     add(solid(slab,h-SLAB,h-.015),f'{parent}_Balkon_Dachterrasse_{i+1}','Belag',parent)
     railing(slab,h,f'{parent}_Gelaender_{i+1}',parent,omit=base)
  if sn=='PH':
   # User instruction: 0.50 m eaves only along terrace-facing penthouse edges.
   facing=[]
   terrace_area=unary_union(terrace)
   cs=np.array(base.exterior.coords)
   for aa,bb in zip(cs[:-1],cs[1:]):
    edge=LineString([aa,bb]);mid=edge.interpolate(.5,normalized=True)
    if terrace_area.distance(mid)<.65:
     facing.append(edge.buffer(.50,cap_style=2,join_style=2).difference(base))
   roof=base.union(unary_union(facing)).buffer(0)
   add(solid(roof,h+STORY-SLAB,h+STORY),parent+'_Decke_oben','Putz',parent,{'terrace_overhang_m':.50,'source':'Nutzervorgabe 13.10.2026; referenzbildorientiert'})
   add(solid(roof.buffer(-.12),h+STORY+.015,h+STORY+.06),k+'_Flachdach_Abdichtung','Dach',parent)
   parapet=roof.difference(roof.buffer(-.20,join_style=2));add(solid(parapet,h+STORY,h+STORY+ATTIKA),k+'_Dachattika_angenommen','Putz',parent)
   audit['buildings'][k]['terrace_overhang']={'width_m':.50,'added_roof_area_m2':roof.area-base.area,'edges':len(facing),'source':'Nutzervorgabe; nur terrassenzugewandte Kanten'}

 if k=='WA12':
  h=c['ffb'];pp=poly(k,'EG',[[290.56,599.5],[490.3977,599.5],[490.3977,958.3551],[290.56,958.3551]])
  add(solid(pp,h-.03,h),'WA12_Offene_Stellplaetze_Belag','Belag',k)
  cols=[]
  for y in [599.5,685.1,770.1,855.15,954.95]:
   p=xy(k,'EG',[[487,y]])[0];cols.append(solid(Point(p).buffer(.15,cap_style=3),h,h+STORY-SLAB))
  add(combine(cols),'WA12_EG_Stellplatzstuetzen','Sockel',k)
  for yy in [599.5,955.5]:
   a,b=xy(k,'EG',[[290.56,yy],[490.4,yy]]);add(bar(a,b,.20,h,h+STORY-SLAB),f'WA12_EG_Stellplatz_Seitenwand_{yy}','WA12_Platzhalter',k)

# WA14 external layout and garage footprints from the current EG drawing.
group('Freianlagen_WA14','WA14');gards=site['WA14'].difference(footprints[('WA14','EG')]).difference(road)
add(drape(gards,.035),'WA14_Garten_Gelaendeangepasst','Rasen','Freianlagen_WA14')
for i,p in enumerate(surfdata['WA14_EG']):
 pp=poly('WA14','EG',p)
 if pp.area>1.7 and pp.intersection(footprints[('WA14','EG')]).area/pp.area<.2:
  pp=pp.intersection(site['WA14']).difference(footprints[('WA14','EG')].buffer(.03))
  add(drape(pp,.09),f'WA14_Freiflaeche_Plan_{i+1}','Belag','Freianlagen_WA14')
garages=[[[488.48,850.77],[655.86,880.94],[640.88,964.07],[473.5,933.90]],[[844.74,871.78],[1012.12,901.95],[997.13,985.08],[829.75,954.91]],[[802.1,1108.34],[969.48,1138.51],[954.49,1221.64],[787.11,1191.48]],[[426.56,1049.32],[595.24,1071.06],[584.44,1154.84],[415.76,1133.09]],[[415.65,1133.94],[584.33,1155.68],[573.53,1239.46],[404.85,1217.72]],[[404.74,1218.56],[573.42,1240.30],[562.62,1324.08],[393.94,1302.34]]]
for i,pp in enumerate(garages):
 en=xy('WA14','EG',pp);g=Polygon(en);h=float(height([g.centroid.coords[0]])[0])+.06;parent=f'WA14_Garage_{i+1}';group(parent,'Freianlagen_WA14')
 add(solid(g,h,h+2.5),parent+'_Baukörper','Putz',parent)
 add(solid(g.buffer(.08,join_style=2),h+2.5,h+2.65),parent+'_Flachdach','Dach',parent)
 edge=1 if i in [0,3,4,5] else 3;a,b=en[edge],en[(edge+1)%4];u=(b-a)/np.linalg.norm(b-a);mid=(a+b)/2;v=mid-np.array(g.centroid.coords[0]);v=v/np.linalg.norm(v)*.015
 add(bar(a+u*.13+v,b-u*.13+v,.04,h+.03,h+2.15),parent+'_Tor','Metall',parent)
# WA12 has only a schematic external layout; limit paving to the shown access/parking zone.
group('Freianlagen_WA12','WA12');garden=site['WA12'].difference(footprints[('WA12','EG')]).difference(road)
add(drape(garden,.035),'WA12_Garten_angenommen','Rasen','Freianlagen_WA12')
access=unary_union([poly('WA12','EG',[[496.6,510],[695,510],[695,972],[496.6,972]]),poly('WA12','EG',[[290,958],[695,958],[695,1100],[290,1100]])]).intersection(site['WA12'])
ap,bp=nearest_points(access,road)
access=access.union(LineString([ap,bp]).buffer(1.5,cap_style=3)).difference(road)
add(drape(access,.09),'WA12_Zugang_Stellplatzvorzone_angenommen','Belag','Freianlagen_WA12')
# Existing survey walls, retained only outside the replacement sites.
walls=[]
for row in survey['lines']:
 if row['layer']!=2181:continue
 for a,b in zip(row['points'][:-1],row['points'][1:]):
  if plots.intersects(LineString([a[:2],b[:2]])):continue
  z=min(a[2],b[2]);walls.append(bar(a[:2],b[:2],.20,z-.5,z))
add(combine(walls),'Vermessene_Bestandsmauern_Hoehe_unten_angenommen','Sockel','Gelaende_und_Gewaesser')

scene.metadata={'title':'Finkenbergstraße WA12 und WA14','status':'Planbasiertes Arbeitsmodell; ungeklärte Höhen und WA12-Fensterplanung','units':'metre','origin_ENH':ORIGIN.tolist(),'axes':'X=E-510395; Y=H-171.50; Z=5449110-N','crs':'ETRS89 / UTM32, DHHN2016 NH','main_scene':'Finkenberg_Hauptszene','additional_scenes':False,'data_source':'Datenquelle: LGL, www.lgl-bw.de, dl-de/by-2-0. Zugeschnitten, konvertiert, ersetzter Bestand entfernt. Projektpläne: bereitgestellte Unterlagen; Rechte bei Urhebern.'}
def finish_tree(tree):
 tree['scenes'][0]['name']='Finkenberg_Hauptszene'
 tree['scene']=0
 # glTF stores linear color factors. Convert the human-selected sRGB swatches.
 for m in tree['materials']:
  a=m['pbrMetallicRoughness']['baseColorFactor'];m['pbrMetallicRoughness']['baseColorFactor']=[((v+.055)/1.055)**2.4 if v>.04045 else v/12.92 for v in a[:3]]+[a[3]]
raw=trimesh.exchange.gltf.export_glb(scene,tree_postprocessor=finish_tree);(HERE/'Finkenberg_Projekt.glb').write_bytes(raw)
loaded=trimesh.load(HERE/'Finkenberg_Projekt.glb',force='scene');assert np.allclose(scene.bounds,loaded.bounds,atol=.0001)
jlen=struct.unpack('<I',raw[12:16])[0];gltf=json.loads(raw[20:20+jlen]);assert len(gltf['scenes'])==1 and gltf['scene']==0
audit.update({'retained_citygml_buildings':len(retained),'removed_count':len(audit['removed_existing']),'survey_points':len(surveypts),'export_bytes':len(raw),'mesh_count':len(scene.geometry),'triangles':sum(len(m.faces) for m in scene.geometry.values()),'scene_count':len(gltf['scenes']),'default_scene':gltf['scene'],'bounds':scene.bounds.tolist(),'reimport_bounds_match':True,'window_count':len(audit['window_openings'])})
assert len(raw)<25_000_000
write('pruefwerte.json',audit);write('georeferenz.json',scene.metadata)
print(json.dumps({k:v for k,v in audit.items() if k not in ['buildings','window_openings','removed_existing']},indent=2))

