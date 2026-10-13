#!/usr/bin/env python3
"""Regenerates the two conceptual PDFs. Requires pymupdf, reportlab, shapely, trimesh, numpy."""
from pathlib import Path
import json,io,math
import fitz,numpy as np,trimesh
from shapely.geometry import Polygon,MultiPoint
from shapely.ops import unary_union
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
R=Path(__file__).resolve().parent;D=R/'daten';W,H=landscape(A3)
GREEN='#385E50'; BLUE='#2079A5'; TEXT='#273932';LIGHT='#EFF3ED'
styles={'body':ParagraphStyle('body',fontName='Helvetica',fontSize=10,leading=14,textColor=HexColor(TEXT)), 'small':ParagraphStyle('small',fontName='Helvetica',fontSize=8,leading=11,textColor=HexColor(TEXT))}
def para(c,text,x,y,width,sty='body'):
 p=Paragraph(text,styles[sty]);_,h=p.wrap(width,500);p.drawOn(c,x,y-h);return y-h

def header(c,title,sub):
 c.setFillColor(HexColor(GREEN));c.rect(0,H-85,W,85,fill=1,stroke=0);c.setFillColorRGB(1,1,1);c.setFont('Helvetica-Bold',23);c.drawString(32,H-39,title);c.setFont('Helvetica',11);c.drawString(33,H-61,sub)
def footer(c,n):
 c.setFillColor(HexColor(TEXT));c.setFont('Helvetica',8);c.drawString(32,22,'Finkenbergstraße · Heilbronn-Biberach | Gestaltungsvorschlag · 13.10.2026 | Maße in m, keine Ausführungsfreigabe');c.drawRightString(W-32,22,str(n))
props=json.loads((D/'WA12_fenstervorschlag.json').read_text());conf=json.loads((D/'gebaeude_parameter.json').read_text())['WA12']
c=canvas.Canvas(str(R/'WA12_Fensterkonzept.pdf'),pagesize=(W,H))
for page_no,(sn,filename,clip) in enumerate([('EG','EG.pdf',(110,235,530,980)),('OG','OG.pdf',(150,220,550,980)),('PH','PH.pdf',(170,205,558,955))],1):
 header(c,'WA12 · Fenstervorschlag '+sn,'Raumbezogen, geradlinig und auf die Formate von WA14 abgestimmt')
 doc=fitz.open(R/'quellen/grundrisse_WA12'/filename);pg=doc[0];rows=[x for x in props if x['story']==sn];poly=Polygon(conf['stories'][sn]['outline'])
 for row in rows:
  a,b=row['ends_pdf'];pg.draw_line(a,b,color=(.12,.48,.65),width=4,overlay=True)
  x,y=row['center_pdf'];dx,dy=b[0]-a[0],b[1]-a[1];v=np.array([-dy,dx]);v=v/np.linalg.norm(v);test=np.array([x,y])+v*5
  if poly.covers(__import__('shapely').geometry.Point(test)):v=-v
  label=np.array([x,y])+v*12;pg.insert_text((float(label[0]-5),float(label[1]+3)),row['id'][-2:],fontsize=8,color=(.03,.3,.5),overlay=True)
 pix=pg.get_pixmap(matrix=fitz.Matrix(1.7,1.7),clip=fitz.Rect(clip),alpha=False);img=ImageReader(io.BytesIO(pix.tobytes('png')));ih=H-140;iw=ih*pix.width/pix.height;c.drawImage(img,32,48,width=iw,height=ih)
 x=max(450,32+iw+30);width=W-x-35;y=H-110
 y=para(c,'<b>Blau = neue Öffnung als Vorschlag.</b> Der bestehende Hauseingang bleibt erhalten. Die Grundrissaufteilung wird nicht geändert.',x,y,width)-12
 c.setFont('Helvetica-Bold',9);c.setFillColor(HexColor(TEXT));c.drawString(x,y,'Nr. / Raum');c.drawString(x+300,y,'B × H');c.drawString(x+380,y,'UK');y-=9
 for row in rows:
  c.setStrokeColor(HexColor('#D6DFD6'));c.line(x,y,x+width,y);y-=7
  label=row['id'][-2:]+' · '+row['room'];yy=para(c,label,x,y,292,'small')
  c.setFont('Helvetica',9);c.drawString(x+300,y-9,f"{row['width_m']:.2f} × {row['head_m']-row['sill_m']:.2f}");c.drawString(x+380,y-9,f"{row['sill_m']:.2f}")
  y=min(yy,y-12)-11
 y-=8;y=para(c,'<b>Gestaltungsregel:</b> 1,09 m für stehende Wohn-/Schlafraumfenster; 0,74 m für kleine, meist hochliegende Öffnungen; 2,40 / 2,99 m für breite Wohn- und Terrassenöffnungen. Gemeinsame Oberkanten: EG/OG 2,30 m, PH 2,40 m.',x,y,width,'small')-10
 notes={'EG':'Die Fenster berücksichtigen Bettstellwand, Küchenzeile und Sanitärobjekte. Abstellräume werden nicht pauschal verglast. Treppenhaus- und Technikfenster sind funktionale Vorschläge; Lüftung und Treppenschnitt sind abzustimmen.', 'OG':'WE2 erhält beide im Grundriss vorgesehenen Balkonzugänge, WE3 und WE4 jeweils einen. Das Bad von WE3 liegt innen und erhält kein Außenfenster. WE5 wird über zwei gleiche stehende Fenster belichtet. Ein rechnerischer Belichtungsnachweis ist nicht Bestandteil.', 'PH':'Beide Wohnungen erhalten einen direkten Dachterrassenzugang außerhalb der Küchenzeilen. Das WC von WE7 liegt innen; Öffnung 07 gehört zum außenliegenden Abstellraum. Fenster an der Treppe sind nach dem Schnitt zu prüfen.'}
 para(c,'<b>Grundrissbezug:</b> '+notes[sn],x,y,width,'small');footer(c,page_no);c.showPage()
c.save()
# Site plan: precise common coordinates, north up, nominal scale 1:400 at A3.
scene=trimesh.load(R/'Finkenberg_Projekt.glb',force='scene');sites={k:Polygon(v) for k,v in json.loads((D/'lageplan.json').read_text()).items()};land=json.loads((D/'freianlagen_entwurf.json').read_text());S=72/25.4*1000/400;E0=510329;N0=5449056
c=canvas.Canvas(str(R/'Freianlagen_Entwurf.pdf'),pagesize=(W,H));header(c,'Freianlagen · Einfacher Entwurf','WA12 und WA14 · vorhandene Erschließung erhalten, Grün- und Aufenthaltsbereiche ergänzen')
def xy(x,y):return (38+(x-E0)*S,57+(y-N0)*S)
def drawpoly(p,color,stroke=None):
 if p.is_empty:return
 for q in ([p] if p.geom_type=='Polygon' else getattr(p,'geoms',[])):
  if q.geom_type!='Polygon':continue
  pp=c.beginPath();pts=list(q.exterior.coords);pp.moveTo(*xy(*pts[0]));[pp.lineTo(*xy(*z)) for z in pts[1:]];pp.close()
  c.setFillColor(HexColor(color));c.setStrokeColor(HexColor(stroke or color));c.setLineWidth(.6);c.drawPath(pp,fill=1,stroke=1)
def footprint(m):
 v=np.column_stack([m.vertices[:,0]+510395,5449110-m.vertices[:,2]]);ps=[Polygon(v[f]) for f in m.faces];return unary_union([p for p in ps if p.area>.00001])
c.saveState();clip=c.beginPath();clip.rect(32,45,735,H-143);c.clipPath(clip,stroke=0,fill=0)
for k in ['WA12','WA14']:drawpoly(sites[k],'#DCE8CE',GREEN)
drawpoly(sites['water'],'#AED4DE')
for n,m in scene.geometry.items():
 if 'Fahrbahn' in n:drawpoly(footprint(m),'#C4C8C5')
 if n.startswith(('WA12_','WA14_')) and any(q in n for q in ['Freiflaeche_Plan','Zugang_Stellplatz','Offene_Stellplaetze','_Terrasse_']):drawpoly(footprint(m),'#E6DCC6')
for n,m in scene.geometry.items():
 if n.startswith(('WA12_','WA14_')) and ('EG_Decke_Boden' in n or 'Baukörper' in n):drawpoly(footprint(m),'#ADBBB4',GREEN)
for row in land['beds']:drawpoly(Polygon(row['polygon']),'#789466')
for row in land['seating']:drawpoly(Polygon(row['polygon']),'#B9A586');x,y=xy(*row['EN']);c.setStrokeColor(HexColor(GREEN));c.setLineWidth(3);c.line(x-7,y,x+7,y)
for row in land['trees']:
 x,y=xy(*row['EN']);c.setFillColor(HexColor('#A4BD83'));c.setStrokeColor(HexColor(GREEN));c.setLineWidth(.8);c.circle(x,y,row['crown_radius_m']*S,fill=1,stroke=1);c.setFillColor(HexColor(GREEN));c.circle(x,y,1.3,fill=1,stroke=0)
for k in ['WA12','WA14']:
 # Label floor footprint centroid.
 m=scene.geometry[k+'_EG_Decke_Boden'];p=footprint(m).centroid;x,y=xy(p.x,p.y);c.setFillColor(HexColor(GREEN));c.setFont('Helvetica-Bold',15);c.drawCentredString(x,y,k)
c.restoreState();x=800;y=H-112;y=para(c,'<b>Entwurfselemente</b>',x,y,340)-15
for color,label in [('#DCE8CE','Grünfläche / Rasen'),('#789466','Niedrige Pflanzbeete · Vorschlag'),('#A4BD83','3 kleinkronige Laubbäume · Vorschlag'),('#B9A586','Sitzplatz mit Bank · Vorschlag'),('#E6DCC6','Beläge / Zugänge / Stellplätze'),('#ADBBB4','Neubauten / Garagen'),('#AED4DE','Gewässer aus Lageplan')]:
 c.setFillColor(HexColor(color));c.rect(x,y-12,13,13,fill=1,stroke=0);y=para(c,label,x+23,y+2,310)-12
 y-=2
para(c,'<b>Konzept:</b> Bestehende Wege, Terrassen, Stellplätze und sechs Garagen bleiben erhalten. Neue niedrige Bepflanzung fasst geeignete Randbereiche ein. Die Bäume stehen außerhalb der Gebäude, Zufahrten und des Gewässerumrisses. Der Sitzplatz ergänzt den gemeinschaftlich nutzbaren Außenraum.',x,y-15,340)
y-=160;para(c,'<b>Planstatus:</b> Gestaltungsvorschlag auf dem vorhandenen Modell. Pflanzenarten, Leitungen, Wurzelschutz, Zufahrtsnachweise, Entwässerung, Spielplatz- und Fahrrad-/Müllausstattung sind noch abzustimmen. Keine Ausführungs- oder Genehmigungsplanung. Höhen und Gelände bleiben entsprechend dem dokumentierten Arbeitsstand.',x,y,340,'small')
c.setStrokeColor(HexColor(GREEN));c.setLineWidth(1.5);c.line(1090,165,1090,220);c.line(1090,220,1085,209);c.line(1090,220,1095,209);c.setFillColor(HexColor(GREEN));c.setFont('Helvetica-Bold',11);c.drawCentredString(1090,232,'N')
c.setFont('Helvetica',9);c.drawString(800,95,'M 1:400 bei Ausdruck auf A3 (100 %)');c.line(800,75,800+10*S,75)
for meters in [0,5,10]:c.line(800+meters*S,72,800+meters*S,78);c.drawCentredString(800+meters*S,60,str(meters)+' m')
footer(c,1);c.save();print('PDFs erstellt')
