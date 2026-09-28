import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np, pandas as pd, sqlite3
from matplotlib.patches import FancyBboxPatch
from runner import run_all
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.edgecolor': '#8a8984', 'axes.labelcolor': '#52514e',
                     'xtick.color': '#52514e', 'ytick.color': '#52514e', 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.titlesize': 8.5, 'axes.titleweight': 'bold', 'axes.titlecolor': '#1F3864'})
BLUE, ORANGE, AQUA, VIOLET, GRID, INK = '#2a78d6', '#eb6834', '#1baf7a', '#4a3aa7', '#e6e5e0', '#52514e'
ns, out = run_all()
raw = sqlite3.connect('rutamarket.db')
ped_raw = pd.read_sql_query(ns['consulta'], raw)
cli_raw = pd.read_sql_query('SELECT * FROM clientes', raw)
def grid(ax, axis='y'):
    ax.grid(axis=axis, color=GRID, lw=0.6); ax.set_axisbelow(True)

# ---- Figura EDA (Semana 5)
fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.4), dpi=220, gridspec_kw={'width_ratios': [1.25, 1, 1]})
ax = axs[0]
m = ped_raw['monto']; fuera = (m > 2000).sum()
ax.hist(m[m <= 2000], bins=40, color=BLUE, edgecolor='white', linewidth=0.4)
ax.set_title('Distribución del monto por pedido'); ax.set_xlabel('Monto (S/)'); ax.set_ylabel('Pedidos'); grid(ax)
ax.text(0.98, 0.95, f'{fuera} pedidos > S/ 2 000\nno se muestran', transform=ax.transAxes, ha='right', va='top', fontsize=6.8, color=INK)
ax = axs[1]
c = out['s5_resumen'][1]; lab = ['visitas', 'pedidos', 'gasto']
ax.imshow(c.values, cmap='Blues', vmin=0, vmax=1)
for i in range(3):
    for j in range(3):
        ax.text(j, i, f'{c.values[i, j]:.2f}', ha='center', va='center', fontsize=7.5, color='white' if c.values[i, j] > 0.6 else '#0b0b0b')
ax.set_xticks(range(3), lab); ax.set_yticks(range(3), lab); ax.set_title('Correlación (por cliente)')
for s in ax.spines.values(): s.set_visible(False)
ax = axs[2]
nul = pd.Series({'metodo_pago\n(pedidos)': ped_raw['metodo_pago'].isnull().sum(), 'ciudad\n(clientes)': cli_raw['ciudad'].isnull().sum(),
                 'edad\n(clientes)': cli_raw['edad'].isnull().sum()})
ax.barh(nul.index, nul.values, color=BLUE, height=0.55)
for y, v in enumerate(nul.values):
    ax.text(v + 2, y, str(v), va='center', fontsize=7.2, color=INK)
ax.set_title('Nulos según isnull()'); ax.set_xlabel('Registros'); grid(ax, 'x'); ax.invert_yaxis(); ax.set_xlim(0, 110)
plt.tight_layout(w_pad=1.6); plt.savefig('fig_eda.png', facecolor='white'); plt.close()

# ---- Figura boxplot (Semana 6)
ped_fix = ns['pedidos']
fig, axs = plt.subplots(1, 2, figsize=(7.4, 1.7), dpi=220)
for ax, serie, t in ((axs[0], ped_raw['monto'], 'Antes: con errores de digitación'), (axs[1], ped_fix['monto'], 'Después: precios corregidos con el catálogo')):
    ax.boxplot(serie, orientation='horizontal', widths=0.5, patch_artist=True, boxprops=dict(facecolor='#cfe0f5', edgecolor=BLUE),
               medianprops=dict(color=BLUE, lw=1.6), whiskerprops=dict(color=INK), capprops=dict(color=INK),
               flierprops=dict(marker='o', markersize=3, markerfacecolor=ORANGE, markeredgecolor='white', markeredgewidth=0.3, alpha=0.8))
    ax.set_title(t); ax.set_yticks([]); ax.set_xlabel('Monto del pedido (S/)'); grid(ax, 'x')
    ax.spines['left'].set_visible(False)
plt.tight_layout(w_pad=2); plt.savefig('fig_boxplot.png', facecolor='white'); plt.close()

# ---- Figura regresión (Semana 7)
df = ns['df']; reg = ns['reg']
fig, ax = plt.subplots(figsize=(4.6, 2.5), dpi=220)
Xtr, Xte = ns['X_train'], ns['X_test']
ax.scatter(df['visitas_web_mes'], df['gasto_2025'], s=10, color=BLUE, alpha=0.55, edgecolor='white', linewidth=0.3, label='Clientes')
xs = np.linspace(df.visitas_web_mes.min(), df.visitas_web_mes.max(), 50)
ax.plot(xs, ns['reg'].intercept_ + ns['reg'].coef_[0] * xs, color=ORANGE, lw=2, label='Recta de regresión')
ax.set_xlabel('Visitas a la web por mes'); ax.set_ylabel('Gasto 2025 (S/)'); grid(ax)
ax.set_title('Gasto anual según visitas a la web'); ax.set_xticks(range(1, 20, 2)); ax.legend(frameon=False, fontsize=7, loc='upper left')
plt.tight_layout(); plt.savefig('fig_regresion.png', facecolor='white'); plt.close()

# ---- Figura K-Means (Semana 8)
fig, axs = plt.subplots(1, 2, figsize=(7.4, 2.6), dpi=220, gridspec_kw={'width_ratios': [0.8, 1.2]})
ax = axs[0]
iner = eval(out['s8_escalar'][0])
ax.plot(range(1, 9), iner, color=BLUE, lw=2, marker='o', markersize=5, markerfacecolor=BLUE, markeredgecolor='white')
ax.plot(4, iner[3], marker='o', markersize=9, markerfacecolor='none', markeredgecolor=ORANGE, markeredgewidth=1.6)
ax.annotate('k = 4', (4, iner[3]), xytext=(5.1, iner[3] + 260), fontsize=7.5, color=INK, arrowprops=dict(arrowstyle='-', color=INK, lw=0.6))
ax.set_xlabel('Número de clusters (k)'); ax.set_ylabel('Inercia'); ax.set_title('Método del codo'); grid(ax)
ax = axs[1]
col = {'Frecuentes': (BLUE, 'o'), 'Regulares': (ORANGE, 's'), 'Inactivos': (AQUA, '^'), 'Compras grandes ocasionales': (VIOLET, 'D')}
for segm, (cc, mk) in col.items():
    d = df[df.segmento == segm]
    ax.scatter(d['dias_sin_comprar'], d['pedidos_2025'], s=12, color=cc, marker=mk, alpha=0.75, edgecolor='white', linewidth=0.3, label=f'{segm} ({len(d)})')
ax.set_xlabel('Días sin comprar (al 31/12/2025)'); ax.set_ylabel('Pedidos en 2025'); ax.set_title('Segmentos de clientes'); grid(ax)
ax.legend(frameon=False, fontsize=6.6, loc='upper right')
plt.tight_layout(w_pad=2); plt.savefig('fig_kmeans.png', facecolor='white'); plt.close()

# ---- CRISP-DM
fig, ax = plt.subplots(figsize=(7.2, 1.6), dpi=220)
et = ['1. Comprensión\ndel negocio', '2. Comprensión\nde los datos', '3. Preparación\nde los datos', '4. Modelado', '5. Evaluación', '6. Despliegue']
sem = ['Toda la unidad', 'Semana 5', 'Semana 6', 'Semanas 7 y 8', 'Semanas 7 y 8', 'Informe PMD1']
xs = np.linspace(0.9, 11.1, 6)
for i, (x, e) in enumerate(zip(xs, et)):
    ax.add_patch(FancyBboxPatch((x - 0.9, 0.45), 1.8, 0.95, boxstyle='round,pad=0.04,rounding_size=0.12', fc='#e3edf9', ec=BLUE, lw=1))
    ax.text(x, 0.93, e, ha='center', va='center', fontsize=6.3, color='#1F3864', weight='bold')
    ax.text(x, 0.2, sem[i], ha='center', va='center', fontsize=6.3, color=INK)
    if i < 5: ax.annotate('', xy=(xs[i + 1] - 0.92, 0.93), xytext=(x + 0.92, 0.93), arrowprops=dict(arrowstyle='->', color=INK, lw=0.9))
ax.annotate('', xy=(xs[0], 1.43), xytext=(xs[4], 1.43), arrowprops=dict(arrowstyle='->', color=ORANGE, lw=0.9, ls='--', connectionstyle='arc3,rad=0.12'))
ax.text((xs[0] + xs[4]) / 2, 1.95, 'Si la evaluación no es satisfactoria, se vuelve a comprender el negocio y los datos', ha='center', fontsize=6.5, color=ORANGE, style='italic')
ax.set_xlim(-0.2, 12.2); ax.set_ylim(0, 2.1); ax.axis('off')
plt.savefig('fig_crisp.png', bbox_inches='tight', facecolor='white'); plt.close()
print('ok')
