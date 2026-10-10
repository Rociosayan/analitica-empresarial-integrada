"""Cálculos de la Serie B (3 casos nuevos) de sustentación — Semana 7.

Igual que calculos.py: cada resultado se verifica con un segundo método.
Uso:  python calculos_b.py
"""
from math import isclose

from calculos import birth_death, erlang_c, pct_ok, var_pct

# --------------------------------------------------------------------------
# Caso 1 — M/M/s  (Caja Rural Sol del Norte: ventanillas)
# --------------------------------------------------------------------------
B1 = dict(
    clientes=5, cada_min=10,          # llegadas: 5 clientes cada 10 min
    servicio_min=5,                   # un cajero atiende 1 cliente cada 5 min
    sueldo_dia=110, sistema_sem=150,
    costo_espera_h=20,
    horas_dia=8, dias_sem=6, sem_mes=4,   # lunes a sábado
    wq_max_min=3,
    s_actual=3, s_propuesta=4,
)


def caso1():
    c = B1
    lam = c["clientes"] * 60 / c["cada_min"]
    mu = 60 / c["servicio_min"]
    horas_mes = c["horas_dia"] * c["dias_sem"] * c["sem_mes"]
    fijo_unit = (c["sueldo_dia"] * c["dias_sem"] * c["sem_mes"]
                 + c["sistema_sem"] * c["sem_mes"])
    assert int(lam // mu) + 1 == c["s_actual"]        # mínimo estable
    out = dict(lam=lam, mu=mu, horas_mes=horas_mes, fijo_unit=fijo_unit)
    for s in (c["s_actual"], c["s_propuesta"], c["s_propuesta"] + 1):
        r = erlang_c(lam, mu, s)
        v = birth_death(lam, mu, s)
        for k in ("p0", "p_espera", "lq", "wq_min"):
            assert isclose(r[k], v[k], rel_tol=1e-9)
        r["fijo"] = fijo_unit * s
        r["espera"] = c["costo_espera_h"] * r["lq"] * horas_mes
        r["total"] = r["fijo"] + r["espera"]
        assert round(c["costo_espera_h"] * round(r["lq"], 4) * horas_mes) == round(r["espera"])
        out[s] = r
    a, b = out[c["s_actual"]], out[c["s_propuesta"]]
    s5 = out[c["s_propuesta"] + 1]
    assert round(a["fijo"]) + round(a["espera"]) == round(a["total"])
    assert round(b["fijo"]) + round(b["espera"]) == round(b["total"])
    assert a["wq_min"] > c["wq_max_min"] >= b["wq_min"]
    assert s5["total"] > b["total"]                    # un cajero más ya no conviene
    out["ahorro"] = round(a["total"]) - round(b["total"])
    out["caida_espera"] = round(a["espera"]) - round(b["espera"])
    out["alza_fijo"] = round(b["fijo"]) - round(a["fijo"])
    assert out["ahorro"] == out["caida_espera"] - out["alza_fijo"]
    out["pct_wq"] = pct_ok(round(a["wq_min"], 2), round(b["wq_min"], 2), a["wq_min"], b["wq_min"], 1)
    out["pct_lq"] = pct_ok(round(a["lq"], 4), round(b["lq"], 4), a["lq"], b["lq"], 1)
    out["pct_fijo"] = pct_ok(round(a["fijo"]), round(b["fijo"]), a["fijo"], b["fijo"], 1)
    out["pct_espera"] = pct_ok(round(a["espera"]), round(b["espera"]), a["espera"], b["espera"], 1)
    out["pct_total"] = pct_ok(round(a["total"]), round(b["total"]), a["total"], b["total"], 1)
    meta = c["wq_max_min"]
    out["pct_exceso_actual"] = pct_ok(meta, round(a["wq_min"], 2), meta, a["wq_min"], 0)
    out["pct_holgura_prop"] = pct_ok(meta, round(b["wq_min"], 2), meta, b["wq_min"], 0)
    for x in (a, b):
        x["rho_pct"] = round(x["rho"] * 100, 1)
        x["pw_pct"] = round(x["p_espera"] * 100, 1)
        x["peso_fijo"] = round(round(x["fijo"]) / round(x["total"]) * 100, 1)
        x["peso_espera"] = round(round(x["espera"]) / round(x["total"]) * 100, 1)
        assert round(x["peso_fijo"] + x["peso_espera"], 1) == 100.0
    return out


# --------------------------------------------------------------------------
# Caso 2 — árbol de un nivel (Finca cafetalera La Selva Alta)
# --------------------------------------------------------------------------
B2 = dict(
    p_alto=0.55,
    conv=dict(costo=90_000, ing_alto=170_000, ing_est=120_000),
    org=dict(costo=140_000, ing_alto=250_000, caida=0.40),
)


def caso2():
    c = B2
    p, q = c["p_alto"], 1 - c["p_alto"]
    cv, og = c["conv"], c["org"]
    ing_est_org = og["ing_alto"] * (1 - og["caida"])
    pay = dict(conv_alto=cv["ing_alto"] - cv["costo"], conv_est=cv["ing_est"] - cv["costo"],
               org_alto=og["ing_alto"] - og["costo"], org_est=ing_est_org - og["costo"])
    ve_c = p * pay["conv_alto"] + q * pay["conv_est"]
    ve_o = p * pay["org_alto"] + q * pay["org_est"]
    assert isclose(ve_c, p * cv["ing_alto"] + q * cv["ing_est"] - cv["costo"])
    assert isclose(ve_o, p * og["ing_alto"] + q * ing_est_org - og["costo"])
    p_eq = (pay["conv_est"] - pay["org_est"]) / (
        (pay["org_alto"] - pay["org_est"]) - (pay["conv_alto"] - pay["conv_est"]))
    assert isclose(p_eq * pay["conv_alto"] + (1 - p_eq) * pay["conv_est"],
                   p_eq * pay["org_alto"] + (1 - p_eq) * pay["org_est"])
    dif = ve_o - ve_c
    assert (dif > 0) == (p > p_eq)                    # coherencia con el equilibrio
    pc = dict(
        dif_sobre_conv=pct_ok(ve_c, ve_o, ve_c, ve_o, 1),
        dif_sobre_org=round(dif / ve_o * 100, 1),
        fav=pct_ok(pay["conv_alto"], pay["org_alto"], pay["conv_alto"], pay["org_alto"], 1),
        des=pct_ok(pay["conv_est"], pay["org_est"], pay["conv_est"], pay["org_est"], 1),
        caida_monto=og["ing_alto"] * og["caida"],
        p_eq=round(p_eq * 100, 1),
    )
    return dict(p=p, q=q, ing_est_org=ing_est_org, pay=pay, ve_conv=ve_c, ve_org=ve_o,
                dif=dif, p_eq=p_eq, pct=pc)


# --------------------------------------------------------------------------
# Caso 3 — árbol con recurso, dos niveles (Rutas del Sur: transporte refrigerado)
# --------------------------------------------------------------------------
B3 = dict(
    seguro=200_000, costo_ini=60_000,
    p_alta=0.55, g_alta=320_000,
    inv_extra=30_000,                       # inversión adicional si reorienta
    p_fav=0.40, u_fav=250_000, u_des=40_000,
    venta=50_000,                           # ingreso neto si vende los activos
)


def caso3():
    c = B3
    p, q = c["p_alta"], 1 - c["p_alta"]
    ve_reor_bruto = c["p_fav"] * c["u_fav"] + (1 - c["p_fav"]) * c["u_des"]
    ve_reor = ve_reor_bruto - c["inv_extra"]          # la inversión se paga en esa rama
    nodo3 = max(ve_reor, c["venta"])
    ve_bruto = p * c["g_alta"] + q * nodo3
    ve_neto = ve_bruto - c["costo_ini"]
    mejor = max(ve_neto, c["seguro"])
    ci, ie = c["costo_ini"], c["inv_extra"]
    hojas_reor = [(p, c["g_alta"] - ci),
                  (q * c["p_fav"], c["u_fav"] - ie - ci),
                  (q * (1 - c["p_fav"]), c["u_des"] - ie - ci)]
    hojas_venta = [(p, c["g_alta"] - ci), (q, c["venta"] - ci)]
    e2 = sum(w * x for w, x in hojas_reor)
    e3 = sum(w * x for w, x in hojas_venta)
    assert isclose(sum(w for w, _ in hojas_reor), 1)
    assert isclose(e2, ve_neto)
    assert mejor == c["seguro"] and ve_neto < c["seguro"]
    pc = dict(
        e2_vs_e1=pct_ok(c["seguro"], ve_neto, c["seguro"], ve_neto, 1),
        e3_vs_e1=pct_ok(c["seguro"], e3, c["seguro"], e3, 1),
        aporte_recurso=e2 - e3,
        aporte_rel=pct_ok(e3, e2, e3, e2, 1),
        p_hojas=[round(w * 100) for w, _ in hojas_reor],
    )
    assert sum(pc["p_hojas"]) == 100
    prob_menor = sum(w for w, x in hojas_reor if x < c["seguro"])
    return dict(ve_reor_bruto=ve_reor_bruto, ve_reor=ve_reor, nodo3=nodo3,
                ve_bruto=ve_bruto, ve_neto=ve_neto, mejor=mejor, e1=c["seguro"],
                e2=e2, e3=e3, dif=c["seguro"] - ve_neto, hojas_reor=hojas_reor,
                prob_menor=prob_menor, pct=pc)


if __name__ == "__main__":
    for nombre, f in (("CASO 1", caso1), ("CASO 2", caso2), ("CASO 3", caso3)):
        print(nombre)
        for k, v in f().items():
            print(" ", k, v)
    print("\nTodas las verificaciones cruzadas pasaron.")
