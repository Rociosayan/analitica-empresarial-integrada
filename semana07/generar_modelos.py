"""Genera los modelos de sustentación de la Semana 7 (DOCENTE y ESTUDIANTE).

Usa como base los .docx de la carpeta plantillas/ (encabezado, pie, estilos y
Tahoma 12 pt idénticos al modelo original) y toma TODOS los números de
calculos.py, de modo que el texto nunca puede contradecir a los cálculos.

Uso:  python generar_modelos.py      (requiere python-docx y matplotlib)
"""
import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Emu, Pt, RGBColor

import calculos as C
import figuras as F

AQUI = Path(__file__).parent
SALIDA = AQUI / "modelos"
FIG = AQUI / "figuras"

RED, DRED, GREEN, GREY = "FF0000", "9E1218", "1F7A3D", "595959"


# ------------------------------------------------------------------ formato
def s(x, dec=0):                       # S/ 13,200
    return f"S/ {x:,.{dec}f}"


def pct(x, dec=1, signo=False):
    t = f"{abs(x):.{dec}f}%"
    if x < 0:
        return "−" + t
    return ("+" + t) if signo else t


def num(x, dec=0, signo=False):
    """Número con coma de miles y signo menos tipográfico."""
    t = f"{abs(x):,.{dec}f}"
    if x < 0:
        return "−" + t
    return ("+" + t) if signo else t


def _fuente(run, b=False, i=False, color=None):
    rpr = run._r.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rpr.insert(0, rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs"):
        rf.set(qn(a), "Tahoma")
    run.font.size = Pt(12)
    run.font.bold = True if b else None
    run.font.italic = True if i else None
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


class Doc:
    def __init__(self, plantilla):
        self.d = Document(str(plantilla))
        body = self.d.element.body
        for el in list(body):
            if el.tag != qn("w:sectPr"):
                body.remove(el)

    def p(self, runs, before=None, after=None, jc="both", style=None, keep_next=False):
        par = self.d.add_paragraph(style=style)
        pf = par.paragraph_format
        if before is not None: pf.space_before = Pt(before / 20)
        if after is not None: pf.space_after = Pt(after / 20)
        par.alignment = {"both": WD_ALIGN_PARAGRAPH.JUSTIFY, "center": WD_ALIGN_PARAGRAPH.CENTER,
                         None: None, "left": None}[jc]
        if keep_next: pf.keep_with_next = True
        for r in runs:
            if isinstance(r, str):
                r = (r, {})
            txt, kw = r
            run = par.add_run(txt)
            _fuente(run, **kw)
        return par

    def imagen(self, ruta, ancho_emu, alto_emu):
        par = self.d.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.space_before = Pt(6); par.paragraph_format.space_after = Pt(6)
        run = par.add_run(); _fuente(run)
        run.add_picture(str(ruta), width=Emu(ancho_emu), height=Emu(alto_emu))

    def tabla(self, filas, anchos):
        t = self.d.add_table(rows=len(filas), cols=len(filas[0]))
        t.style = self.d.styles["Table Grid"]
        tblPr = t._tbl.tblPr
        for i, w in enumerate(anchos):
            t._tbl.tblGrid.findall(qn("w:gridCol"))[i].set(qn("w:w"), str(w))
        for ri, fila in enumerate(filas):
            for ci, txt in enumerate(fila):
                cell = t.cell(ri, ci)
                tcPr = cell._tc.get_or_add_tcPr()
                tcW = tcPr.find(qn("w:tcW"))
                if tcW is None:
                    tcW = OxmlElement("w:tcW"); tcPr.append(tcW)
                tcW.set(qn("w:w"), str(anchos[ci])); tcW.set(qn("w:type"), "dxa")
                par = cell.paragraphs[0]
                run = par.add_run(txt)
                if ri == 0:
                    shd = OxmlElement("w:shd")
                    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto")
                    shd.set(qn("w:fill"), DRED); tcPr.append(shd)
                    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    _fuente(run, b=True, color="FFFFFF")
                else:
                    if ci > 0: par.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    _fuente(run)
        return t

    def vacio(self):
        self.p([], jc=None)

    def limpiar_huerfanos(self):
        """Quita imágenes, gráficos y tinta de la plantilla que ya no se usan."""
        part = self.d.part
        xml = part.element.xml
        usados = set(re.findall(r'r:(?:embed|id|link|pict)="(rId\d+)"', xml))
        conservar = ("styles", "numbering", "settings", "fontTable", "theme", "webSettings",
                     "footnotes", "endnotes", "header", "footer", "customXml")
        for rid, rel in list(part.rels.items()):
            tipo = rel.reltype.rsplit("/", 1)[-1]
            es_tinta = "ink/" in (rel.target_ref or "")
            if rid not in usados and (es_tinta or not tipo.startswith(conservar)):
                del part.rels[rid]

    def guardar(self, ruta):
        self.limpiar_huerfanos()
        Path(ruta).parent.mkdir(exist_ok=True)
        self.d.save(str(ruta))


# ----------------------------------------------------------- bloques comunes
class Modelo:
    """Escribe el documento; `docente` añade rúbrica, 'Respuesta' y '¿Por qué?'."""

    def __init__(self, docente, plantilla):
        self.doc = Doc(plantilla)
        self.docente = docente
        self._espacio = None          # espacio de respuesta pendiente (solo estudiante)

    def _cerrar_pregunta(self):
        """Hoja del estudiante: deja el espacio en blanco para responder."""
        if self._espacio is None:
            return
        self.doc.p([("Respuesta:", dict(b=True, color=DRED))], before=40, after=40, jc=None)
        for _ in range(self._espacio):
            self.doc.vacio()
        self._espacio = None

    def fin(self):
        self._cerrar_pregunta()

    # encabezados
    def titulo(self):
        if self.docente:
            self.doc.p([("Sustentación", dict(b=True, color=RED)),
                        (" – SOLUCIONARIO DOCENTE", dict(b=True, color=RED))],
                       after=40, jc="center")
        else:
            self.doc.p([("Sustentación", dict(b=True, color=DRED))], after=40, jc="center")
            self.doc.p([("Nombre: ______________________________   Fecha: ____________",
                         dict(color=GREY))], after=80, jc="center")
        self.doc.p([("Semana 7 · Teoría de colas y Teoría de decisión",
                     dict(i=True, color=GREY))], jc="center")

    def caso(self, n, titulo, subtitulo):
        self._cerrar_pregunta()
        self.doc.p([(f"Caso {n}: ", dict(b=True, color=DRED)), (titulo, dict(b=True))],
                   before=280, after=80, jc=None, keep_next=True)
        self.doc.p([(subtitulo, dict(i=True, color=GREY))], jc=None, keep_next=True)

    def enunciado(self, texto, italica=False):
        self.doc.p([(texto, dict(i=italica))], after=160)

    def vineta(self, texto):
        self.doc.p([texto], after=80, jc=None, style="List Bullet")

    def pregunta(self, texto, criterio, espacio=5):
        self._cerrar_pregunta()
        if not self.docente:
            self._espacio = espacio
        runs = [(texto, dict(b=not self.docente))]
        if self.docente:
            runs.append((f"   [Criterio de la rúbrica: {criterio}]", dict(b=True, color=DRED)))
        self.doc.p(runs, before=120, after=80, keep_next=True)

    def respuesta(self, texto):
        if not self.docente:
            return
        runs = []
        if self.docente:
            runs.append(("Respuesta: ", dict(b=True, color=DRED)))
        runs.append((texto, dict(color=GREEN)))
        self.doc.p(runs, before=40, after=40)

    def linea(self, texto, color=GREEN, b=True):
        if not self.docente:
            return
        self.doc.p([(texto, dict(b=b, color=color))], after=40, jc=None)

    def texto(self, texto, italica=False):
        if not self.docente:
            return
        self.doc.p([(texto, dict(i=italica))], after=120)

    def nota(self, texto):
        if not self.docente:
            return
        self.doc.p([(texto, dict(i=True, color=GREY))], after=120)

    def imagen(self, nombre, ancho, alto):
        if self.docente:
            self.doc.imagen(FIG / nombre, ancho, alto)

    def tabla(self, filas, anchos):
        """Docente: cuadro resuelto. Estudiante: mismo cuadro con las celdas de resultado vacías."""
        self.doc.vacio()
        self.doc.tabla(filas, anchos)
        self.doc.vacio()

    def por_que(self, texto):
        if not self.docente:
            return
        self.doc.p([("¿Por qué se resuelve así?  ", dict(b=True, i=True, color=GREY)),
                    (texto, dict(i=True, color=GREY))])


# ------------------------------------------------------------------- caso 1
def escribir_caso1(m):
    r = C.caso1(); c = C.C1
    a, b = r[c["s_actual"]], r[c["s_propuesta"]]
    s6 = r[c["s_propuesta"] + 1]
    lam, mu = int(r["lam"]), int(r["mu"])
    m.caso(1, "Ampliación de la central de citas de CLÍNICA VALLE SUR", "Teoría de colas")
    m.enunciado("CLÍNICA VALLE SUR es una clínica privada peruana que atiende las solicitudes "
                "de citas médicas de sus pacientes a través de una central telefónica. Cuando "
                "un paciente llama, ingresa a una cola de espera hasta que un operador de citas "
                f"esté disponible. A un operador le toma, en promedio, {c['servicio_min']} minutos "
                "atender una llamada, con tiempos que se ajustan a una distribución exponencial. "
                f"Asimismo, se ha estimado que en promedio ingresan a la central {c['llamadas']} "
                f"llamadas cada {c['cada_min']} minutos, siguiendo una distribución de Poisson.")
    m.enunciado("Los operadores trabajan un solo turno diario de 8:00 a. m. a 4:00 p. m., de "
                f"lunes a viernes, {c['sem_mes']} semanas al mes, y tienen una remuneración de "
                f"{c['sueldo_dia']} soles diarios. Los costos del sistema telefónico son de "
                f"{c['plataforma_sem']} soles semanales por operador. Asimismo, se estima que por "
                "cada paciente que permanece en espera se incurre en un costo de oportunidad de "
                f"{c['costo_espera_h']} soles por hora.")
    m.enunciado("Actualmente, la clínica trabaja con el número mínimo de operadores que le "
                "garantiza poder atender a todos los pacientes que llaman; sin embargo, en las "
                "últimas semanas ha recibido numerosas quejas por la demora en la atención, por "
                "lo que se desea evaluar la conveniencia de contratar a un operador adicional. "
                "Esta propuesta debe estar sustentada en lo siguiente:")
    m.vineta(f"El paciente no debe esperar en cola más de {c['wq_max_min']} minutos por la "
             "atención del operador.")
    m.vineta("El costo total del servicio debe ser menor.")
    m.enunciado("Las tasas de llegada y de atención deben expresarse en pacientes/hora.",
                italica=True)

    # -- interpretación
    m.pregunta("¿Cuál es la situación problemática? (Debe incluir el problema a resolver, las "
               "distintas propuestas y el objetivo)", "INTERPRETACIÓN")
    m.respuesta("El problema es que CLÍNICA VALLE SUR atiende las solicitudes de citas por una "
                "central telefónica con operadores especializados y, en las últimas semanas, los "
                "pacientes esperan más de lo razonable en la cola, lo que genera quejas. Hay que "
                f"decidir entre dos propuestas: (1) mantener el esquema actual de {c['s_actual']} "
                f"operadores, o (2) ampliar a {c['s_propuesta']} operadores. El objetivo común es "
                "elegir la propuesta que cumpla la meta de servicio (espera máxima de "
                f"{c['wq_max_min']} minutos en cola) al menor costo mensual posible.")
    m.por_que("La interpretación exige traducir el relato a un problema formal de decisión: "
              "primero se nombran las alternativas concretas que se van a comparar (4 vs. 5 "
              "operadores), porque sin alternativas explícitas no hay nada que calcular después; "
              "luego se fija el objetivo común (cumplir la meta de espera al menor costo) porque "
              "ese objetivo es el que finalmente decide cuál propuesta gana en la pregunta de "
              "análisis.")

    # -- representación
    m.pregunta("¿Cómo representaría los modelos a comparar y las metas que debe alcanzar?",
               "REPRESENTACIÓN")
    m.respuesta("El sistema corresponde a un modelo de colas M/M/s (notación de Kendall): "
                "llegadas Poisson (M), tiempos de servicio exponenciales (M) y s servidores en "
                "paralelo (los operadores), con capacidad y población infinitas y disciplina "
                f"FIFO. Los parámetros son λ = {lam} pacientes/hora ({c['llamadas']} cada "
                f"{c['cada_min']} minutos) y μ = {mu} pacientes/hora por operador (1 atención "
                f"cada {c['servicio_min']} minutos), con s = {c['s_actual']} (actual) y "
                f"s = {c['s_propuesta']} (propuesta). El sistema es estable porque "
                f"ρ = λ/(s·μ) < 1; además, s = {c['s_actual']} es el mínimo posible, ya que "
                f"λ/μ = {r['lam']/r['mu']:.1f} y se necesita s > {r['lam']/r['mu']:.1f}. Las metas "
                "se expresan como dos medidas de rendimiento: el tiempo promedio de espera en "
                f"cola Wq (debe ser ≤ {c['wq_max_min']} min = {c['wq_max_min']/60:.2f} h) y el "
                "costo total mensual CT (debe ser menor en la propuesta).")
    m.por_que("Se usa la notación de Kendall porque dejar explícitos M/M/s obliga a verificar que "
              "se cumplen los supuestos (Poisson y exponencial) que habilitan las fórmulas de "
              "colas que se usarán en el siguiente paso; y las metas se expresan como medidas de "
              "rendimiento (Wq, CT) porque son exactamente lo que se va a calcular y comparar, no "
              "conceptos abstractos.")

    # -- cálculo
    m.pregunta("¿Qué cálculos debe obtener para evaluar las metas? (Debe ser presentado en un "
               "cuadro y presentar un gráfico que explique el comportamiento de los costos)",
               "CÁLCULO", espacio=8)
    m.respuesta("Se calcula el sistema M/M/s con la fórmula de Erlang C para s = "
                f"{c['s_actual']} y s = {c['s_propuesta']}, y se convierte cada resultado a un "
                "costo mensual:")
    hm = r["horas_mes"]
    filas = [["Medida", f"s = {c['s_actual']} (actual)", f"s = {c['s_propuesta']} (propuesta)"],
             ["λ (pacientes/hora)", f"{lam}", f"{lam}"],
             ["μ por operador (pacientes/hora)", f"{mu}", f"{mu}"],
             ["ρ = λ / (s·μ)", f"{a['rho']:.3f}", f"{b['rho']:.3f}"],
             ["P0 (prob. sistema vacío)", f"{a['p0']:.4f}", f"{b['p0']:.4f}"],
             ["P(espera) – Erlang C", f"{a['p_espera']:.3f}", f"{b['p_espera']:.3f}"],
             ["Wq (minutos)", f"{a['wq_min']:.2f}  (> {c['wq_max_min']} min: no cumple)",
              f"{b['wq_min']:.2f}  (≤ {c['wq_max_min']} min: cumple)"],
             ["Lq (pacientes en espera)", f"{a['lq']:.4f}", f"{b['lq']:.4f}"]]
    if m.docente:
        filas += [["Costo fijo mensual (planilla + plataforma)", s(a["fijo"]), s(b["fijo"])],
                  [f"Costo de espera mensual ({c['costo_espera_h']} soles/h × Lq × {hm} h/mes)",
                   s(a["espera"]), s(b["espera"])],
                  ["Costo total mensual", s(a["total"]), s(b["total"])]]
    else:
        d, w, sw = c["dias_sem"], c["sem_mes"], c["sueldo_dia"]
        pl = c["plataforma_sem"]
        filas += [
            ["Costo fijo mensual (planilla + plataforma)",
             f"{sw}×{d} días×{w} sem×{c['s_actual']} operadores + {pl}×{w} sem×{c['s_actual']} "
             f"operadores = {s(a['fijo'])}",
             f"{sw}×{d} días×{w} sem×{c['s_propuesta']} operadores + {pl}×{w} sem×"
             f"{c['s_propuesta']} operadores = {s(b['fijo'])}"],
            [f"Costo de espera mensual ({c['costo_espera_h']} soles/h × Lq × {hm} h/mes)",
             f"{c['costo_espera_h']} × {a['lq']:.4f} × {c['horas_dia']} h × {d} días × {w} sem = "
             f"{s(a['espera'])}",
             f"{c['costo_espera_h']} × {b['lq']:.4f} × {c['horas_dia']} h × {d} días × {w} sem = "
             f"{s(b['espera'])}"],
            ["Costo total mensual", f"{s(a['fijo'])} + {s(a['espera'])} = {s(a['total'])}",
             f"{s(b['fijo'])} + {s(b['espera'])} = {s(b['total'])}"]]
    if not m.docente:
        filas = [filas[0]] + [[f[0], "", ""] for f in filas[1:]]
    m.tabla(filas, [3489, 3489, 3489])
    m.texto(f"El costo fijo mensual por operador es {c['sueldo_dia']}×{c['dias_sem']*c['sem_mes']} "
            f"(planilla: {c['dias_sem']} días × {c['sem_mes']} semanas) + {c['plataforma_sem']}×"
            f"{c['sem_mes']} (plataforma) = {s(r['fijo_unit'])}; se multiplica por s. El costo de "
            "espera mensual parte de Lq = λ·Wq (número promedio de pacientes esperando en un "
            f"instante cualquiera), se valoriza a {c['costo_espera_h']} soles por hora y se "
            f"extiende a las {hm} horas de operación del mes ({c['horas_dia']} h × "
            f"{c['dias_sem']} d × {c['sem_mes']} sem). Los montos se calculan con Lq sin "
            "redondear y se muestran redondeados al sol.")
    # ---- detalle del cálculo de porcentajes (solo docente)
    ma, mb = round(a["wq_min"], 2), round(b["wq_min"], 2)
    la, lb = round(a["lq"], 4), round(b["lq"], 4)
    fa, fb = round(a["fijo"]), round(b["fijo"])
    ea, eb = round(a["espera"]), round(b["espera"])
    ta, tb = round(a["total"]), round(b["total"])
    meta = c["wq_max_min"]
    m.texto("Cómo se calcula el porcentaje (variación relativa). Paso 1: se toma como base el "
            f"valor actual (s = {c['s_actual']}), porque es la situación con la que se compara. "
            "Paso 2: se resta valor propuesta − valor actual (si da negativo la medida baja; si "
            "da positivo, sube). Paso 3: esa diferencia se divide entre la base y se multiplica "
            "por 100:")
    m.linea("Variación % = (valor propuesta − valor actual) ÷ valor actual × 100")
    var = lambda a_, b_, d: (f"({num(b_, d)} − {num(a_, d)}) ÷ {num(a_, d)} × 100 = "
                             f"{num(b_ - a_, d)} ÷ {num(a_, d)} × 100")
    filas_p = [["Medida", "Cálculo con los valores del cuadro", "Resultado"],
               ["Wq (min)", var(ma, mb, 2), pct(r["pct_wq"], signo=True)],
               ["Lq (pacientes)", var(la, lb, 4), pct(r["pct_lq"], signo=True)],
               ["Costo fijo mensual", var(fa, fb, 0), pct(r["pct_fijo"], signo=True)],
               ["Costo de espera mensual", var(ea, eb, 0), pct(r["pct_espera"], signo=True)],
               ["Costo total mensual", var(ta, tb, 0), pct(r["pct_total"], signo=True)]]
    if m.docente:
        m.tabla(filas_p, [2400, 5800, 2267])
    m.texto("Porcentajes respecto de la meta de espera (aquí la base es la meta de "
            f"{meta} minutos, no el valor actual): con s = {c['s_actual']}, "
            f"({num(ma, 2)} − {meta}) ÷ {meta} × 100 = {num(ma - meta, 2)} ÷ {meta} × 100 ≈ "
            f"{pct(r['pct_exceso_actual'], 0, True)}, es decir, se pasa de la meta en "
            f"{num(ma - meta, 2)} minutos; con s = {c['s_propuesta']}, "
            f"({num(mb, 2)} − {meta}) ÷ {meta} × 100 = {num(mb - meta, 2)} ÷ {meta} × 100 ≈ "
            f"{pct(r['pct_holgura_prop'], 0)}, es decir, queda {pct(-r['pct_holgura_prop'], 0)} "
            "por debajo del máximo permitido.")
    m.texto("Magnitudes que ya son porcentajes: utilización de los operadores = ρ × 100 → "
            f"s = {c['s_actual']}: {a['rho']:.3f} × 100 = {a['rho_pct']:.1f}%; "
            f"s = {c['s_propuesta']}: {b['rho']:.3f} × 100 = {b['rho_pct']:.1f}%. Probabilidad de "
            f"tener que esperar = P(espera) × 100 → s = {c['s_actual']}: {a['p_espera']:.3f} × 100 "
            f"= {a['pw_pct']:.1f}%; s = {c['s_propuesta']}: {b['p_espera']:.3f} × 100 = "
            f"{b['pw_pct']:.1f}%.")
    m.texto("Peso de cada componente en el costo total = componente ÷ costo total × 100 "
            f"(la base es el costo total de cada propuesta): s = {c['s_actual']}: costo fijo "
            f"{num(fa)} ÷ {num(ta)} × 100 = {a['peso_fijo']:.1f}% y costo de espera "
            f"{num(ea)} ÷ {num(ta)} × 100 = {a['peso_espera']:.1f}%; s = {c['s_propuesta']}: "
            f"costo fijo {num(fb)} ÷ {num(tb)} × 100 = {b['peso_fijo']:.1f}% y costo de espera "
            f"{num(eb)} ÷ {num(tb)} × 100 = {b['peso_espera']:.1f}%. Al contratar al quinto "
            "operador el costo deja de estar dominado por la espera y pasa a ser sobre todo costo "
            "fijo.")
    m.nota("Observaciones: (1) los porcentajes se calcularon con los valores que muestra el "
           "cuadro; con los valores sin redondear se obtiene el mismo resultado al decimal "
           "indicado. (2) El porcentaje depende de la base: el costo fijo sube "
           f"{pct(r['pct_fijo'])} respecto de s = {c['s_actual']}, pero volver de "
           f"s = {c['s_propuesta']} a s = {c['s_actual']} lo bajaría solo "
           f"{pct(-C.var_pct(fb, fa), 1)}. (3) No confundir porcentaje con puntos porcentuales: "
           f"ρ pasa de {a['rho_pct']:.1f}% a {b['rho_pct']:.1f}%, es decir, "
           f"{num(b['rho_pct'] - a['rho_pct'], 1)} puntos porcentuales, que equivalen a una "
           f"variación relativa de ({b['rho_pct']:.1f} − {a['rho_pct']:.1f}) ÷ "
           f"{a['rho_pct']:.1f} × 100 = {pct((b['rho_pct'] - a['rho_pct']) / a['rho_pct'] * 100)}.")
    m.imagen("caso1_costos.png", 5219700, 3103245)
    m.por_que("Wq y Lq se calculan con Erlang C —y no con fórmulas de M/M/1— porque hay varios "
              "servidores atendiendo en paralelo la misma cola única; usar M/M/1 aquí subestimaría "
              "la espera real. El costo se separa en “fijo” y “de espera” porque son las dos "
              "fuerzas que se mueven en direcciones opuestas al agregar un operador (el fijo sube, "
              "el de espera baja), y solo mostrando ambas por separado se puede argumentar después "
              "cuál efecto domina; el gráfico hace visible esa compensación de un vistazo, que es "
              "justamente lo que pide la pregunta.")

    # -- análisis
    m.pregunta("¿Qué propuesta es la mejor? Realice una discusión de resultados para argumentar "
               "su decisión.", "ANÁLISIS Y ARGUMENTACIÓN")
    exceso = a["wq_min"] - c["wq_max_min"]
    m.respuesta(f"La mejor propuesta es contratar al quinto operador (s = {c['s_propuesta']}). "
                "Cumple las dos condiciones planteadas: el tiempo de espera baja de "
                f"{a['wq_min']:.2f} a {b['wq_min']:.2f} minutos (con s = {c['s_actual']} se excede "
                f"la meta en {exceso:.2f} minutos, ≈{r['pct_exceso_actual']:.0f}% por encima de "
                f"los {c['wq_max_min']} minutos exigidos; con s = {c['s_propuesta']} se cumple con "
                f"holgura), y el costo total mensual baja de {s(a['total'])} a {s(b['total'])}, es "
                f"decir, un ahorro de {s(r['ahorro'])} al mes ({pct(-r['pct_total'])}). El ahorro "
                f"ocurre porque, aunque el costo fijo sube en {s(r['alza_fijo'])} "
                f"({pct(r['pct_fijo'])}) al pasar de 4 a 5 operadores, el costo de oportunidad por "
                f"las horas de espera de los pacientes cae en {s(r['caida_espera'])} "
                f"({pct(-r['pct_espera'])}), una reducción más de dos veces mayor que el aumento del "
                f"costo fijo. Además, no conviene ir más allá: con un sexto operador el costo total "
                f"({s(s6['total'])}) volvería a superar al de s = {c['s_propuesta']} "
                f"({s(b['total'])}).")
    m.por_que("La discusión no puede quedarse en “cumple la meta de tiempo” ni en “es más barato” "
              "por separado: hay que mostrar que ambas metas se cumplen a la vez y explicar el "
              "mecanismo económico (qué sube y qué baja, y por qué lo que baja pesa más) porque "
              "eso es lo que distingue una recomendación argumentada de una simple lectura de la "
              "tabla.")


# ------------------------------------------------------------------- caso 2
def escribir_caso2(m):
    r = C.caso2(); c = C.C2; p = r["pay"]; t, v = c["trad"], c["veg"]
    m.doc.vacio()
    m.caso(2, "Estrategia de renovación de la carta del restaurante “Sabores del Sur”",
           "Teoría de decisión – valor esperado, un nivel")
    m.enunciado("Marco Quispe, dueño del restaurante “Sabores del Sur”, debe decidir cómo invertir "
                "en su oferta para la próxima temporada: mantener únicamente su carta criolla "
                "tradicional o incorporar una línea de platos vegetarianos gourmet, con el "
                "objetivo de maximizar su utilidad neta. El resultado dependerá de la demanda del "
                "mercado, que prevé dos escenarios: alta demanda por tendencias saludables o "
                "demanda estable tradicional.")
    m.enunciado(f"Si opta por mantener solo la carta criolla, sus costos serán de {s(t['costo'])}; "
                "si hay alta demanda por tendencias saludables obtendría ingresos por "
                f"{s(t['ing_alta'])}, mientras que si hay demanda estable obtendría ingresos por "
                f"{s(t['ing_est'])}.")
    m.enunciado("Si opta por incorporar la línea vegetariana, sus costos serán de "
                f"{s(v['costo'])}; si hay alta demanda obtendría ingresos por {s(v['ing_alta'])}, "
                f"mientras que si hay demanda estable, dichos ingresos se reducirían en un "
                f"{v['caida']*100:.0f}%. Además, ha estimado que la probabilidad de alta demanda "
                f"por tendencias saludables es de {r['p']:.2f}.")

    m.pregunta("¿Cuál es la situación problemática, qué problema hay que resolver y con qué "
               "finalidad?", "INTERPRETACIÓN")
    m.respuesta("Marco debe decidir entre dos alternativas de inversión para el restaurante: "
                "mantener solo la carta criolla tradicional o incorporar una línea de platos "
                "vegetarianos gourmet. El problema por resolver es cuál de las dos alternativas "
                "conviene bajo la incertidumbre de la demanda (alta demanda saludable o demanda "
                "estable), y la finalidad es maximizar la utilidad neta esperada.")
    m.por_que("Antes de calcular cualquier valor esperado hay que dejar claro qué se está "
              "decidiendo (dos alternativas mutuamente excluyentes) y bajo qué incertidumbre (dos "
              "estados de demanda con una probabilidad dada); si no se nombra el criterio de "
              "decisión (maximizar la utilidad esperada) no queda claro qué herramienta aplicar "
              "después.")

    m.pregunta("¿Qué herramienta se utilizaría para resolver el problema? Presente los elementos, "
               "muestre el desarrollo de los cálculos necesarios para hallar los pagos y aplicar "
               "el criterio del valor esperado.", "REPRESENTACIÓN y CÁLCULO", espacio=12)
    m.respuesta("Se utiliza un árbol de decisión de un nivel: un nodo de decisión del que salen "
                "las dos alternativas, cada una con un nodo de azar con dos estados de la "
                "naturaleza. Primero se hallan los pagos (utilidad = ingreso − costo) de cada "
                "rama:")
    q = r["q"]
    filas = [["Alternativa", "Escenario", "Ingreso", "Costo", "Pago (utilidad)"],
             ["Carta criolla tradicional", f"Alta demanda saludable (P = {r['p']:.2f})",
              s(t["ing_alta"]), s(t["costo"]), s(p["trad_alta"])],
             ["Carta criolla tradicional", f"Demanda estable (P = {q:.2f})",
              s(t["ing_est"]), s(t["costo"]), s(p["trad_est"])],
             ["Línea vegetariana", f"Alta demanda saludable (P = {r['p']:.2f})",
              s(v["ing_alta"]), s(v["costo"]), s(p["veg_alta"])],
             ["Línea vegetariana", f"Demanda estable (P = {q:.2f})" + (" *" if m.docente else ""),
              s(r["ing_est_veg"]), s(v["costo"]), s(p["veg_est"])]]
    if not m.docente:
        filas = [filas[0]] + [[f[0], f[1], "", "", ""] for f in filas[1:]]
    m.tabla(filas, [2013, 1988, 1955, 1916, 1983])
    m.nota(f"* Demanda estable en la línea vegetariana = {s(v['ing_alta'])} × "
           f"(1 − {v['caida']:.2f}) = {s(r['ing_est_veg'])} (los ingresos se reducen "
           f"{v['caida']*100:.0f}% respecto del escenario de alta demanda).")
    m.imagen("caso2_arbol.png", 5303520, 3337173)
    m.texto("Con los pagos ya calculados se aplica el criterio del valor esperado en cada nodo de "
            "azar:")
    pt, pv = p["trad_alta"], p["veg_alta"]
    m.linea(f"VE(Carta criolla) = {r['p']:.2f}({pt:,}) + {q:.2f}({p['trad_est']:,}) = "
            f"{r['p']*pt:,.0f} + {q*p['trad_est']:,.0f} = {s(r['ve_trad'])}")
    m.linea(f"VE(Línea vegetariana) = {r['p']:.2f}({pv:,}) + {q:.2f}({p['veg_est']:,.0f}) = "
            f"{r['p']*pv:,.0f} + {q*p['veg_est']:,.0f} = {s(r['ve_veg'])}")
    m.por_que("El pago de cada rama se calcula como ingreso menos costo —y no solo el ingreso— "
              "porque lo que Marco maximiza es utilidad neta, según el propio objetivo planteado "
              "en la interpretación; y el valor esperado se calcula por separado para cada "
              "alternativa (y no un promedio global) porque cada alternativa tiene su propio par "
              "de pagos y debe compararse como un todo frente a la otra.")

    m.pregunta("¿Cuál es la mejor decisión? Realice una discusión de resultados para argumentar su "
               "elección.", "ANÁLISIS Y ARGUMENTACIÓN")
    rel = r["dif"] / r["ve_veg"] * 100
    m.respuesta("La mejor decisión es mantener solo la carta criolla tradicional, porque su valor "
                f"esperado ({s(r['ve_trad'])}) es mayor que el de incorporar la línea vegetariana "
                f"({s(r['ve_veg'])}), una diferencia de {s(r['dif'])} a favor de la carta "
                f"tradicional ({pct(rel)} más que la alternativa). En el escenario favorable (alta "
                f"demanda) la línea vegetariana solo supera a la tradicional en "
                f"{s(pv - pt)} ({s(pv)} frente a {s(pt)}), mientras que en el escenario "
                f"desfavorable (demanda estable, que es el más probable: P = {q:.2f}) rinde "
                f"{s(p['trad_est'] - p['veg_est'])} menos ({s(p['veg_est'])} frente a "
                f"{s(p['trad_est'])}). La línea vegetariana solo sería preferible si la "
                f"probabilidad de alta demanda superara aproximadamente {r['p_eq']:.2f}, muy por "
                f"encima del {r['p']:.2f} estimado.")
    pc = r["pct"]
    m.texto("Detalle de cómo se calculan los porcentajes (siempre hay que decir cuál es la "
            "base):")
    m.linea(f"Probabilidades: {r['p']:.2f} = {r['p']*100:.0f}% y {q:.2f} = {q*100:.0f}% "
            "(se multiplica por 100).")
    m.linea(f"Reducción del {v['caida']*100:.0f}% de los ingresos: {v['caida']:.2f} × "
            f"{v['ing_alta']:,} = {pc['caida_monto']:,.0f}; {v['ing_alta']:,} − "
            f"{pc['caida_monto']:,.0f} = {r['ing_est_veg']:,.0f} (equivale a {v['ing_alta']:,} × "
            f"{1 - v['caida']:.2f}).")
    m.linea(f"Diferencia de VE con base en la línea vegetariana: ({r['ve_trad']:,.0f} − "
            f"{r['ve_veg']:,.0f}) ÷ {r['ve_veg']:,.0f} × 100 = {r['dif']:,.0f} ÷ "
            f"{r['ve_veg']:,.0f} × 100 = {pct(pc['dif_sobre_veg'])} (la carta criolla rinde "
            f"{pct(pc['dif_sobre_veg'])} más).")
    m.linea(f"La misma diferencia con base en la carta criolla: {r['dif']:,.0f} ÷ "
            f"{r['ve_trad']:,.0f} × 100 = {pct(pc['dif_sobre_trad'])} (la línea vegetariana "
            f"rinde {pct(pc['dif_sobre_trad'])} menos). Son dos porcentajes distintos porque "
            "cambia la base.")
    m.linea(f"Escenario favorable: ({pv:,} − {pt:,}) ÷ {pt:,} × 100 = {pv - pt:,} ÷ {pt:,} × 100 "
            f"= {pct(pc['fav'], signo=True)}")
    m.linea(f"Escenario desfavorable: ({p['veg_est']:,.0f} − {p['trad_est']:,}) ÷ "
            f"{p['trad_est']:,} × 100 = {num(p['veg_est'] - p['trad_est'])} ÷ "
            f"{p['trad_est']:,} × 100 = {pct(pc['des'])}")
    m.linea(f"Probabilidad de equilibrio p: p({pt:,}) + (1 − p)({p['trad_est']:,}) = "
            f"p({pv:,}) + (1 − p)({p['veg_est']:,.0f})  →  {p['trad_est']:,} + "
            f"{pt - p['trad_est']:,}p = {p['veg_est']:,.0f} + {pv - p['veg_est']:,.0f}p  →  "
            f"{p['trad_est'] - p['veg_est']:,.0f} = {(pv - p['veg_est']) - (pt - p['trad_est']):,.0f}"
            f"p  →  p = {r['p_eq']:.4f} = {pc['p_eq']:.1f}%.")
    m.por_que(f"No basta con decir “se elige la de mayor valor esperado”: hay que mostrar cuánto "
              f"mayor es ({s(r['dif'])}) para que la recomendación sea cuantitativa, y conviene "
              "revisar también ambos escenarios para ver por qué el promedio favorece a una "
              "alternativa: la ganancia adicional en el escenario bueno es pequeña y la pérdida "
              "en el malo es grande. El punto de equilibrio de la probabilidad indica qué tan "
              "sensible es la decisión a la estimación de Marco.")


# ------------------------------------------------------------------- caso 3
def escribir_caso3(m):
    r = C.caso3(); c = C.C3; q = 1 - c["p_alta"]
    e2h = r["hojas_camp"]
    m.doc.vacio()
    m.caso(3, "Estrategia de expansión para la clínica veterinaria “Huellitas”",
           "Teoría de decisión – árbol con recurso, dos niveles")
    m.enunciado("Una clínica veterinaria evalúa si continuar operando únicamente con su "
                f"consultorio presencial, obteniendo una utilidad anual segura de {s(c['seguro'])}, "
                "o lanzar un servicio de telemedicina veterinaria con planes de suscripción, para "
                "lo cual deberá asumir costos iniciales de desarrollo de la plataforma y marketing "
                f"por {s(c['costo_ini'])}. Las ganancias y pérdidas que se indican a continuación "
                "no incluyen este costo inicial.")
    m.enunciado(f"Si decide lanzar el servicio, existe una probabilidad de {c['p_alta']*100:.0f}% "
                f"de lograr una alta aceptación entre los clientes, generando una ganancia de "
                f"{s(c['g_alta'])}. Sin embargo, existe una probabilidad de {q*100:.0f}% de no "
                "alcanzar la aceptación esperada, situación en la que deberá decidir entre lanzar "
                "una campaña de descuentos para atraer más suscriptores o cancelar el servicio.")
    m.enunciado("Si decide lanzar la campaña de descuentos, el mercado podría responder "
                f"favorablemente, con una probabilidad de {c['p_camp_fav']*100:.0f}%, generando una "
                f"utilidad de {s(c['u_camp_fav'])}, o desfavorablemente, con una probabilidad de "
                f"{(1-c['p_camp_fav'])*100:.0f}%, generando una utilidad de {s(c['u_camp_des'])}.")
    m.enunciado("Si decide cancelar el servicio, luego de cubrir penalidades contractuales y "
                f"liquidar los equipos, tendría una pérdida neta de {s(-c['cancelar'])}.")

    m.pregunta("Construya el árbol de decisión con todos sus elementos.", "REPRESENTACIÓN",
               espacio=16)
    if m.docente:
        m.respuesta("El árbol tiene dos niveles de decisión porque, a diferencia del Caso 2, aquí "
                    "una de las ramas de azar desemboca en una segunda decisión (con recurso) en "
                    "lugar de terminar directamente en un pago:")
    m.imagen("caso3_arbol.png", 5852160, 2926080)
    m.por_que("El nodo cuadrado 3 (segunda decisión) se dibuja porque la propia narración dice "
              "“deberá decidir entre lanzar una campaña de descuentos o cancelar”: eso es, por "
              "definición, otro punto de decisión del dueño del negocio, no un evento del azar, y "
              "por eso lleva símbolo de cuadrado y no de círculo. Se construye de izquierda a "
              "derecha en el orden cronológico real de las decisiones (primero lanzar o no, "
              "después —solo si hay baja aceptación— campaña o cancelar) porque así el árbol "
              "refleja la información disponible en cada momento.")

    m.pregunta("Desarrolle el criterio del valor esperado realizando los cálculos necesarios y "
               "tome la decisión que corresponda en cada nodo.", "CÁLCULO", espacio=12)
    m.respuesta("El árbol se resuelve “de atrás hacia adelante” (roll-back), empezando por el "
                "nodo más a la derecha:")
    fav, des = c["p_camp_fav"], 1 - c["p_camp_fav"]
    m.linea("1) Nodo de azar 4 “Campaña de descuentos”:", color=None)
    m.linea(f"VE(campaña) = {fav:.2f}({c['u_camp_fav']:,}) + {des:.2f}({c['u_camp_des']:,}) = "
            f"{fav*c['u_camp_fav']:,.0f} + {des*c['u_camp_des']:,.0f} = {s(r['ve_camp'])}")
    m.linea(f"2) Nodo de decisión 3 “baja aceptación”: se compara la campaña ({s(r['ve_camp'])}) "
            f"contra cancelar (−{s(-c['cancelar'])}).", color=None)
    m.linea(f"Se elige “campaña de descuentos” → valor del nodo = {s(r['nodo3'])}  (se descarta "
            f"cancelar, porque −{s(-c['cancelar'])} < {s(r['ve_camp'])})")
    m.linea("3) Nodo de azar 2 “lanzar el servicio” (usa el valor ya podado del paso anterior en "
            "la rama de baja aceptación):", color=None)
    m.linea(f"VE(lanzar, bruto) = {c['p_alta']:.2f}({c['g_alta']:,}) + {q:.2f}({r['nodo3']:,.0f}) "
            f"= {c['p_alta']*c['g_alta']:,.0f} + {q*r['nodo3']:,.0f} = {s(r['ve_bruto'])}")
    m.linea(f"VE(lanzar, neto) = {r['ve_bruto']:,.0f} − {c['costo_ini']:,} (costo inicial) = "
            f"{s(r['ve_neto'])}")
    m.linea(f"4) Nodo de decisión raíz 1: se compara lanzar ({s(r['ve_neto'])}) contra continuar "
            f"solo con el consultorio ({s(c['seguro'])}, valor seguro).", color=None)
    m.linea(f"Se elige “lanzar el servicio” → VE = {s(r['mejor'])}")
    m.por_que("El cálculo avanza de derecha a izquierda porque el valor de un nodo de decisión "
              "(como el nodo 3) solo puede conocerse después de saber cuánto vale cada una de sus "
              "ramas, y el valor de la rama “baja aceptación” del nodo 2 solo puede conocerse "
              "después de resolver el nodo 3; hacerlo en el orden inverso obligaría a adivinar el "
              "valor de una rama que aún no se ha calculado. En cada nodo de decisión se elige el "
              "mayor valor esperado (y se “poda” la otra rama) porque un decisor racional, llegado "
              "ese punto del árbol, siempre tomaría la opción que más le conviene en ese momento; "
              "y el costo inicial de S/ 40,000 se resta una sola vez, al final, porque es un costo "
              "único del proyecto que se paga en cualquier rama de “lanzar” (restarlo en cada "
              "hoja da exactamente el mismo resultado).")

    m.pregunta("¿Qué posibles estrategias se pueden seguir a partir del árbol construido?",
               "INTERPRETACIÓN")
    m.respuesta("Del árbol se desprenden tres estrategias completas: (1) continuar solo con el "
                "consultorio (no lanzar la telemedicina); (2) lanzar el servicio y, si hay baja "
                "aceptación, lanzar la campaña de descuentos; y (3) lanzar el servicio y, si hay "
                "baja aceptación, cancelar. No existe una cuarta estrategia “lanzar y no decidir "
                "nada si hay baja aceptación”, porque el propio caso obliga a tomar una de las dos "
                "acciones de recurso en ese punto.")
    m.por_que("En un árbol con recurso, una “estrategia” no es una sola rama sino un plan "
              "contingente completo: qué se hace al inicio y qué se hará después en cada punto de "
              "decisión futuro. Enumerarlas así, antes de comparar valores, evita el error común "
              "de evaluar “lanzar” como si fuera una sola apuesta, cuando en realidad incluye una "
              "decisión de segundo momento que cambia el resultado.")

    m.pregunta("¿Cuál es la mejor estrategia? Sustente su respuesta.", "ANÁLISIS Y ARGUMENTACIÓN")
    m.respuesta("La mejor estrategia es lanzar el servicio de telemedicina y, si hay baja "
                f"aceptación, lanzar la campaña de descuentos. Su valor esperado neto "
                f"({s(r['e2'])}) supera a la utilidad segura de continuar solo con el consultorio "
                f"({s(r['e1'])}) en {s(r['dif'])} ({pct(r['dif']/r['e1']*100)}). Comparando las "
                f"tres estrategias completas: (1) continuar = {s(r['e1'])}; (2) lanzar con "
                f"campaña = {s(r['e2'])}; (3) lanzar y cancelar si hay baja aceptación = "
                f"{c['p_alta']:.2f}({c['g_alta']:,}) + {q:.2f}(−{-c['cancelar']:,}) − "
                f"{c['costo_ini']:,} = {s(r['e3'])}. El recurso es lo que cambia la decisión: sin "
                f"la campaña, lanzar valdría {s(r['e1'] - r['e3'])} menos que continuar. Como "
                f"criterio de riesgo, con la estrategia (2) hay una probabilidad de "
                f"{r['prob_menor']*100:.0f}% de terminar con solo "
                f"{s(c['u_camp_des'] - c['costo_ini'])} (campaña desfavorable, ya descontado el "
                f"costo inicial), frente a la utilidad segura de {s(c['seguro'])}; con "
                f"{(1-r['prob_menor'])*100:.0f}% de probabilidad se obtienen "
                f"{s(e2h[1][1])} o más. Por eso se recomienda lanzar, aunque un dueño muy "
                "adverso al riesgo podría preferir la utilidad segura.")
    pc = r["pct"]
    m.texto("Detalle de cómo se calculan los porcentajes (siempre hay que decir cuál es la "
            "base):")
    m.linea(f"Ventaja de lanzar sobre continuar (base = utilidad segura): ({r['e2']:,.0f} − "
            f"{r['e1']:,}) ÷ {r['e1']:,} × 100 = {r['dif']:,.0f} ÷ {r['e1']:,} × 100 = "
            f"{pct(pc['e2_vs_e1'])}")
    m.linea(f"Lanzar y cancelar frente a continuar: ({r['e3']:,.0f} − {r['e1']:,}) ÷ "
            f"{r['e1']:,} × 100 = {num(r['e3'] - r['e1'])} ÷ {r['e1']:,} × 100 = "
            f"{pct(pc['e3_vs_e1'])}")
    m.linea(f"Aporte del recurso: {r['e2']:,.0f} − {r['e3']:,.0f} = {pc['aporte_recurso']:,.0f}, "
            f"que sobre la estrategia (3) es {pc['aporte_recurso']:,.0f} ÷ {r['e3']:,.0f} × 100 "
            f"= {pct(pc['aporte_rel'])}")
    ph = pc["p_hojas"]
    m.linea(f"Probabilidad de cada resultado de la estrategia (2) = producto de las "
            f"probabilidades de su rama: alta aceptación {c['p_alta']:.2f} = {ph[0]}%; baja "
            f"aceptación y respuesta favorable {q:.2f} × {c['p_camp_fav']:.2f} = "
            f"{q * c['p_camp_fav']:.2f} = {ph[1]}%; baja aceptación y respuesta desfavorable "
            f"{q:.2f} × {1 - c['p_camp_fav']:.2f} = {q * (1 - c['p_camp_fav']):.2f} = {ph[2]}%. "
            f"Suma: {sum(ph)}%.")
    m.por_que("La respuesta no puede limitarse a “se lanza porque el valor esperado es mayor”: hay "
              "que comparar los valores finales de las tres estrategias completas y mostrar qué "
              "aporta el recurso (sin él, la conclusión se invierte). Además, el valor esperado es "
              "un promedio: conviene mostrar cuánta probabilidad hay de quedar por debajo de la "
              "alternativa segura, para que la recomendación no oculte el riesgo.")


def main():
    FIG.mkdir(exist_ok=True)
    F.grafico_costos(FIG / "caso1_costos.png")
    F.arbol_caso2(FIG / "caso2_arbol.png")
    F.arbol_caso3(FIG / "caso3_arbol.png")
    for docente, nombre, plantilla in (
            (True, "Modelo_de_Sustentacion_Semana7_DOCENTE.docx",
             "Modelo_de_Sustentacion_2_DOCENTE.docx"),
            (False, "Hoja_de_Sustentacion_Semana7_ESTUDIANTE.docx",
             "Modelo_de_Sustentacion_2_ESTUDIANTE.docx")):
        m = Modelo(docente, AQUI / "plantillas" / plantilla)
        m.titulo()
        escribir_caso1(m)
        escribir_caso2(m)
        escribir_caso3(m)
        m.fin()
        m.doc.d.core_properties.title = "Sustentación Semana 7 – " + (
            "Solucionario docente" if docente else "Hoja del estudiante")
        m.doc.guardar(SALIDA / nombre)
        print("generado:", SALIDA / nombre)


if __name__ == "__main__":
    main()
