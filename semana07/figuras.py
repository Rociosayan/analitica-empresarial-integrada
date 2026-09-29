"""Figuras de los modelos de sustentación de la Semana 7 (mismo estilo que el modelo base)."""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

import calculos as C

RED, DRED, GREEN, GREY, INK = "#ED1C24", "#9E1218", "#1F7A3D", "#9A9A9A", "#222222"
plt.rcParams["font.family"] = "DejaVu Sans"


def _soles(x):
    return "S/ " + f"{x:,.0f}".replace(",", " ")


def _soles_c(x):
    return f"S/ {x:,.0f}"


# ---------------------------------------------------------------- Caso 1
def grafico_costos(ruta):
    r = C.caso1()
    a, b = r[C.C1["s_actual"]], r[C.C1["s_propuesta"]]
    cats = ["Costo fijo\n(planilla + plataforma)", "Costo de espera\n(oportunidad)",
            "Costo total\nmensual"]
    va = [round(a["fijo"]), round(a["espera"]), round(a["total"])]
    vb = [round(b["fijo"]), round(b["espera"]), round(b["total"])]
    fig, ax = plt.subplots(figsize=(10, 5.94), dpi=144)
    w = 0.32
    xs = range(3)
    ba = ax.bar([x - w / 2 for x in xs], va, w, color=DRED,
                label=f"Actual (s = {C.C1['s_actual']})")
    bb = ax.bar([x + w / 2 for x in xs], vb, w, color=RED,
                label=f"Propuesta (s = {C.C1['s_propuesta']})")
    for bars, vals in ((ba, va), (bb, vb)):
        for rect, v in zip(bars, vals):
            ax.text(rect.get_x() + rect.get_width() / 2, v + 350, _soles_c(v),
                    ha="center", va="bottom", fontsize=11, color=INK)
    ax.set_xticks(list(xs)); ax.set_xticklabels(cats, fontsize=11)
    ax.set_ylabel("Soles por mes", fontsize=11)
    ax.set_ylim(0, max(va + vb) * 1.16)
    ax.set_title("Comportamiento de los costos mensuales del servicio",
                 color=DRED, fontweight="bold", fontsize=13)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.legend(frameon=False, loc="upper left", fontsize=11)
    fig.tight_layout()
    fig.savefig(ruta); plt.close(fig)


# ------------------------------------------------------- utilidades de árbol
class Arbol:
    def __init__(self, w, h, xmax, ymax, escala=0.9):
        self.fig = plt.figure(figsize=(w, h), dpi=125)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, xmax); self.ax.set_ylim(0, ymax)
        self.ax.axis("off")
        self.fs = w * escala  # escala de fuente

    def nodo(self, x, y, num, tipo, r=0.36):
        if tipo == "decision":
            self.ax.add_patch(Rectangle((x - r, y - r), 2 * r, 2 * r, fill=False,
                                        ec=RED, lw=3, zorder=3))
        else:
            self.ax.add_patch(Circle((x, y), r, fill=False, ec=RED, lw=3, zorder=3))
        self.ax.text(x, y, str(num), color=RED, fontweight="bold", ha="center",
                     va="center", fontsize=self.fs * 1.25, zorder=4)

    def rama(self, p1, p2, etiqueta, color=INK, prob=None, costo=None, off=0.28,
             lw=2.2, lc="#555555"):
        (x1, y1), (x2, y2) = p1, p2
        self.ax.plot([x1, x2], [y1, y2], color=lc, lw=lw, solid_capstyle="round", zorder=1)
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        nx, ny = -math.sin(math.radians(ang)), math.cos(math.radians(ang))
        mx, my = x1 + (x2 - x1) * 0.5, y1 + (y2 - y1) * 0.5
        self.ax.text(mx + nx * off, my + ny * off, etiqueta, rotation=ang, color=color,
                     ha="center", va="center", fontsize=self.fs * 1.0,
                     rotation_mode="anchor")
        if prob is not None:
            px, py = x1 + (x2 - x1) * 0.80, y1 + (y2 - y1) * 0.80
            self.ax.text(px - nx * off * 1.15, py - ny * off * 1.15, prob, rotation=ang,
                         color=DRED, style="italic", ha="center", va="center",
                         fontsize=self.fs * 0.82, rotation_mode="anchor")
        if costo is not None:
            px, py = x1 + (x2 - x1) * 0.42, y1 + (y2 - y1) * 0.42
            self.ax.text(px - nx * off * 1.25, py - ny * off * 1.25, costo, rotation=ang,
                         color=DRED, style="italic", ha="center", va="center",
                         fontsize=self.fs * 0.82, rotation_mode="anchor")

    def texto(self, x, y, s, color=INK, bold=False, size=1.0, ha="left", italic=False):
        self.ax.text(x, y, s, color=color, fontweight="bold" if bold else "normal",
                     style="italic" if italic else "normal", ha=ha, va="center",
                     fontsize=self.fs * size)

    def guardar(self, ruta):
        self.fig.savefig(ruta); plt.close(self.fig)


# ---------------------------------------------------------------- Caso 2
def arbol_caso2(ruta):
    r = C.caso2(); p = r["pay"]; q = r["q"]
    t = Arbol(9.53, 6.0, 9.53, 6.0, escala=1.15)
    n1, n2, n3 = (0.9, 3.0), (3.75, 4.55), (3.75, 1.55)
    t.nodo(*n1, 1, "decision"); t.nodo(*n2, 2, "azar"); t.nodo(*n3, 3, "azar")
    t.rama(n1, n2, "Carta criolla tradicional", off=0.3)
    t.rama(n1, n3, "Línea vegetariana", off=0.3)
    ex = 7.2
    for nodo, (pa, pe), ve in ((n2, (p["trad_alta"], p["trad_est"]), r["ve_trad"]),
                               (n3, (p["veg_alta"], p["veg_est"]), r["ve_veg"])):
        y = nodo[1]
        ya, ye = y + 0.62, y - 0.62
        t.rama(nodo, (ex, ya), "Alta demanda saludable", prob=f"P = {r['p']:.2f}", off=0.25)
        t.rama(nodo, (ex, ye), "Demanda estable", prob=f"P = {q:.2f}", off=0.25)
        t.texto(ex + 0.15, ya, _soles(pa).replace("S/ ", ""), bold=True, size=1.25)
        t.texto(ex + 0.15, ye, _soles(pe).replace("S/ ", ""), bold=True, size=1.25)
        t.texto(nodo[0] - 0.4, y + 0.95, f"VE = {_soles(ve)}", color=GREEN, bold=True, size=1.1)
    t.texto(0.2, 0.35, f"Se elige: carta criolla tradicional (VE = {_soles(r['ve_trad'])})",
            color=GREEN, bold=True, size=1.0)
    t.guardar(ruta)


# ---------------------------------------------------------------- Caso 3
def arbol_caso3(ruta):
    r = C.caso3(); c = C.C3; q = 1 - c["p_alta"]
    t = Arbol(16, 8, 20, 10)
    n1, n2, n3, n4 = (1.2, 4.9), (5.4, 4.0), (9.6, 2.6), (13.3, 3.9)
    # rama superior: continuar
    leaf_c = (5.4, 8.0)
    t.rama(n1, leaf_c, "Continuar solo con el consultorio", off=0.3, color="#888888",
           lc="#AAAAAA")
    t.texto(5.65, 8.0, f"{_soles(c['seguro'])}  (seguro)", bold=True, size=1.15, color="#888888")
    t.texto(5.65, 8.6, f"se descarta: {_soles(r['e1'])} < {_soles(r['ve_neto'])}",
            color="#888888", size=0.85, italic=True)
    t.rama(n1, n2, "Lanzar telemedicina", costo=f"costo inicial {_soles(c['costo_ini'])}",
           off=0.3)
    t.rama(n2, (9.6, 6.1), "Alta aceptación", prob=f"P = {c['p_alta']:.2f}", off=0.3)
    t.rama(n2, n3, "Baja aceptación", prob=f"P = {q:.2f}", off=0.3)
    t.rama(n3, n4, "Campaña de descuentos", color=GREEN, off=0.3)
    t.rama(n3, (13.3, 1.2), "Cancelar el servicio", color="#888888", lc="#AAAAAA", off=0.3)
    t.rama(n4, (17.0, 5.0), "Respuesta favorable", prob=f"P = {c['p_camp_fav']:.2f}", off=0.28)
    t.rama(n4, (17.0, 2.8), "Respuesta desfavorable", prob=f"P = {1-c['p_camp_fav']:.2f}",
           off=-0.3)
    t.texto(9.85, 6.1, _soles(c["g_alta"]), bold=True, size=1.15)
    t.texto(13.55, 1.2, f"− {_soles(-c['cancelar'])}", bold=True, size=1.15, color="#888888")
    t.texto(13.55, 0.6, f"se descarta: −{_soles(-c['cancelar'])} < {_soles(r['ve_camp'])}",
            color="#888888", size=0.85, italic=True)
    t.texto(17.25, 5.0, _soles(c["u_camp_fav"]), bold=True, size=1.15)
    t.texto(17.25, 2.8, _soles(c["u_camp_des"]), bold=True, size=1.15)
    t.nodo(*n1, 1, "decision"); t.nodo(*n2, 2, "azar")
    t.nodo(*n3, 3, "decision"); t.nodo(*n4, 4, "azar")
    t.texto(3.3, 3.05, f"VE bruto = {_soles(r['ve_bruto'])}", color=GREEN, bold=True, size=1.0)
    t.texto(11.9, 4.75, f"VE = {_soles(r['ve_camp'])}", color=GREEN, bold=True, size=1.0)
    t.texto(1.0, 1.35, f"VE(lanzar) = {_soles(r['ve_bruto'])} − {_soles(c['costo_ini'])} = "
            f"{_soles(r['ve_neto'])}", color=DRED, size=1.0)
    t.texto(1.0, 0.85, f"VE(continuar) = {_soles(c['seguro'])}  →  se elige lanzar "
            f"(mayor VE)", color=DRED, size=1.0)
    t.guardar(ruta)


if __name__ == "__main__":
    import os
    os.makedirs("figuras", exist_ok=True)
    grafico_costos("figuras/caso1_costos.png")
    arbol_caso2("figuras/caso2_arbol.png")
    arbol_caso3("figuras/caso3_arbol.png")
