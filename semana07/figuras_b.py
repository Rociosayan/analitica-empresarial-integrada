"""Figuras de la Serie B (gráfico de costos y dos árboles de decisión)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import calculos_b as B
from figuras import Arbol, DRED, GREEN, INK, RED, _soles, _soles_c


def grafico_costos(ruta):
    r = B.caso1(); c = B.B1
    a, b = r[c["s_actual"]], r[c["s_propuesta"]]
    cats = ["Costo fijo\n(planilla + sistema)", "Costo de espera\n(oportunidad)",
            "Costo total\nmensual"]
    va = [round(a["fijo"]), round(a["espera"]), round(a["total"])]
    vb = [round(b["fijo"]), round(b["espera"]), round(b["total"])]
    fig, ax = plt.subplots(figsize=(10, 5.94), dpi=144)
    w = 0.32
    ba = ax.bar([x - w / 2 for x in range(3)], va, w, color=DRED,
                label=f"Actual (s = {c['s_actual']})")
    bb = ax.bar([x + w / 2 for x in range(3)], vb, w, color=RED,
                label=f"Propuesta (s = {c['s_propuesta']})")
    for bars, vals in ((ba, va), (bb, vb)):
        for rect, v in zip(bars, vals):
            ax.text(rect.get_x() + rect.get_width() / 2, v + 350, _soles_c(v),
                    ha="center", va="bottom", fontsize=11, color=INK)
    ax.set_xticks(range(3)); ax.set_xticklabels(cats, fontsize=11)
    ax.set_ylabel("Soles por mes", fontsize=11)
    ax.set_ylim(0, max(va + vb) * 1.16)
    ax.set_title("Comportamiento de los costos mensuales del servicio",
                 color=DRED, fontweight="bold", fontsize=13)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.legend(frameon=False, loc="upper left", fontsize=11)
    fig.tight_layout(); fig.savefig(ruta); plt.close(fig)


def arbol_caso2(ruta):
    r = B.caso2(); p = r["pay"]; q = r["q"]
    t = Arbol(9.53, 6.0, 9.53, 6.0, escala=1.15)
    n1, n2, n3 = (0.9, 3.0), (3.75, 4.55), (3.75, 1.55)
    t.nodo(*n1, 1, "decision"); t.nodo(*n2, 2, "azar"); t.nodo(*n3, 3, "azar")
    t.rama(n1, n2, "Café convencional", off=0.3)
    t.rama(n1, n3, "Café orgánico", off=0.3)
    ex = 7.2
    for nodo, (pa, pe), ve in ((n2, (p["conv_alto"], p["conv_est"]), r["ve_conv"]),
                               (n3, (p["org_alto"], p["org_est"]), r["ve_org"])):
        y = nodo[1]; ya, ye = y + 0.62, y - 0.62
        t.rama(nodo, (ex, ya), "Precio alto", prob=f"P = {r['p']:.2f}", off=0.25)
        t.rama(nodo, (ex, ye), "Precio estándar", prob=f"P = {q:.2f}", off=0.25)
        t.texto(ex + 0.15, ya, _soles(pa).replace("S/ ", ""), bold=True, size=1.25)
        t.texto(ex + 0.15, ye, _soles(pe).replace("S/ ", ""), bold=True, size=1.25)
        t.texto(nodo[0] - 0.4, y + 0.95, f"VE = {_soles(ve)}", color=GREEN, bold=True, size=1.1)
    t.texto(0.2, 0.35, f"Se elige: café orgánico (VE = {_soles(r['ve_org'])})",
            color=GREEN, bold=True, size=1.0)
    t.guardar(ruta)


def arbol_caso3(ruta):
    r = B.caso3(); c = B.B3; q = 1 - c["p_alta"]
    t = Arbol(16, 8, 20, 10)
    n1, n2, n3, n4 = (1.2, 4.9), (5.4, 4.0), (9.6, 2.6), (13.3, 3.9)
    t.rama(n1, (5.4, 8.0), "Continuar con carga seca", color=GREEN, off=0.3)
    t.texto(5.65, 8.0, f"{_soles(c['seguro'])}  (seguro)", bold=True, size=1.15, color=GREEN)
    t.texto(5.65, 8.6, f"SE ELIGE → VE = {_soles(r['mejor'])}", color=GREEN, bold=True, size=0.95)
    t.rama(n1, n2, "Lanzar línea refrigerada",
           costo=f"costo inicial {_soles(c['costo_ini'])}", off=0.3, color="#888888",
           lc="#AAAAAA")
    t.rama(n2, (9.6, 6.1), "Alta aceptación", prob=f"P = {c['p_alta']:.2f}", off=0.3)
    t.rama(n2, n3, "Baja aceptación", prob=f"P = {q:.2f}", off=0.3)
    t.rama(n3, n4, "Reorientar el servicio", costo=f"inversión {_soles(c['inv_extra'])}",
           color=GREEN, off=0.3)
    t.rama(n3, (13.3, 1.2), "Vender los camiones", color="#888888", lc="#AAAAAA", off=-0.3)
    t.rama(n4, (17.0, 5.0), "Respuesta favorable", prob=f"P = {c['p_fav']:.2f}", off=0.28)
    t.rama(n4, (17.0, 2.8), "Respuesta desfavorable", prob=f"P = {1-c['p_fav']:.2f}", off=-0.3)
    t.texto(9.85, 6.1, _soles(c["g_alta"]), bold=True, size=1.15)
    t.texto(13.55, 1.2, _soles(c["venta"]), bold=True, size=1.15, color="#888888")
    t.texto(13.55, 0.6, f"se descarta: {_soles(c['venta'])} < {_soles(r['nodo3'])}",
            color="#888888", size=0.85, italic=True)
    t.texto(17.25, 5.0, _soles(c["u_fav"]), bold=True, size=1.15)
    t.texto(17.25, 2.8, _soles(c["u_des"]), bold=True, size=1.15)
    t.nodo(*n1, 1, "decision"); t.nodo(*n2, 2, "azar")
    t.nodo(*n3, 3, "decision"); t.nodo(*n4, 4, "azar")
    t.texto(3.3, 3.05, f"VE bruto = {_soles(r['ve_bruto'])}", color=GREEN, bold=True, size=1.0)
    t.texto(10.6, 5.75, f"VE = {_soles(r['ve_reor_bruto'])} − {_soles(c['inv_extra'])}"
            f" = {_soles(r['ve_reor'])}", color=GREEN, bold=True, size=0.95)
    t.texto(1.0, 1.35, f"VE(lanzar) = {_soles(r['ve_bruto'])} − {_soles(c['costo_ini'])} = "
            f"{_soles(r['ve_neto'])}", color=DRED, size=1.0)
    t.texto(1.0, 0.85, f"VE(continuar) = {_soles(c['seguro'])}  →  se elige continuar "
            "(mayor VE)", color=DRED, size=1.0)
    t.guardar(ruta)


if __name__ == "__main__":
    import os
    os.makedirs("figuras", exist_ok=True)
    grafico_costos("figuras/b_caso1_costos.png")
    arbol_caso2("figuras/b_caso2_arbol.png")
    arbol_caso3("figuras/b_caso3_arbol.png")
