"""Serie B de modelos de sustentación (Semana 7): 3 casos nuevos.

Fase 1 (esta versión): hoja del ESTUDIANTE, sin soluciones.
Los números salen de calculos_b.py (verificados con un segundo método).
Uso:  python generar_b.py
"""
from pathlib import Path

from fractions import Fraction
from math import factorial

import calculos as C0
import calculos_b as B
import figuras_b as FB
from generar_modelos import AQUI, FIG, SALIDA, Modelo, num, pct, s

def cifra(x, dec):
    return f"{x:.{dec}f}"


def pasos_erlang(a_, s_):
    """Textos paso a paso de P0, P(espera), Lq y Wq para s servidores (a_ = λ/μ)."""
    rho = a_ / s_
    terms = [a_**n / factorial(n) for n in range(s_)]
    ult = a_**s_ / (factorial(s_) * (1 - rho))
    suma = sum(terms) + ult
    p0 = 1 / suma
    pw = ult * p0
    ratio = rho / (1 - rho)
    lq = pw * ratio
    return dict(rho=rho, terms=terms, ult=ult, suma=suma, p0=p0, pw=pw, ratio=ratio, lq=lq)


SUBTITULO = "Semana 7 · Serie B · Teoría de colas y Teoría de decisión"


def caso1(m):
    c = B.B1
    r = B.caso1()
    hm = r["horas_mes"]
    m.caso(1, "Atención en ventanillas de CAJA RURAL SOL DEL NORTE", "Teoría de colas")
    m.enunciado("CAJA RURAL SOL DEL NORTE es una entidad financiera peruana que atiende a sus "
                "clientes en las ventanillas de una de sus agencias. Cuando un cliente llega, se "
                "incorpora a una fila única hasta que un cajero esté disponible. A un cajero le "
                f"toma, en promedio, {c['servicio_min']} minutos atender a un cliente, con "
                "tiempos que se ajustan a una distribución exponencial. Asimismo, se ha "
                f"estimado que en promedio llegan a la agencia {c['clientes']} clientes cada "
                f"{c['cada_min']} minutos, siguiendo una distribución de Poisson.")
    m.enunciado("Los cajeros trabajan un solo turno diario de 8:00 a. m. a 4:00 p. m., de lunes "
                f"a sábado, {c['sem_mes']} semanas al mes, y tienen una remuneración de "
                f"{c['sueldo_dia']} soles diarios. Los costos del sistema de caja (terminal y "
                f"licencias) son de {c['sistema_sem']} soles semanales por cajero. Asimismo, se "
                "estima que por cada cliente que permanece en la fila se incurre en un costo de "
                f"oportunidad de {c['costo_espera_h']} soles por hora.")
    m.enunciado("Actualmente, la entidad trabaja con el número mínimo de cajeros que le garantiza "
                "poder atender a todos los clientes que llegan; sin embargo, en las últimas "
                "semanas ha recibido numerosos reclamos por las largas filas, por lo que se "
                "desea evaluar la conveniencia de contratar a un cajero adicional. Esta "
                "propuesta debe estar sustentada en lo siguiente:")
    m.vineta(f"El cliente no debe esperar en la fila más de {c['wq_max_min']} minutos por la "
             "atención del cajero.")
    m.vineta("El costo total del servicio debe ser menor.")
    m.enunciado("Las tasas de llegada y de atención deben expresarse en clientes/hora.",
                italica=True)

    sa, sp = c["s_actual"], c["s_propuesta"]
    a, b = r[sa], r[sp]
    s6 = r[sp + 1]
    lam, mu = int(r["lam"]), int(r["mu"])
    m.pregunta("¿Cuál es la situación problemática? (Debe incluir el problema a resolver, las "
               "distintas propuestas y el objetivo)", "INTERPRETACIÓN")
    m.respuesta("El problema es que CAJA RURAL SOL DEL NORTE atiende a sus clientes en las "
                "ventanillas de una agencia con cajeros y, en las últimas semanas, los clientes "
                "esperan en la fila más de lo razonable, lo que genera reclamos. Hay que decidir "
                f"entre dos propuestas: (1) mantener el esquema actual de {sa} cajeros, o (2) "
                f"ampliar a {sp} cajeros. El objetivo común es elegir la propuesta que cumpla la "
                f"meta de servicio (espera máxima de {c['wq_max_min']} minutos en la fila) al "
                "menor costo mensual posible.")
    m.por_que("La interpretación exige traducir el relato a un problema formal de decisión: "
              f"primero se nombran las alternativas concretas que se van a comparar ({sa} vs. "
              f"{sp} cajeros), porque sin alternativas explícitas no hay nada que calcular "
              "después; luego se fija el objetivo común (cumplir la meta de espera al menor "
              "costo) porque ese objetivo es el que finalmente decide cuál propuesta gana en la "
              "pregunta de análisis.")
    m.pregunta("¿Cómo representaría los modelos a comparar y las metas que debe alcanzar?",
               "REPRESENTACIÓN")
    m.respuesta("El sistema corresponde a un modelo de colas M/M/s (notación de Kendall): "
                "llegadas Poisson (M), tiempos de servicio exponenciales (M) y s servidores en "
                "paralelo (los cajeros), con capacidad y población infinitas y disciplina FIFO "
                "(una sola fila). Los parámetros son "
                f"λ = {lam} clientes/hora ({c['clientes']} cada {c['cada_min']} minutos) y "
                f"μ = {mu} clientes/hora por cajero (1 atención cada {c['servicio_min']} minutos), "
                f"con s = {sa} (actual) y s = {sp} (propuesta). El sistema es estable porque "
                f"ρ = λ/(s·μ) < 1; además, s = {sa} es el mínimo posible, ya que λ/μ = "
                f"{r['lam']/r['mu']:.1f} y se necesita s > {r['lam']/r['mu']:.1f}. Las metas se "
                "expresan como dos medidas de rendimiento: el tiempo promedio de espera en cola "
                f"Wq (debe ser ≤ {c['wq_max_min']} min = {c['wq_max_min']/60:.2f} h) y el costo "
                "total mensual CT (debe ser menor en la propuesta).")
    m.por_que("Se usa la notación de Kendall porque dejar explícitos M/M/s obliga a verificar que "
              "se cumplen los supuestos (Poisson y exponencial) que habilitan las fórmulas de "
              "colas que se usarán en el siguiente paso; y las metas se expresan como medidas de "
              "rendimiento (Wq, CT) porque son exactamente lo que se va a calcular y comparar, no "
              "conceptos abstractos.")
    m.pregunta("¿Qué cálculos debe obtener para evaluar las metas? (Debe ser presentado en un "
               "cuadro y presentar un gráfico que explique el comportamiento de los costos)",
               "CÁLCULO", espacio=8)
    m.respuesta("Se calcula el sistema M/M/s con la fórmula de Erlang C para s = "
                f"{sa} y s = {sp}, y se convierte cada resultado a un costo mensual. "
                "Desarrollo paso a paso:")
    m.linea(f"Paso 1 — Tasas en clientes/hora: λ = {c['clientes']} ÷ {c['cada_min']} × 60 = "
            f"{lam} clientes/hora;  μ = 60 ÷ {c['servicio_min']} = {mu} clientes/hora por cajero.",
            color=None)
    m.linea(f"Paso 2 — Número mínimo de cajeros: λ/μ = {lam} ÷ {mu} = {r['lam']/r['mu']:.1f}; "
            f"como s·μ debe superar a λ, s > {r['lam']/r['mu']:.1f}, luego el mínimo es s = {sa} "
            "(la situación actual).", color=None)
    m.linea("Paso 3 — Utilización: ρ = λ / (s·μ).", color=None)
    for s_ in (sa, sp):
        fr = Fraction(lam, s_ * mu)
        m.linea(f"s = {s_}:  ρ = {lam} ÷ ({s_} × {mu}) = {lam} ÷ {s_*mu} = {fr} = "
                f"{lam/(s_*mu):.4f} ≈ {lam/(s_*mu):.3f}")
    a_ = r["lam"] / r["mu"]
    m.linea("Paso 4 — Probabilidad de sistema vacío (Erlang C), con a = λ/μ = "
            f"{a_:.1f}:   P0 = 1 ÷ [ Σ (aⁿ/n!) para n = 0 hasta s−1  +  aˢ / (s!·(1 − ρ)) ]",
            color=None)
    pe = {}
    for s_ in (sa, sp):
        e = pasos_erlang(a_, s_)
        pe[s_] = e
        assert round(e["p0"], 4) == round(r[s_]["p0"], 4)
        assert round(e["pw"], 4) == round(r[s_]["p_espera"], 4)
        assert round(e["lq"], 4) == round(r[s_]["lq"], 4)
        ts = " + ".join(cifra(t, 4) for t in e["terms"])
        m.linea(f"s = {s_}:  suma de n = 0 a {s_-1}: {ts} = {cifra(sum(e['terms']), 4)};  "
                f"aˢ/(s!·(1−ρ)) = {a_:.1f}^{s_} ÷ ({s_}! × {1 - Fraction(lam, s_ * mu)}) = "
                f"{cifra(e['ult'], 4)};  P0 = 1 ÷ ({cifra(sum(e['terms']), 4)} + "
                f"{cifra(e['ult'], 4)}) = 1 ÷ {cifra(e['suma'], 4)} = {cifra(e['p0'], 4)}")
    m.linea("Paso 5 — Probabilidad de esperar (Erlang C):  P(espera) = [aˢ / (s!·(1 − ρ))] × P0",
            color=None)
    for s_ in (sa, sp):
        e = pe[s_]
        m.linea(f"s = {s_}:  P(espera) = {cifra(e['ult'], 4)} × {cifra(e['p0'], 4)} ≈ "
                f"{cifra(e['pw'], 4)} ≈ {cifra(e['pw'], 3)}")
    m.linea("Paso 6 — Clientes en espera:  Lq = P(espera) × ρ / (1 − ρ).", color=None)
    for s_ in (sa, sp):
        e = pe[s_]
        fr = Fraction(lam, s_ * mu)
        m.linea(f"s = {s_}:  ρ/(1−ρ) = {fr} ÷ {1 - fr} = {fr / (1 - fr)} = "
                f"{cifra(e['ratio'], 4)};  Lq = {cifra(e['pw'], 4)} × {cifra(e['ratio'], 4)} ≈ "
                f"{cifra(e['lq'], 4)} clientes")
    m.linea("Paso 7 — Tiempo de espera en cola:  Wq = Lq ÷ λ (en horas) y se multiplica por 60 "
            "para pasar a minutos.", color=None)
    for s_ in (sa, sp):
        e = pe[s_]
        m.linea(f"s = {s_}:  Wq = {cifra(e['lq'], 4)} ÷ {lam} = {cifra(e['lq']/lam, 4)} h  →  "
                f"× 60 = {cifra(r[s_]['wq_min'], 2)} minutos")
    m.nota("Se operan los decimales completos; por eso el último decimal puede diferir de "
           "repetir la multiplicación con los valores ya redondeados que se muestran.")
    filas = [["Medida", f"s = {c['s_actual']} (actual)", f"s = {c['s_propuesta']} (propuesta)"],
             ["λ (clientes/hora)", "", ""],
             ["μ por cajero (clientes/hora)", "", ""],
             ["ρ = λ / (s·μ)", "", ""],
             ["P0 (prob. sistema vacío)", "", ""],
             ["P(espera) – Erlang C", "", ""],
             ["Wq (minutos)", "", ""],
             ["Lq (clientes en espera)", "", ""],
             ["Costo fijo mensual (planilla + sistema)", "", ""],
             [f"Costo de espera mensual ({c['costo_espera_h']} soles/h × Lq × {hm} h/mes)",
              "", ""],
             ["Costo total mensual", "", ""]]
    if m.docente:
        filas[1] = ["λ (clientes/hora)", f"{lam}", f"{lam}"]
        filas[2] = ["μ por cajero (clientes/hora)", f"{mu}", f"{mu}"]
        filas[3] = ["ρ = λ / (s·μ)", f"{a['rho']:.3f}", f"{b['rho']:.3f}"]
        filas[4] = ["P0 (prob. sistema vacío)", f"{a['p0']:.4f}", f"{b['p0']:.4f}"]
        filas[5] = ["P(espera) – Erlang C", f"{a['p_espera']:.3f}", f"{b['p_espera']:.3f}"]
        filas[6] = ["Wq (minutos)", f"{a['wq_min']:.2f}  (> {c['wq_max_min']} min: no cumple)",
                    f"{b['wq_min']:.2f}  (≤ {c['wq_max_min']} min: cumple)"]
        filas[7] = ["Lq (clientes en espera)", f"{a['lq']:.4f}", f"{b['lq']:.4f}"]
        filas[8][1:] = [s(a["fijo"]), s(b["fijo"])]
        filas[9][1:] = [s(a["espera"]), s(b["espera"])]
        filas[10][1:] = [s(a["total"]), s(b["total"])]
    m.tabla(filas, [3489, 3489, 3489])
    d_, w_, sw, sis, hm_ = c["dias_sem"], c["sem_mes"], c["sueldo_dia"], c["sistema_sem"], hm
    m.linea("Paso 8 — Costos mensuales.", color=None)
    m.linea(f"Costo fijo por cajero = {sw} × {d_*w_} días (planilla: {d_} días × {w_} semanas) + "
            f"{sis} × {w_} semanas (sistema) = {sw*d_*w_:,} + {sis*w_:,} = {s(r['fijo_unit'])}; "
            "se multiplica por s.")
    for s_ in (sa, sp):
        x = r[s_]
        m.linea(f"s = {s_}:  costo fijo = {r['fijo_unit']:,} × {s_} = {s(x['fijo'])};  "
                f"costo de espera = {c['costo_espera_h']} × Lq × {hm_} h = {c['costo_espera_h']} × "
                f"{x['lq']:.4f} × {hm_} = {s(x['espera'])};  costo total = {x['fijo']:,.0f} + "
                f"{round(x['espera']):,} = {s(x['total'])}")
    m.nota(f"Las {hm_} horas del mes salen de {c['horas_dia']} h × {d_} días × {w_} semanas. Lq "
           "(= λ·Wq) es el número promedio de clientes esperando en un instante cualquiera, y "
           f"cada uno cuesta {c['costo_espera_h']} soles por hora. Los montos se calculan con Lq "
           "sin redondear y se muestran redondeados al sol.")
    ma, mb = round(a["wq_min"], 2), round(b["wq_min"], 2)
    la, lb = round(a["lq"], 4), round(b["lq"], 4)
    fa, fb = round(a["fijo"]), round(b["fijo"])
    ea, eb = round(a["espera"]), round(b["espera"])
    ta, tb = round(a["total"]), round(b["total"])
    meta = c["wq_max_min"]
    m.texto("Cómo se calcula el porcentaje (variación relativa). Paso 1: se toma como base el "
            f"valor actual (s = {sa}), porque es la situación con la que se compara. Paso 2: se "
            "resta valor propuesta − valor actual (si da negativo la medida baja; si da "
            "positivo, sube). Paso 3: esa diferencia se divide entre la base y se multiplica por "
            "100:")
    m.linea("Variación % = (valor propuesta − valor actual) ÷ valor actual × 100")
    var = lambda a_, b_, d: (f"({num(b_, d)} − {num(a_, d)}) ÷ {num(a_, d)} × 100 = "
                             f"{num(b_ - a_, d)} ÷ {num(a_, d)} × 100")
    if m.docente:
        filas_p = [["Medida", "Cálculo con los valores del cuadro", "Resultado"],
                   ["Wq (min)", var(ma, mb, 2), pct(r["pct_wq"], signo=True)],
                   ["Lq (clientes)", var(la, lb, 4), pct(r["pct_lq"], signo=True)],
                   ["Costo fijo mensual", var(fa, fb, 0), pct(r["pct_fijo"], signo=True)],
                   ["Costo de espera mensual", var(ea, eb, 0), pct(r["pct_espera"], signo=True)],
                   ["Costo total mensual", var(ta, tb, 0), pct(r["pct_total"], signo=True)]]
        m.tabla(filas_p, [2400, 5800, 2267])
    m.texto("Porcentajes respecto de la meta de espera (aquí la base es la meta de "
            f"{meta} minutos, no el valor actual): con s = {sa}, "
            f"({num(ma, 2)} − {meta}) ÷ {meta} × 100 = {num(ma - meta, 2)} ÷ {meta} × 100 ≈ "
            f"{pct(r['pct_exceso_actual'], 0, True)}, es decir, se pasa de la meta en "
            f"{num(ma - meta, 2)} minutos; con s = {sp}, "
            f"({num(mb, 2)} − {meta}) ÷ {meta} × 100 = {num(mb - meta, 2)} ÷ {meta} × 100 ≈ "
            f"{pct(r['pct_holgura_prop'], 0)}, es decir, queda {pct(-r['pct_holgura_prop'], 0)} "
            "por debajo del máximo permitido.")
    m.texto("Magnitudes que ya son porcentajes: utilización de los cajeros = ρ × 100 → "
            f"s = {sa}: {a['rho']:.3f} × 100 = {a['rho_pct']:.1f}%; "
            f"s = {sp}: {b['rho']:.3f} × 100 = {b['rho_pct']:.1f}%. Probabilidad de tener que "
            f"esperar = P(espera) × 100 → s = {sa}: {a['p_espera']:.3f} × 100 = "
            f"{a['pw_pct']:.1f}%; s = {sp}: {b['p_espera']:.3f} × 100 = {b['pw_pct']:.1f}%.")
    m.texto("Peso de cada componente en el costo total = componente ÷ costo total × 100 "
            f"(la base es el costo total de cada propuesta): s = {sa}: costo fijo "
            f"{num(fa)} ÷ {num(ta)} × 100 = {a['peso_fijo']:.1f}% y costo de espera "
            f"{num(ea)} ÷ {num(ta)} × 100 = {a['peso_espera']:.1f}%; s = {sp}: "
            f"costo fijo {num(fb)} ÷ {num(tb)} × 100 = {b['peso_fijo']:.1f}% y costo de espera "
            f"{num(eb)} ÷ {num(tb)} × 100 = {b['peso_espera']:.1f}%.")
    m.nota("Observaciones: (1) los porcentajes se calcularon con los valores que muestra el "
           "cuadro; con los valores sin redondear se obtiene el mismo resultado al decimal "
           f"indicado. (2) El porcentaje depende de la base: el costo fijo sube {pct(r['pct_fijo'])}"
           f" respecto de s = {sa}, pero volver de s = {sp} a s = {sa} lo bajaría solo "
           f"{pct(-C0.var_pct(fb, fa))}. (3) No confundir porcentaje con puntos porcentuales: ρ "
           f"pasa de {a['rho_pct']:.1f}% a {b['rho_pct']:.1f}%, es decir, "
           f"{num(b['rho_pct'] - a['rho_pct'], 1)} puntos porcentuales, que equivalen a una "
           f"variación relativa de ({b['rho_pct']:.1f} − {a['rho_pct']:.1f}) ÷ {a['rho_pct']:.1f}"
           f" × 100 = {pct((b['rho_pct'] - a['rho_pct']) / a['rho_pct'] * 100)}.")
    m.imagen("b_caso1_costos.png", 5219700, 3103245)
    m.por_que("Wq y Lq se calculan con Erlang C —y no con fórmulas de M/M/1— porque hay varios "
              "servidores atendiendo en paralelo la misma fila única; usar M/M/1 aquí "
              "subestimaría la espera real. El costo se separa en “fijo” y “de espera” porque "
              "son las dos fuerzas que se mueven en direcciones opuestas al agregar un cajero "
              "(el fijo sube, el de espera baja), y solo mostrando ambas por separado se puede "
              "argumentar después cuál efecto domina; el gráfico hace visible esa compensación de "
              "un vistazo, que es justamente lo que pide la pregunta.")
    m.pregunta("¿Qué propuesta es la mejor? Realice una discusión de resultados para argumentar "
               "su decisión.", "ANÁLISIS Y ARGUMENTACIÓN")
    exceso = a["wq_min"] - c["wq_max_min"]
    m.respuesta(f"La mejor propuesta es contratar al cuarto cajero (s = {sp}). Cumple las dos "
                f"condiciones planteadas: el tiempo de espera baja de {a['wq_min']:.2f} a "
                f"{b['wq_min']:.2f} minutos (con s = {sa} se excede la meta en {exceso:.2f} "
                f"minutos, ≈{r['pct_exceso_actual']:.0f}% por encima de los {meta} minutos "
                f"exigidos; con s = {sp} se cumple con holgura), y el costo total mensual baja de "
                f"{s(a['total'])} a {s(b['total'])}, es decir, un ahorro de {s(r['ahorro'])} al "
                f"mes ({pct(-r['pct_total'])}). El ahorro ocurre porque, aunque el costo fijo "
                f"sube en {s(r['alza_fijo'])} ({pct(r['pct_fijo'])}) al pasar de {sa} a {sp} "
                f"cajeros, el costo de oportunidad por las horas de espera de los clientes cae en "
                f"{s(r['caida_espera'])} ({pct(-r['pct_espera'])}), una reducción más de tres "
                f"veces mayor que el aumento del costo fijo. Además, no conviene ir más allá: con "
                f"un quinto cajero el costo total ({s(s6['total'])}) volvería a superar al de "
                f"s = {sp} ({s(b['total'])}).")
    m.por_que("La discusión no puede quedarse en “cumple la meta de tiempo” ni en “es más barato” "
              "por separado: hay que mostrar que ambas metas se cumplen a la vez y explicar el "
              "mecanismo económico (qué sube y qué baja, y por qué lo que baja pesa más) porque "
              "eso es lo que distingue una recomendación argumentada de una simple lectura de la "
              "tabla.")


def caso2(m):
    c = B.B2
    cv, og = c["conv"], c["org"]
    q = 1 - c["p_alto"]
    r = B.caso2(); p = r["pay"]; pc = r["pct"]
    pa, pe_, oa, oe = p["conv_alto"], p["conv_est"], p["org_alto"], p["org_est"]
    m.doc.vacio()
    m.caso(2, "Decisión de certificación orgánica en la finca cafetalera “La Selva Alta”",
           "Teoría de decisión – valor esperado, un nivel")
    m.enunciado("Carmen Huamán, dueña de la finca cafetalera “La Selva Alta”, debe decidir cómo "
                "orientar su producción para la próxima campaña: mantener únicamente su café "
                "convencional o certificar una parcela como café orgánico de especialidad, con "
                "el objetivo de maximizar su utilidad neta. El resultado dependerá del precio de "
                "mercado, que se prevé en dos escenarios: precio alto por demanda de cafés "
                "especiales o precio estándar.")
    m.enunciado(f"Si opta por mantener solo el café convencional, sus costos serán de "
                f"{s(cv['costo'])}; si el precio es alto obtendría ingresos por "
                f"{s(cv['ing_alto'])}, mientras que si el precio es estándar obtendría ingresos "
                f"por {s(cv['ing_est'])}.")
    m.enunciado(f"Si opta por certificar el café orgánico, sus costos serán de {s(og['costo'])}; "
                f"si el precio es alto obtendría ingresos por {s(og['ing_alto'])}, mientras que "
                f"si el precio es estándar, dichos ingresos se reducirían en un "
                f"{og['caida']*100:.0f}%. Además, ha estimado que la probabilidad de un precio "
                f"alto es de {c['p_alto']:.2f}.")

    # ---- interpretación
    m.pregunta("¿Cuál es la situación problemática, qué problema hay que resolver y con qué "
               "finalidad?", "INTERPRETACIÓN")
    m.respuesta("Carmen debe decidir entre dos alternativas de producción para la finca: "
                "mantener solo el café convencional o certificar una parcela como café orgánico "
                "de especialidad. El problema por resolver es cuál de las dos alternativas "
                "conviene bajo la incertidumbre del precio de mercado (precio alto o precio "
                "estándar), y la finalidad es maximizar la utilidad neta esperada.")
    m.por_que("Antes de calcular cualquier valor esperado hay que dejar claro qué se está "
              "decidiendo (dos alternativas mutuamente excluyentes) y bajo qué incertidumbre (dos "
              "estados del precio con una probabilidad dada); si no se nombra el criterio de "
              "decisión (maximizar la utilidad esperada) no queda claro qué herramienta aplicar "
              "después.")

    # ---- representación y cálculo
    m.pregunta("¿Qué herramienta se utilizaría para resolver el problema? Presente los "
               "elementos, muestre el desarrollo de los cálculos necesarios para hallar los "
               "pagos y aplicar el criterio del valor esperado.", "REPRESENTACIÓN y CÁLCULO",
               espacio=12)
    m.respuesta("Se utiliza un árbol de decisión de un nivel: un nodo de decisión del que salen "
                "las dos alternativas, cada una con un nodo de azar con dos estados de la "
                "naturaleza. Desarrollo paso a paso:")
    m.linea(f"Paso 1 — Ingreso del café orgánico con precio estándar: la reducción del "
            f"{og['caida']*100:.0f}% es {og['caida']:.2f} × {og['ing_alto']:,} = "
            f"{pc['caida_monto']:,.0f}; ingreso = {og['ing_alto']:,} − {pc['caida_monto']:,.0f} = "
            f"{r['ing_est_org']:,.0f} (equivale a {og['ing_alto']:,} × {1-og['caida']:.2f}).",
            color=None)
    m.linea("Paso 2 — Pago (utilidad) = ingreso − costo en cada rama:", color=None)
    m.linea(f"Convencional, precio alto: {cv['ing_alto']:,} − {cv['costo']:,} = {s(pa)}")
    m.linea(f"Convencional, precio estándar: {cv['ing_est']:,} − {cv['costo']:,} = {s(pe_)}")
    m.linea(f"Orgánico, precio alto: {og['ing_alto']:,} − {og['costo']:,} = {s(oa)}")
    m.linea(f"Orgánico, precio estándar: {r['ing_est_org']:,.0f} − {og['costo']:,} = {s(oe)}")
    if m.docente:
        filas = [["Alternativa", "Escenario", "Ingreso", "Costo", "Pago (utilidad)"],
                 ["Café convencional", f"Precio alto (P = {c['p_alto']:.2f})",
                  s(cv["ing_alto"]), s(cv["costo"]), s(pa)],
                 ["Café convencional", f"Precio estándar (P = {q:.2f})",
                  s(cv["ing_est"]), s(cv["costo"]), s(pe_)],
                 ["Café orgánico", f"Precio alto (P = {c['p_alto']:.2f})",
                  s(og["ing_alto"]), s(og["costo"]), s(oa)],
                 ["Café orgánico", f"Precio estándar (P = {q:.2f}) *",
                  s(r["ing_est_org"]), s(og["costo"]), s(oe)]]
    else:
        filas = [["Alternativa", "Escenario", "Ingreso", "Costo", "Pago (utilidad)"],
                 ["Café convencional", f"Precio alto (P = {c['p_alto']:.2f})", "", "", ""],
                 ["Café convencional", f"Precio estándar (P = {q:.2f})", "", "", ""],
                 ["Café orgánico", f"Precio alto (P = {c['p_alto']:.2f})", "", "", ""],
                 ["Café orgánico", f"Precio estándar (P = {q:.2f})", "", "", ""]]
    m.tabla(filas, [2013, 1988, 1955, 1916, 1983])
    m.nota(f"* Ingreso del café orgánico con precio estándar = {s(og['ing_alto'])} × "
           f"(1 − {og['caida']:.2f}) = {s(r['ing_est_org'])} (los ingresos se reducen "
           f"{og['caida']*100:.0f}% respecto del escenario de precio alto).")
    m.imagen("b_caso2_arbol.png", 5303520, 3337173)
    m.texto("Paso 3 — Con los pagos ya calculados se aplica el criterio del valor esperado en "
            "cada nodo de azar (VE = Σ probabilidad × pago):")
    m.linea(f"VE(Café convencional) = {c['p_alto']:.2f}({pa:,}) + {q:.2f}({pe_:,}) = "
            f"{c['p_alto']*pa:,.0f} + {q*pe_:,.0f} = {s(r['ve_conv'])}")
    m.linea(f"VE(Café orgánico) = {c['p_alto']:.2f}({oa:,}) + {q:.2f}({oe:,.0f}) = "
            f"{c['p_alto']*oa:,.0f} + {q*oe:,.0f} = {s(r['ve_org'])}")
    m.linea(f"Paso 4 — Decisión en el nodo 1: se elige la alternativa de mayor VE → café "
            f"orgánico ({s(r['ve_org'])} > {s(r['ve_conv'])}).", color=None)
    m.por_que("El pago de cada rama se calcula como ingreso menos costo —y no solo el ingreso— "
              "porque lo que Carmen maximiza es utilidad neta, según el propio objetivo planteado "
              "en la interpretación; y el valor esperado se calcula por separado para cada "
              "alternativa (y no un promedio global) porque cada alternativa tiene su propio par "
              "de pagos y debe compararse como un todo frente a la otra.")

    # ---- análisis
    m.pregunta("¿Cuál es la mejor decisión? Realice una discusión de resultados para argumentar "
               "su elección.", "ANÁLISIS Y ARGUMENTACIÓN")
    m.respuesta("La mejor decisión es certificar el café orgánico, porque su valor esperado "
                f"({s(r['ve_org'])}) es mayor que el de mantener solo el convencional "
                f"({s(r['ve_conv'])}), una diferencia de {s(r['dif'])} a favor del orgánico "
                f"({pct(pc['dif_sobre_conv'])} más que el convencional). En el escenario "
                f"favorable (precio alto) el orgánico supera al convencional en {s(oa - pa)} "
                f"({s(oa)} frente a {s(pa)}), mientras que en el desfavorable (precio estándar) "
                f"rinde {s(pe_ - oe)} menos ({s(oe)} frente a {s(pe_)}). La decisión es sensible "
                f"a la probabilidad: el orgánico solo es preferible si la probabilidad de precio "
                f"alto supera {r['p_eq']:.2f}; con {c['p_alto']:.2f} se cumple, pero con un "
                "margen moderado.")
    m.por_que(f"No basta con decir “se elige la de mayor valor esperado”: hay que mostrar cuánto "
              f"mayor es ({s(r['dif'])}) para que la recomendación sea cuantitativa, y conviene "
              "revisar también ambos escenarios para ver por qué el promedio favorece a una "
              "alternativa: aquí la ganancia adicional en el escenario bueno es grande y la "
              "pérdida en el malo también, y el promedio inclina la balanza porque el escenario "
              "bueno es el más probable. El punto de equilibrio de la probabilidad indica qué tan "
              "sensible es la decisión a la estimación de Carmen.")
    m.texto("Detalle de cómo se calculan los porcentajes (siempre hay que decir cuál es la "
            "base):")
    m.linea(f"Probabilidades: {c['p_alto']:.2f} = {c['p_alto']*100:.0f}% y {q:.2f} = "
            f"{q*100:.0f}% (se multiplica por 100).")
    m.linea(f"Diferencia de VE con base en el café convencional: ({r['ve_org']:,.0f} − "
            f"{r['ve_conv']:,.0f}) ÷ {r['ve_conv']:,.0f} × 100 = {r['dif']:,.0f} ÷ "
            f"{r['ve_conv']:,.0f} × 100 = {pct(pc['dif_sobre_conv'])} (el orgánico rinde "
            f"{pct(pc['dif_sobre_conv'])} más).")
    m.linea(f"La misma diferencia con base en el café orgánico: {r['dif']:,.0f} ÷ "
            f"{r['ve_org']:,.0f} × 100 = {pct(pc['dif_sobre_org'])} (el convencional rinde "
            f"{pct(pc['dif_sobre_org'])} menos). Son dos porcentajes distintos porque cambia la "
            "base.")
    m.linea(f"Escenario favorable: ({oa:,} − {pa:,}) ÷ {pa:,} × 100 = {oa - pa:,} ÷ {pa:,} × 100 "
            f"= {pct(pc['fav'], signo=True)}")
    m.linea(f"Escenario desfavorable: ({oe:,.0f} − {pe_:,}) ÷ {pe_:,} × 100 = "
            f"{num(oe - pe_)} ÷ {pe_:,} × 100 = {pct(pc['des'])}")
    m.linea(f"Probabilidad de equilibrio p: p({pa:,}) + (1 − p)({pe_:,}) = p({oa:,}) + "
            f"(1 − p)({oe:,.0f})  →  {pe_:,} + {pa - pe_:,}p = {oe:,.0f} + {oa - oe:,.0f}p  →  "
            f"{pe_ - oe:,.0f} = {(oa - oe) - (pa - pe_):,.0f}p  →  p = {r['p_eq']:.4f} = "
            f"{pc['p_eq']:.1f}%.")


def caso3(m):
    c = B.B3
    q = 1 - c["p_alta"]
    r = B.caso3(); pc = r["pct"]
    m.doc.vacio()
    m.caso(3, "Estrategia de expansión de la empresa de transporte “Rutas del Sur”",
           "Teoría de decisión – árbol con recurso, dos niveles")
    m.enunciado("Una empresa de transporte evalúa si continuar operando únicamente con su "
                f"servicio de carga seca, obteniendo una utilidad anual segura de "
                f"{s(c['seguro'])}, o lanzar una nueva línea de transporte refrigerado, para lo "
                "cual deberá asumir costos iniciales de flota y certificaciones por "
                f"{s(c['costo_ini'])}. Las ganancias y pérdidas que se indican a continuación no "
                "incluyen este costo inicial ni la inversión adicional que se menciona más "
                "adelante.")
    m.enunciado(f"Si decide lanzar la nueva línea, existe una probabilidad de "
                f"{c['p_alta']*100:.0f}% de lograr una alta aceptación entre los clientes, "
                f"generando una ganancia de {s(c['g_alta'])}. Sin embargo, existe una "
                f"probabilidad de {q*100:.0f}% de no alcanzar la aceptación esperada, situación "
                "en la que deberá decidir entre reorientar el servicio hacia nuevos clientes, "
                f"lo que requiere una inversión adicional de {s(c['inv_extra'])}, o vender los "
                "camiones refrigerados.")
    m.enunciado(f"Si decide reorientar el servicio, el mercado podría responder "
                f"favorablemente, con una probabilidad de {c['p_fav']*100:.0f}%, generando una "
                f"utilidad de {s(c['u_fav'])}, o desfavorablemente, con una probabilidad de "
                f"{(1-c['p_fav'])*100:.0f}%, generando una utilidad de {s(c['u_des'])}.")
    m.enunciado("Si decide vender los camiones refrigerados, luego de cubrir los gastos de "
                f"traspaso, obtendría un ingreso neto de {s(c['venta'])}.")

    # ---- representación
    m.pregunta("Construya el árbol de decisión con todos sus elementos.", "REPRESENTACIÓN",
               espacio=16)
    m.respuesta("El árbol tiene dos niveles de decisión porque, a diferencia del Caso 2, aquí "
                "una de las ramas de azar desemboca en una segunda decisión (con recurso) en "
                "lugar de terminar directamente en un pago. Elementos: nodo 1 (decisión: "
                "continuar o lanzar), nodo 2 (azar: alta o baja aceptación), nodo 3 (decisión "
                "de recurso: reorientar o vender) y nodo 4 (azar: respuesta favorable o "
                "desfavorable); el costo inicial va sobre la rama “lanzar” y la inversión "
                "adicional sobre la rama “reorientar”:")
    m.imagen("b_caso3_arbol.png", 5852160, 2926080)
    m.por_que("El nodo cuadrado 3 (segunda decisión) se dibuja porque la propia narración dice "
              "“deberá decidir entre reorientar o vender”: eso es, por definición, otro punto de "
              "decisión del dueño del negocio, no un evento del azar, y por eso lleva símbolo de "
              "cuadrado y no de círculo. Se construye de izquierda a derecha en el orden "
              "cronológico real de las decisiones (primero lanzar o no, después —solo si hay "
              "baja aceptación— reorientar o vender) porque así el árbol refleja la información "
              "disponible en cada momento.")

    # ---- cálculo
    m.pregunta("Desarrolle el criterio del valor esperado realizando los cálculos necesarios y "
               "tome la decisión que corresponda en cada nodo.", "CÁLCULO", espacio=12)
    m.respuesta("El árbol se resuelve “de atrás hacia adelante” (roll-back), empezando por el "
                "nodo más a la derecha:")
    f_, d_ = c["p_fav"], 1 - c["p_fav"]
    m.linea("1) Nodo de azar 4 “Reorientar el servicio”:", color=None)
    m.linea(f"VE(reorientar, bruto) = {f_:.2f}({c['u_fav']:,}) + {d_:.2f}({c['u_des']:,}) = "
            f"{f_*c['u_fav']:,.0f} + {d_*c['u_des']:,.0f} = {s(r['ve_reor_bruto'])}")
    m.linea(f"VE(reorientar, neto) = {r['ve_reor_bruto']:,.0f} − {c['inv_extra']:,} (inversión "
            f"adicional) = {s(r['ve_reor'])}")
    m.linea(f"2) Nodo de decisión 3 “baja aceptación”: se compara reorientar ({s(r['ve_reor'])}) "
            f"contra vender ({s(c['venta'])}).", color=None)
    m.linea(f"Se elige “reorientar el servicio” → valor del nodo = {s(r['nodo3'])}  (se descarta "
            f"vender, porque {s(c['venta'])} < {s(r['ve_reor'])})")
    m.linea("3) Nodo de azar 2 “lanzar la línea” (usa el valor ya podado del paso anterior en "
            "la rama de baja aceptación):", color=None)
    m.linea(f"VE(lanzar, bruto) = {c['p_alta']:.2f}({c['g_alta']:,}) + {q:.2f}({r['nodo3']:,.0f}) "
            f"= {c['p_alta']*c['g_alta']:,.0f} + {q*r['nodo3']:,.0f} = {s(r['ve_bruto'])}")
    m.linea(f"VE(lanzar, neto) = {r['ve_bruto']:,.0f} − {c['costo_ini']:,} (costo inicial) = "
            f"{s(r['ve_neto'])}")
    m.linea(f"4) Nodo de decisión raíz 1: se compara lanzar ({s(r['ve_neto'])}) contra continuar "
            f"con carga seca ({s(c['seguro'])}, valor seguro).", color=None)
    m.linea(f"Se elige “continuar con carga seca” → VE = {s(r['mejor'])}")
    m.por_que("El cálculo avanza de derecha a izquierda porque el valor de un nodo de decisión "
              "(como el nodo 3) solo puede conocerse después de saber cuánto vale cada una de sus "
              "ramas, y el valor de la rama “baja aceptación” del nodo 2 solo puede conocerse "
              "después de resolver el nodo 3; hacerlo en el orden inverso obligaría a adivinar el "
              "valor de una rama que aún no se ha calculado. En cada nodo de decisión se elige el "
              "mayor valor esperado (y se “poda” la otra rama). Los dos costos se restan donde "
              "ocurren: la inversión adicional de S/ 30,000 solo se paga si se reorienta, por eso "
              "se resta dentro de esa rama (nodo 4) y antes de comparar con vender; el costo "
              "inicial de S/ 60,000 se paga en cualquier rama de “lanzar”, por eso se resta una "
              "sola vez, después del nodo 2. Restarlo en cada hoja da exactamente el mismo "
              "resultado.")

    # ---- estrategias
    m.pregunta("¿Qué posibles estrategias se pueden seguir a partir del árbol construido?",
               "INTERPRETACIÓN")
    m.respuesta("Del árbol se desprenden tres estrategias completas: (1) continuar solo con la "
                "carga seca (no lanzar la línea refrigerada); (2) lanzar la línea y, si hay baja "
                "aceptación, reorientar el servicio; y (3) lanzar la línea y, si hay baja "
                "aceptación, vender los camiones. No existe una cuarta estrategia “lanzar y no "
                "decidir nada si hay baja aceptación”, porque el propio caso obliga a tomar una "
                "de las dos acciones de recurso en ese punto.")
    m.por_que("En un árbol con recurso, una “estrategia” no es una sola rama sino un plan "
              "contingente completo: qué se hace al inicio y qué se hará después en cada punto de "
              "decisión futuro. Enumerarlas así, antes de comparar valores, evita el error común "
              "de evaluar “lanzar” como si fuera una sola apuesta, cuando en realidad incluye una "
              "decisión de segundo momento que cambia el resultado.")

    # ---- análisis
    m.pregunta("¿Cuál es la mejor estrategia? Sustente su respuesta.", "ANÁLISIS Y ARGUMENTACIÓN")
    ph = pc["p_hojas"]
    m.respuesta("La mejor estrategia es continuar solo con la carga seca. Aunque lanzar la línea "
                f"con recurso a reorientar es la mejor forma de lanzarla ({s(r['ve_reor'])} frente "
                f"a {s(c['venta'])} de vender), su valor esperado neto ({s(r['e2'])}) sigue "
                f"siendo menor que la utilidad segura de continuar ({s(r['e1'])}). La diferencia "
                f"es de {s(r['dif'])} a favor de no lanzar. Comparando las tres estrategias "
                f"completas: (1) continuar = {s(r['e1'])}; (2) lanzar y reorientar = "
                f"{s(r['e2'])}; (3) lanzar y vender si hay baja aceptación = "
                f"{c['p_alta']:.2f}({c['g_alta']:,}) + {q:.2f}({c['venta']:,}) − "
                f"{c['costo_ini']:,} = {s(r['e3'])}. El recurso sí mejora el lanzamiento (de "
                f"{s(r['e3'])} a {s(r['e2'])}, {s(pc['aporte_recurso'])} más), pero no alcanza "
                f"para superar a la utilidad segura. Además, con la estrategia (2) hay "
                f"{pc['p_perdida']}% de probabilidad de terminar con una pérdida neta de "
                f"{s(-(c['u_des'] - c['inv_extra'] - c['costo_ini']))}, "
                f"y {r['prob_menor']*100:.0f}% de quedar por debajo de la utilidad segura. "
                f"Lanzar solo valdría la pena si la probabilidad de alta aceptación fuera mayor "
                f"que {r['p_eq']:.2f}, frente al {c['p_alta']:.2f} estimado.")
    m.por_que("La respuesta no puede limitarse a “se lanza porque tiene recurso”: el recurso "
              "(reorientar) sí mejora el resultado de lanzar frente a no tener esa opción, pero "
              "eso no basta para superar la alternativa segura; solo comparando los dos valores "
              "finales del nodo raíz —y no los valores intermedios— se llega a la recomendación "
              "correcta. Además, el valor esperado es un promedio: conviene mostrar cuánta "
              "probabilidad hay de quedar por debajo de la alternativa segura, y a partir de qué "
              "probabilidad cambiaría la decisión.")
    m.texto("Detalle de cómo se calculan los porcentajes (siempre hay que decir cuál es la "
            "base):")
    m.linea(f"Lanzar y reorientar frente a continuar (base = utilidad segura): ({r['e2']:,.0f} − "
            f"{r['e1']:,}) ÷ {r['e1']:,} × 100 = {num(r['e2'] - r['e1'])} ÷ {r['e1']:,} × 100 = "
            f"{pct(pc['e2_vs_e1'])}")
    m.linea(f"Lanzar y vender frente a continuar: ({r['e3']:,.0f} − {r['e1']:,}) ÷ "
            f"{r['e1']:,} × 100 = {num(r['e3'] - r['e1'])} ÷ {r['e1']:,} × 100 = "
            f"{pct(pc['e3_vs_e1'])}")
    m.linea(f"Aporte del recurso: {r['e2']:,.0f} − {r['e3']:,.0f} = {pc['aporte_recurso']:,.0f}, "
            f"que sobre la estrategia (3) es {pc['aporte_recurso']:,.0f} ÷ {r['e3']:,.0f} × 100 "
            f"= {pct(pc['aporte_rel'])}")
    m.linea(f"Probabilidad de cada resultado de la estrategia (2) = producto de las "
            f"probabilidades de su rama: alta aceptación {c['p_alta']:.2f} = {ph[0]}%; baja "
            f"aceptación y respuesta favorable {q:.2f} × {c['p_fav']:.2f} = "
            f"{q * c['p_fav']:.2f} = {ph[1]}%; baja aceptación y respuesta desfavorable "
            f"{q:.2f} × {1 - c['p_fav']:.2f} = {q * (1 - c['p_fav']):.2f} = {ph[2]}%. "
            f"Suma: {sum(ph)}%.")
    m.linea(f"Resultado neto en cada hoja de la estrategia (2): alta aceptación "
            f"{c['g_alta']:,} − {c['costo_ini']:,} = {s(c['g_alta'] - c['costo_ini'])}; favorable "
            f"{c['u_fav']:,} − {c['inv_extra']:,} − {c['costo_ini']:,} = "
            f"{s(c['u_fav'] - c['inv_extra'] - c['costo_ini'])}; desfavorable {c['u_des']:,} − "
            f"{c['inv_extra']:,} − {c['costo_ini']:,} = "
            f"{num(c['u_des'] - c['inv_extra'] - c['costo_ini'])}. Control: "
            f"{ph[0]/100:.2f}({c['g_alta'] - c['costo_ini']:,}) + {ph[1]/100:.2f}("
            f"{c['u_fav'] - c['inv_extra'] - c['costo_ini']:,}) + {ph[2]/100:.2f}("
            f"{num(c['u_des'] - c['inv_extra'] - c['costo_ini'])}) = {s(r['e2'])}, igual al "
            "resultado del roll-back.")
    m.linea(f"Probabilidad de alta aceptación de equilibrio p: p({c['g_alta']:,}) + "
            f"(1 − p)({r['nodo3']:,.0f}) − {c['costo_ini']:,} = {c['seguro']:,}  →  "
            f"{(c['g_alta'] - r['nodo3']):,.0f}p = {c['seguro'] + c['costo_ini'] - r['nodo3']:,.0f}"
            f"  →  p = {r['p_eq']:.4f} = {pc['p_eq']:.1f}%.")


def generar(docente):
    nombre = "Modelo_de_Sustentacion_2_DOCENTE.docx" if docente else \
        "Modelo_de_Sustentacion_2_ESTUDIANTE.docx"
    m = Modelo(docente, AQUI / "plantillas" / nombre)
    m.titulo(SUBTITULO)
    caso1(m); caso2(m); caso3(m)
    m.fin()
    m.doc.d.core_properties.title = "Sustentación Semana 7 – Serie B – " + (
        "Solucionario docente" if docente else "Hoja del estudiante")
    ruta = SALIDA / ("Modelo_de_Sustentacion_Semana7_SerieB_DOCENTE.docx" if docente
                     else "Hoja_de_Sustentacion_Semana7_SerieB_ESTUDIANTE.docx")
    m.doc.guardar(ruta)
    return ruta


if __name__ == "__main__":
    FIG.mkdir(exist_ok=True)
    FB.grafico_costos(FIG / "b_caso1_costos.png")
    FB.arbol_caso2(FIG / "b_caso2_arbol.png")
    FB.arbol_caso3(FIG / "b_caso3_arbol.png")
    for d in (True, False):
        print("generado:", generar(d))
