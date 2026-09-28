import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch
plt.rcParams['font.family']='DejaVu Sans'
NAVY='#1F3864'; TEAL='#2E75B6'; GRAY='#595959'

# DIKW
fig,ax=plt.subplots(figsize=(7.2,3.6),dpi=200)
cols=['#DEEAF6','#BDD7EE','#9DC3E6','#2E75B6']
labs=[('DATO','Hecho registrado, sin contexto','"Pedido 105: 2 unidades, S/ 240"'),
      ('INFORMACIÓN','Datos organizados y con contexto','"Tecnología generó casi la mitad de los ingresos de marzo"'),
      ('CONOCIMIENTO','Patrón comprendido y explicable','"Los clientes de Lima compran más tecnología"'),
      ('SABIDURÍA','Juicio para decidir y actuar','"Priorizar stock de tecnología para Lima en abril"')]
n=4
for i,(t,d,e) in enumerate(labs):
    y0=i; y1=i+1; w0=3.2*(1-i/n); w1=3.2*(1-(i+1)/n)
    ax.add_patch(Polygon([(-w0,y0),(w0,y0),(w1,y1),(-w1,y1)],closed=True,fc=cols[i],ec='white',lw=2))
    ax.text(0,y0+0.42,t[0] if t!='CONOCIMIENTO' else 'C',ha='center',va='center',fontsize=11,weight='bold',color='white' if i==3 else NAVY)
    ax.text(3.5,y0+0.62,t+'  ·  '+d,ha='left',va='center',fontsize=8.5,weight='bold',color=NAVY)
    ax.text(3.5,y0+0.3,e,ha='left',va='center',fontsize=7.8,color=GRAY,style='italic')
ax.annotate('',xy=(-3.9,4),xytext=(-3.9,0),arrowprops=dict(arrowstyle='->',color=GRAY,lw=1.2))
ax.text(-4.35,2,'más contexto, más valor',rotation=90,ha='center',va='center',fontsize=7.5,color=GRAY)
ax.set_xlim(-4.6,11.5); ax.set_ylim(-0.1,4.1); ax.axis('off')
plt.savefig('dikw.png',bbox_inches='tight',facecolor='white'); plt.close()

# Ciclo de vida
import numpy as np
fig,ax=plt.subplots(figsize=(7.2,2.3),dpi=200)
etapas=['1. Captura','2. Almacena-\nmiento','3. Limpieza y\npreparación','4. Análisis','5. Visualización\ny comunicación','6. Decisión','7. Archivo o\neliminación']
xs=np.linspace(0.6,12.6,7)
for i,(x,e) in enumerate(zip(xs,etapas)):
    ax.add_patch(FancyBboxPatch((x-0.88,0.35),1.76,1.0,boxstyle='round,pad=0.05,rounding_size=0.15',fc='#DEEAF6' if i%2==0 else '#BDD7EE',ec=TEAL,lw=1))
    ax.text(x,0.85,e,ha='center',va='center',fontsize=6.6,color=NAVY,weight='bold')
    if i<6: ax.annotate('',xy=(xs[i+1]-0.9,0.85),xytext=(x+0.9,0.85),arrowprops=dict(arrowstyle='->',color=GRAY,lw=1))
ax.annotate('',xy=(xs[0],0.3),xytext=(xs[5],0.3),arrowprops=dict(arrowstyle='->',color=TEAL,lw=1,ls='--',connectionstyle='arc3,rad=-0.12'))
ax.text((xs[0]+xs[5])/2,-0.3,'Las decisiones generan nuevos datos (nuevas ventas, nuevos registros)',ha='center',fontsize=7.2,color=TEAL,style='italic')
ax.set_xlim(-0.4,13.6); ax.set_ylim(-0.45,1.45); ax.axis('off')
plt.savefig('ciclo.png',bbox_inches='tight',facecolor='white'); plt.close()

# ER
fig,ax=plt.subplots(figsize=(7.4,4.2),dpi=200)
T={'clientes':(0.2,3.2,['PK id_cliente','nombre','ciudad','email','fecha_registro']),
   'pedidos':(3.7,3.2,['PK id_pedido','FK id_cliente','fecha_pedido','estado']),
   'detalle_pedido':(7.2,3.2,['PK,FK id_pedido','PK,FK id_producto','cantidad','precio_unitario']),
   'productos':(7.2,0.0,['PK id_producto','nombre_producto','FK id_categoria','precio_unitario']),
   'categorias':(3.7,0.0,['PK id_categoria','nombre_categoria'])}
W=2.7; H=0.36; box={}
for name,(x,y,attrs) in T.items():
    h=H*(len(attrs)+1)
    ax.add_patch(FancyBboxPatch((x,y),W,h,boxstyle='square,pad=0',fc='white',ec=NAVY,lw=1.2))
    ax.add_patch(FancyBboxPatch((x,y+h-H),W,H,boxstyle='square,pad=0',fc=NAVY,ec=NAVY,lw=1.2))
    ax.text(x+W/2,y+h-H/2,name,ha='center',va='center',color='white',fontsize=8.5,weight='bold')
    for j,a in enumerate(attrs):
        yy=y+h-H*(j+1.5)
        if a.startswith('PK') or a.startswith('FK'):
            tag,rest=a.rsplit(' ',1)
            ax.text(x+0.08,yy,tag,fontsize=6.5,color=TEAL,weight='bold',va='center')
            ax.text(x+0.85,yy,rest,fontsize=7.5,va='center',weight='bold' if 'PK' in tag else 'normal')
        else: ax.text(x+0.85,yy,a,fontsize=7.5,va='center')
    box[name]=(x,y,W,h)
def link(p1,p2,l1,l2,o1,o2):
    ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color=GRAY,lw=1.2)
    ax.text(p1[0]+o1[0],p1[1]+o1[1],l1,fontsize=8.5,weight='bold',color='#C00000',ha='center',va='center')
    ax.text(p2[0]+o2[0],p2[1]+o2[1],l2,fontsize=8.5,weight='bold',color='#C00000',ha='center',va='center')
yc=3.2+H*5-H*1.5
link((0.2+W,yc),(3.7,yc),'1','N',(0.15,0.15),(-0.15,0.15))
link((3.7+W,yc),(7.2,yc),'1','N',(0.15,0.15),(-0.15,0.15))
link((7.2+W/2,3.2),(7.2+W/2,0.0+H*5),'N','1',(0.2,-0.15),(0.2,0.15))
link((3.7+W,0.0+H*1.5),(7.2,0.0+H*1.5),'1','N',(0.15,0.15),(-0.15,0.15))
ax.text(0.2,2.6,'Lectura del modelo',fontsize=8,weight='bold',color=NAVY)
ax.text(0.2,2.4,'• Un cliente realiza muchos\n  pedidos (1:N).\n• Un pedido contiene muchos\n  productos y un producto aparece\n  en muchos pedidos (N:M): se\n  resuelve con detalle_pedido.\n• Una categoría agrupa muchos\n  productos (1:N).',fontsize=7,color=GRAY,va='top',linespacing=1.35)
ax.set_xlim(0,10.1); ax.set_ylim(-0.1,5.45); ax.axis('off')
plt.savefig('er.png',bbox_inches='tight',facecolor='white'); plt.close()
