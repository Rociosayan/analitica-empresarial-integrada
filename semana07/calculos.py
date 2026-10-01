"""Cálculos de los tres casos de sustentación de la Semana 7.

Todo número que aparece en los modelos DOCENTE y ESTUDIANTE sale de este módulo.
Cada resultado se verifica con un segundo método independiente (assert):

* Caso 1 (M/M/s): fórmula de Erlang C  vs.  distribución estacionaria del
  proceso de nacimiento y muerte resuelta numéricamente.
* Caso 2 (árbol de un nivel): valor esperado por rama  vs.  simulación exacta
  por enumeración de escenarios y punto de equilibrio de la probabilidad.
* Caso 3 (árbol con recurso): roll-back  vs.  enumeración de las tres
  estrategias completas con sus resultados netos en cada hoja.

Uso:  python calculos.py
"""
from math import factorial, isclose

# --------------------------------------------------------------------------
# Caso 1 — Teoría de colas M/M/s (Clínica Valle Sur)
# --------------------------------------------------------------------------
C1 = dict(
    llamadas=4, cada_min=15,          # llegadas: 4 llamadas cada 15 min
    servicio_min=12,                  # 1 llamada cada 12 min por operador
    sueldo_dia=130, plataforma_sem=175,
    costo_espera_h=25,                # S/ por paciente y por hora en cola
    horas_dia=8, dias_sem=5, sem_mes=4,
    wq_max_min=6,
    s_actual=4, s_propuesta=5,
)


def var_pct(base, nuevo):
    """Variación porcentual = (nuevo − base) ÷ base × 100  (la base es el valor de referencia)."""
    return (nuevo - base) / base * 100


def pct_ok(base_mostrada, nueva_mostrada, base_exacta, nueva_exacta, dec):
    """Variación % calculada con los valores MOSTRADOS en el cuadro (lo que puede repetir
    el estudiante) y con los valores SIN redondear: deben coincidir al decimal publicado."""
    a = round(var_pct(base_mostrada, nueva_mostrada), dec)
    b = round(var_pct(base_exacta, nueva_exacta), dec)
    assert a == b, (base_mostrada, nueva_mostrada, a, b)
    return a


def erlang_c(lam, mu, s):
    """Medidas de rendimiento del M/M/s con la fórmula de Erlang C."""
    a = lam / mu
    rho = a / s
    assert rho < 1, "el sistema no es estable"
    p0 = 1 / (sum(a**n / factorial(n) for n in range(s))
              + a**s / (factorial(s) * (1 - rho)))
    p_espera = a**s / (factorial(s) * (1 - rho)) * p0
    lq = p_espera * rho / (1 - rho)
    wq = lq / lam                       # horas (Little)
    return dict(a=a, rho=rho, p0=p0, p_espera=p_espera, lq=lq,
                wq_h=wq, wq_min=wq * 60)


def birth_death(lam, mu, s, n_max=600):
    """Verificación independiente: distribución estacionaria numérica."""
    w = [1.0]
    for n in range(1, n_max + 1):
        w.append(w[-1] * lam / (min(n, s) * mu))
    z = sum(w)
    p = [x / z for x in w]
    lq = sum((n - s) * p[n] for n in range(s + 1, n_max + 1))
    p_espera = sum(p[n] for n in range(s, n_max + 1))
    return dict(p0=p[0], p_espera=p_espera, lq=lq, wq_min=lq / lam * 60)


def caso1():
    c = C1
    lam = c["llamadas"] * 60 / c["cada_min"]         # pacientes/hora
    mu = 60 / c["servicio_min"]                      # pacientes/hora/operador
    horas_mes = c["horas_dia"] * c["dias_sem"] * c["sem_mes"]
    fijo_unit = (c["sueldo_dia"] * c["dias_sem"] * c["sem_mes"]
                 + c["plataforma_sem"] * c["sem_mes"])
    s_min = int(lam // mu) + 1                       # mínimo estable
    assert s_min == c["s_actual"]
    out = dict(lam=lam, mu=mu, horas_mes=horas_mes, fijo_unit=fijo_unit,
               s_min=s_min)
    for s in (c["s_actual"], c["s_propuesta"], c["s_propuesta"] + 1):
        r = erlang_c(lam, mu, s)
        v = birth_death(lam, mu, s)
        for k in ("p0", "p_espera", "lq", "wq_min"):
            assert isclose(r[k], v[k], rel_tol=1e-9), (s, k, r[k], v[k])
        r["fijo"] = fijo_unit * s
        r["espera"] = c["costo_espera_h"] * r["lq"] * horas_mes
        r["total"] = r["fijo"] + r["espera"]
        # el cálculo con Lq redondeado a 4 decimales da el mismo monto al sol
        assert round(c["costo_espera_h"] * round(r["lq"], 4) * horas_mes) \
            == round(r["espera"])
        out[s] = r
    a, b = out[c["s_actual"]], out[c["s_propuesta"]]
    # los importes redondeados al sol deben sumar bien
    assert round(a["fijo"]) + round(a["espera"]) == round(a["total"])
    assert round(b["fijo"]) + round(b["espera"]) == round(b["total"])
    out["ahorro"] = round(a["total"]) - round(b["total"])
    out["caida_espera"] = round(a["espera"]) - round(b["espera"])
    out["alza_fijo"] = round(b["fijo"]) - round(a["fijo"])
    assert out["ahorro"] == out["caida_espera"] - out["alza_fijo"]
    # variaciones % con los valores que muestra el cuadro (2 decimales en Wq, 4 en Lq,
    # soles enteros) y comprobación contra los valores sin redondear
    out["pct_wq"] = pct_ok(round(a["wq_min"], 2), round(b["wq_min"], 2),
                           a["wq_min"], b["wq_min"], 1)
    out["pct_lq"] = pct_ok(round(a["lq"], 4), round(b["lq"], 4), a["lq"], b["lq"], 1)
    out["pct_fijo"] = pct_ok(round(a["fijo"]), round(b["fijo"]), a["fijo"], b["fijo"], 1)
    out["pct_espera"] = pct_ok(round(a["espera"]), round(b["espera"]),
                               a["espera"], b["espera"], 1)
    out["pct_total"] = pct_ok(round(a["total"]), round(b["total"]),
                              a["total"], b["total"], 1)
    # cuánto se pasa / sobra respecto de la meta de espera (base = la meta)
    meta = c["wq_max_min"]
    out["pct_exceso_actual"] = pct_ok(meta, round(a["wq_min"], 2), meta, a["wq_min"], 0)
    out["pct_holgura_prop"] = pct_ok(meta, round(b["wq_min"], 2), meta, b["wq_min"], 0)
    # utilización y probabilidad de espera expresadas en %
    for k, x in ((c["s_actual"], a), (c["s_propuesta"], b)):
        x["rho_pct"] = round(x["rho"] * 100, 1)
        x["pw_pct"] = round(x["p_espera"] * 100, 1)
    # peso de cada componente en el costo total (base = costo total de cada propuesta)
    for x in (a, b):
        x["peso_fijo"] = round(round(x["fijo"]) / round(x["total"]) * 100, 1)
        x["peso_espera"] = round(round(x["espera"]) / round(x["total"]) * 100, 1)
        assert round(x["peso_fijo"] + x["peso_espera"], 1) == 100.0
        assert round(round(x["fijo"]) / round(x["total"]) * 100, 1) == \
            round(x["fijo"] / x["total"] * 100, 1)
    # ¿tiene sentido parar en 5? el sexto operador ya no compensa
    c6 = out[c["s_propuesta"] + 1]
    assert c6["total"] > b["total"]
    assert a["wq_min"] > c["wq_max_min"] >= b["wq_min"]
    return out


# --------------------------------------------------------------------------
# Caso 2 — Árbol de decisión de un nivel (Restaurante Sabores del Sur)
# --------------------------------------------------------------------------
C2 = dict(
    p_alta=0.45,
    trad=dict(costo=60_000, ing_alta=130_000, ing_est=100_000),
    veg=dict(costo=95_000, ing_alta=170_000, caida=0.35),
)


def caso2():
    c = C2
    p, q = c["p_alta"], 1 - c["p_alta"]
    t, v = c["trad"], c["veg"]
    ing_est_veg = v["ing_alta"] * (1 - v["caida"])
    pay = dict(
        trad_alta=t["ing_alta"] - t["costo"],
        trad_est=t["ing_est"] - t["costo"],
        veg_alta=v["ing_alta"] - v["costo"],
        veg_est=ing_est_veg - v["costo"],
    )
    ve_t = p * pay["trad_alta"] + q * pay["trad_est"]
    ve_v = p * pay["veg_alta"] + q * pay["veg_est"]
    # verificación: VE = E[ingreso] − costo
    assert isclose(ve_t, p * t["ing_alta"] + q * t["ing_est"] - t["costo"])
    assert isclose(ve_v, p * v["ing_alta"] + q * ing_est_veg - v["costo"])
    # punto de equilibrio de la probabilidad de alta demanda
    p_eq = (pay["trad_est"] - pay["veg_est"]) / (
        (pay["veg_alta"] - pay["veg_est"]) - (pay["trad_alta"] - pay["trad_est"]))
    assert isclose(p_eq * pay["trad_alta"] + (1 - p_eq) * pay["trad_est"],
                   p_eq * pay["veg_alta"] + (1 - p_eq) * pay["veg_est"])
    dif = ve_t - ve_v
    pc = dict(
        dif_sobre_veg=pct_ok(ve_v, ve_t, ve_v, ve_t, 1),       # base: la alternativa descartada
        dif_sobre_trad=round(dif / ve_t * 100, 1),              # base: la alternativa elegida
        fav=pct_ok(pay["trad_alta"], pay["veg_alta"], pay["trad_alta"], pay["veg_alta"], 1),
        des=pct_ok(pay["trad_est"], pay["veg_est"], pay["trad_est"], pay["veg_est"], 1),
        caida_monto=v["ing_alta"] * v["caida"],
        p_eq=round(p_eq * 100, 1),
    )
    assert isclose(ing_est_veg, v["ing_alta"] - pc["caida_monto"])
    return dict(p=p, q=q, ing_est_veg=ing_est_veg, pay=pay, ve_trad=ve_t,
                ve_veg=ve_v, dif=dif, p_eq=p_eq, pct=pc)


# --------------------------------------------------------------------------
# Caso 3 — Árbol con recurso, dos niveles (Clínica veterinaria Huellitas)
# --------------------------------------------------------------------------
C3 = dict(
    seguro=140_000, costo_ini=40_000,
    p_alta=0.60, g_alta=240_000,
    p_camp_fav=0.50, u_camp_fav=200_000, u_camp_des=60_000,
    cancelar=-20_000,
)


def caso3():
    c = C3
    p, q = c["p_alta"], 1 - c["p_alta"]
    ve_camp = (c["p_camp_fav"] * c["u_camp_fav"]
               + (1 - c["p_camp_fav"]) * c["u_camp_des"])
    nodo3 = max(ve_camp, c["cancelar"])
    ve_bruto = p * c["g_alta"] + q * nodo3
    ve_neto = ve_bruto - c["costo_ini"]
    mejor = max(ve_neto, c["seguro"])
    # verificación por estrategias completas (resultado neto en cada hoja)
    ci = c["costo_ini"]
    hojas_camp = [
        (p, c["g_alta"] - ci),
        (q * c["p_camp_fav"], c["u_camp_fav"] - ci),
        (q * (1 - c["p_camp_fav"]), c["u_camp_des"] - ci),
    ]
    hojas_canc = [(p, c["g_alta"] - ci), (q, c["cancelar"] - ci)]
    e2 = sum(w * x for w, x in hojas_camp)
    e3 = sum(w * x for w, x in hojas_canc)
    assert isclose(sum(w for w, _ in hojas_camp), 1)
    assert isclose(e2, ve_neto)
    prob_menor = sum(w for w, x in hojas_camp if x < c["seguro"])
    pc = dict(
        e2_vs_e1=pct_ok(c["seguro"], ve_neto, c["seguro"], ve_neto, 1),
        e3_vs_e1=pct_ok(c["seguro"], e3, c["seguro"], e3, 1),
        aporte_recurso=ve_neto - e3,
        aporte_rel=pct_ok(e3, ve_neto, e3, ve_neto, 1),
        p_hojas=[round(w * 100) for w, _ in hojas_camp],
    )
    assert sum(pc["p_hojas"]) == 100
    return dict(ve_camp=ve_camp, nodo3=nodo3, ve_bruto=ve_bruto,
                ve_neto=ve_neto, mejor=mejor, e1=c["seguro"], e2=e2, e3=e3,
                dif=ve_neto - c["seguro"], hojas_camp=hojas_camp,
                prob_menor=prob_menor, pct=pc)


if __name__ == "__main__":
    r1, r2, r3 = caso1(), caso2(), caso3()
    print("CASO 1"); [print(" ", k, v) for k, v in r1.items()]
    print("CASO 2"); [print(" ", k, v) for k, v in r2.items()]
    print("CASO 3"); [print(" ", k, v) for k, v in r3.items()]
    print("\nTodas las verificaciones cruzadas pasaron.")
